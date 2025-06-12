<div align="right">
<a href="./README_zh-CN.md">简体中文 🇨🇳</a>
</div>

# ⌛ Time Awareness Filter for Open WebUI

This is a powerful Filter designed for [Open WebUI](https://github.com/open-webui/open-webui) to inject precise temporal context into your conversations. It automatically adds timestamps to both historical and current messages, enabling the Large Language Model to understand the timeline of your dialogue and provide more accurate, context-aware responses.

[![Author](https://img.shields.io/badge/Author-CookSleep-blue.svg)](https://github.com/CookSleep)
[![Version](https://img.shields.io/badge/Version-1.0-brightgreen.svg)]()
[![Compatibility](https://img.shields.io/badge/Open_WebUI-%3E%3D0.6.10-orange.svg)]()

## ✨ Key Features

- **Fully Automatic Time Injection**: Automatically prepends timestamps to all user messages in a conversation.
- **Smart Formatting**:
  - Displays the full date (`[YYYY-MM-DD, Weekday, HH:MM:SS]`) at the start of a new day.
  - Uses a concise time format (`[HH:MM:SS]`) for subsequent messages within the same day to enhance readability.
- **Robust Compatibility**:
  - Supports plain text messages.
  - Supports mixed content messages (text with images).
  - Supports media-only messages (images or files), automatically creating a timestamp text block.
- **Highly Configurable**:
  - Customize your local timezone.
  - Choose from multiple date formats (ISO, DMY, MDY, etc.).
- **Resilient Error Handling**: Gracefully skips injection and provides clear notifications if it fails to fetch chat history (e.g., due to an invalid token), ensuring your conversation is not interrupted.
- **Real-time Toggle**: Easily enable or disable the filter on-the-fly from the Open WebUI interface.

## ⚙️ Configuration

After [importing](https://openwebui.com/f/cooksleep/time_awareness) and enabling the Filter, click the gear icon to the right of "Time Awareness" under **Admin Panel > Functions** to find the following options:

-   **`api_base_url` (Required)**:
    -   **Description**: The base URL of your Open WebUI backend.
    -   **Default**: `http://127.0.0.1:8080`

-   **`auth_token` (Required)**:
    -   **Description**: The authentication token (supports JWT or API Key) for the Open WebUI API. **This is the key to ensuring that the Filter can read the timestamps of messages in the history.**
    -   **How to get it**:
        1.  Log in to Open WebUI in your browser.
        2.  Go to "Settings" > "Account" > "API Keys".
        3.  Click "Show" and copy the content of either the **"JWT Token"** or **"API Key"** field.
        4.  Paste the copied token here.
    -   **Tip**: If you don't see an API Key, go to "Admin Panel" > "Settings" > "General", turn on "Enable API Key" and click "Save".

-   **`timezone`**:
    -   **Description**: Your local timezone (IANA standard name).
    -   **Default**: `Asia/Shanghai`
    -   **Examples**: `America/New_York`, `Europe/London`

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
-   Regarding the `auth_token`: Please be aware that **JWTs have a limited lifetime** and will expire. If the filter suddenly stops working and shows an error, your JWT has likely expired. In contrast, **standard API Keys generally do not expire** unless revoked. For long-term stability, using an API Key is recommended.

## 💬 Feedback & Contributing

If you encounter any issues or have suggestions for improvement, please feel free to [open an issue](https://github.com/CookSleep/Time-Awareness-Filter-for-Open-WebUI/issues) on GitHub.

## 📜 License

This project is licensed under the MIT License.
