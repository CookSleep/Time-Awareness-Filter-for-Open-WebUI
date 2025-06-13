<div align="right">
<a href="./README_zh-CN.md">简体中文 🇨🇳</a>
</div>

# ⌛ Time Awareness Filter for Open WebUI

This is a powerful Filter designed for [Open WebUI](https://github.com/open-webui/open-webui) to inject precise temporal context into your conversations. It automatically adds timestamps to both historical and current messages, enabling the Large Language Model to understand the timeline of your dialogue and provide more accurate, context-aware responses.

[![Author](https://img.shields.io/badge/Author-CookSleep-blue.svg)](https://github.com/CookSleep)
[![Version](https://img.shields.io/badge/Version-1.1-brightgreen.svg)]()
[![Compatibility](https://img.shields.io/badge/Open_WebUI-%3E%3D0.6.10-orange.svg)]()

## ✨ Key Features

- **Fully Automatic Time Injection**: Automatically prepends timestamps to all user messages.
- **Zero-Config Auth & Timezone**: Automatically detects the current user's authentication info and timezone, eliminating any manual setup for true multi-user support out of the box.
- **Smart Formatting**:
  - Displays the full date (`[YYYY-MM-DD, Weekday, HH:MM:SS]`) at the start of a new day.
  - Uses a concise time format (`[HH:MM:SS]`) for subsequent messages within the same day to enhance readability.
- **Robust Compatibility**:
  - Supports plain text, text with images, and file-only messages.
- **Resilient Error Handling**: Gracefully skips injection if it fails to fetch chat history, ensuring your conversation is not interrupted.
- **Real-time Toggle**: Easily enable or disable the filter on-the-fly from the Open WebUI interface.

## ⚙️ Configuration

After [importing](https://openwebui.com/f/cooksleep/time_awareness) and enabling the Filter (You also need to click "More" and enable "Global" so that it appears in all conversations), click the gear icon to the right of "Time Awareness" under **Admin Panel > Functions** to find the following options:

-   **`api_base_url`**:
    -   **Description**: The base URL of your Open WebUI backend.
    -   **Default**: `http://127.0.0.1:8080`

-   **`date_format`**:
    -   **Description**: The display format for the date.
    -   **Default**: `ISO`
    -   **Options**:
        -   `"ISO"` (2025-06-13)
        -   `"DMY_SLASH"` (13/06/2025)
        -   `"MDY_SLASH"` (06/13/2025)
        -   `"DMY_DOT"` (13.06.2025)

-   **`debug_print_request`**:
    -   **Description**: Logs detailed debugging information to the **Open WebUI backend logs**, useful for troubleshooting.
    -   **Default**: `False`

## ⚠️ Important Notes

-   This filter requires the `httpx` library. If you have a manual (non-Docker) installation of Open WebUI, ensure it's installed: `pip install httpx`. Docker users don't need to worry, as it's included in the image.
-   Please ensure the `api_base_url` is configured correctly so the Filter can reach the Open WebUI API.

## 💬 Feedback & Contributing

If you encounter any issues or have suggestions for improvement, please feel free to [open an issue](https://github.com/CookSleep/Time-Awareness-Filter-for-Open-WebUI/issues) on GitHub.

## 📜 License

This project is licensed under the MIT License.
