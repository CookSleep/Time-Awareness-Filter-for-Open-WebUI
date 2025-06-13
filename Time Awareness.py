"""
title: Time Awareness
author: https://github.com/CookSleep
description: Injects accurate time context into all user messages, including historical ones. It handles various message types and optimizes readability. Supports multiple users and automatically detects user timezone and auth info without manual configuration.
version: 1.1
"""
import time
import datetime
import logging
import json
import zoneinfo
from typing import Any, Optional, Dict, List, Callable, Union
from collections import defaultdict
from pydantic import BaseModel, Field

# --- httpx (needs to be installed via `pip install httpx`) ---
try:
    import httpx
except ImportError:
    httpx = None

# --- Logger Setup ---
LOGGER = logging.getLogger("TimeAwareness_v1_1")
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s[%(name)s]%(lineno)s:%(asctime)s: %(message)s"))
if not LOGGER.handlers:
    LOGGER.addHandler(handler)


class Filter:
    class Valves(BaseModel):
        api_base_url: str = Field(default="http://127.0.0.1:8080", description="The base URL of your Open WebUI backend.")
        date_format: str = Field(default="ISO", description='The date format. E.g., "ISO" (2025-06-13), "DMY_SLASH" (13/06/2025), "MDY_SLASH" (06/13/2025), "DMY_DOT" (13.06.2025).')
        debug_print_request: bool = Field(default=False, description="Log detailed debugging information and performance metrics.")

    def __init__(self):
        self.valves = self.Valves()
        self.toggle = True
        self.icon = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNsb2NrIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIvPjxwb2x5bGluZSBwb2ludHM9IjEyIDYgMTIgMTIgMTYgMTQiLz48L3N2Zz4="
        self.weekday_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        if not httpx: 
            LOGGER.error("The `httpx` library is not installed. The Time Awareness Filter will not work. Please run `pip install httpx`.")

    def _extract_jwt_from_request(self, request) -> Optional[str]:
        try:
            auth_header = request.headers.get("authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                if token and "." in token:
                    return token
            LOGGER.warning("Could not find a valid Bearer Token in the request headers.")
            return None
        except Exception as e:
            LOGGER.error(f"Error extracting JWT token: {e}")
            return None

    async def _get_chat_history(self, chat_id: str, jwt_token: str, event_emitter: Optional[Callable]) -> Optional[Dict]:
        if not httpx: return None
        if not jwt_token:
            LOGGER.error("Authentication token (JWT) is empty, cannot fetch chat history.")
            if event_emitter: 
                await event_emitter({"type": "notification", "data": {"type": "error", "content": "Time Awareness: Cannot get user auth info"}})
            return None

        api_url = f"{self.valves.api_base_url.strip('/')}/api/v1/chats/{chat_id}"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            LOGGER.error(f"Error fetching or parsing chat history: {e}")
            if event_emitter: 
                await event_emitter({"type": "notification", "data": {"type": "error", "content": "Time Awareness: Failed to get history"}})
        return None

    def get_time_prefix(self, dt_object: datetime.datetime, is_full_format: bool) -> str:
        time_str = dt_object.strftime("%H:%M:%S")
        if is_full_format:
            format_str = {"ISO": "%Y-%m-%d", "DMY_SLASH": "%d/%m/%Y", "MDY_SLASH": "%m/%d/%Y", "DMY_DOT": "%d.%m.%Y"}.get(self.valves.date_format, "%Y-%m-%d")
            date_str = dt_object.strftime(format_str)
            weekday_str = self.weekday_map[dt_object.weekday()]
            return f"[{date_str}, {weekday_str}, {time_str}]"
        else:
            return f"[{time_str}]"

    def _get_text_from_content(self, content: Union[str, list, None]) -> str:
        if isinstance(content, str): return content
        if isinstance(content, list):
            return "\n".join([p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"])
        return ""

    async def inlet(self, body: dict, __metadata__: Optional[dict] = None, __event_emitter__: Optional[Callable] = None, __request__: Optional[object] = None) -> dict:
        start_time = time.time()
        
        if not self.toggle or not __request__:
            if not __request__: LOGGER.warning("Could not access __request__, skipping time injection.")
            return body

        if self.valves.debug_print_request: LOGGER.info("--- Time Awareness Filter starting ---")

        messages_to_send = body.get("messages", [])
        if not messages_to_send: return body
        
        # Automatically detect timezone, fall back to UTC
        user_timezone_str = "UTC"
        if __metadata__ and isinstance(__metadata__.get("variables"), dict):
            tz_from_meta = __metadata__["variables"].get("{{CURRENT_TIMEZONE}}")
            if tz_from_meta:
                user_timezone_str = tz_from_meta
            else:
                LOGGER.warning("Could not find timezone in metadata, falling back to UTC.")

        try:
            tz = zoneinfo.ZoneInfo(user_timezone_str)
        except Exception as e:
            LOGGER.error(f"Invalid timezone '{user_timezone_str}', falling back to UTC. Error: {e}")
            tz = zoneinfo.ZoneInfo("UTC")

        # If it's a new chat, just add a timestamp to the current message
        chat_id = __metadata__.get("chat_id") if __metadata__ else None
        if not chat_id:
            if messages_to_send[-1].get("role") == "user":
                time_prefix = self.get_time_prefix(datetime.datetime.now(tz), is_full_format=True)
                last_message = messages_to_send[-1]
                content = last_message.get("content")
                
                if self._get_text_from_content(content).strip().startswith("["): return body
                
                if isinstance(content, str):
                    last_message["content"] = f"{time_prefix}\n{content}"
                elif isinstance(content, list):
                    content.insert(0, {"type": "text", "text": f"{time_prefix}\n"})
            return body

        # For existing chats, fetch history and inject time
        jwt_token = self._extract_jwt_from_request(__request__)
        chat_history_data = await self._get_chat_history(chat_id, jwt_token, __event_emitter__)
        if not chat_history_data:
            LOGGER.warning("Failed to get chat history, skipping time injection.")
            return body

        content_to_timestamps_map = defaultdict(list)
        history_messages = chat_history_data.get("chat", {}).get("history", {}).get("messages", {})
        
        if isinstance(history_messages, dict):
            sorted_history = sorted(history_messages.values(), key=lambda msg: msg.get("timestamp", 0))
            for msg_data in sorted_history:
                if isinstance(msg_data, dict) and msg_data.get("role") == "user":
                    text_content = self._get_text_from_content(msg_data.get("content"))
                    if "timestamp" in msg_data:
                        content_to_timestamps_map[text_content].append(msg_data.get("timestamp"))

        last_user_message_idx = -1
        for i in range(len(messages_to_send) - 1, -1, -1):
            if messages_to_send[i].get("role") == "user":
                last_user_message_idx = i; break

        last_processed_date: Optional[datetime.date] = None
        for i, message in enumerate(messages_to_send):
            if message.get("role") == "user":
                content = message.get("content")
                text_content = self._get_text_from_content(content)
                if text_content.strip().startswith('['): continue

                current_dt = None
                if i == last_user_message_idx:
                    current_dt = datetime.datetime.now(tz)
                else:
                    timestamp_queue = content_to_timestamps_map.get(text_content)
                    if timestamp_queue:
                        timestamp = timestamp_queue.pop(0)
                        current_dt = datetime.datetime.fromtimestamp(timestamp, tz)
                    else: continue
                
                if not current_dt: continue

                use_full_format = (last_processed_date is None) or (current_dt.date() != last_processed_date)
                time_prefix = self.get_time_prefix(current_dt, use_full_format)

                if isinstance(content, str): message["content"] = f"{time_prefix}\n{content}"
                elif isinstance(content, list):
                    text_part_found = False
                    for part in content:
                        if part.get("type") == "text":
                            part["text"] = f"{time_prefix}\n{part.get('text', '')}"; text_part_found = True; break
                    if not text_part_found: content.insert(0, {"type": "text", "text": f"{time_prefix}\n"})

                last_processed_date = current_dt.date()

        if self.valves.debug_print_request:
            LOGGER.info(f"Final messages sent to model:\n{json.dumps(messages_to_send, indent=2, ensure_ascii=False)}")
            end_time = time.time()
            LOGGER.info(f"--- Time Awareness Filter finished in: {end_time - start_time:.4f} seconds ---")

        return body
