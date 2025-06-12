<div align="right">
<a href="./README.md">Read in English 🇬🇧</a>
</div>

# ⌛ 时间感知 (Time Awareness) Filter for Open WebUI

这是一个为 [Open WebUI](https://github.com/open-webui/open-webui) 设计的强大 Filter，旨在为您的每一次对话注入精确的时间上下文。它会自动为历史消息和当前发送的消息添加时间戳，让大语言模型能够准确理解对话发生的时间背景，从而提供更精准、更具上下文感知能力的回答。

[![作者](https://img.shields.io/badge/作者-CookSleep-blue.svg)](https://github.com/CookSleep)
[![版本](https://img.shields.io/badge/版本-1.0-brightgreen.svg)]()
[![兼容性](https://img.shields.io/badge/Open_WebUI-%3E%3D0.6.10-orange.svg)]()

## ✨ 主要功能

- **全自动时间注入**：自动为对话中的所有用户消息添加时间戳。
- **智能格式化**：
  - 在新的一天开始时，会自动显示完整的日期（`[年-月-日, 星期, 时:分:秒]`）。
  - 对于当天内的后续消息，则只显示简洁的时间（`[时:分:秒]`），增强可读性。
- **强大的兼容性**：
  - 支持纯文本消息。
  - 支持图文混合消息。
  - 支持纯图片或纯文件消息（会自动创建时间戳文本）。
- **高可配置性**：
  - 自定义你所在的时区。
  - 多种日期格式可供选择（ISO, DMY, MDY 等）。
- **健壮的错误处理**：在无法获取历史记录时（如 Token 错误），会自动跳过注入，保证对话的正常进行，并提供清晰的错误提示。
- **实时开关**：可以在 Open WebUI 界面上随时启用或禁用此 Filter。

## ⚙️ 配置方法

[导入](https://openwebui.com/f/cooksleep/%E6%97%B6%E9%97%B4%E6%84%9F%E7%9F%A5)并启用 Filter （还需要点击“更多”，开启“全局”，这样才会显示在任何对话中）后，点击 “管理员面板-函数-时间感知”右侧的齿轮图标，您会看到以下配置选项：

-   **`api_base_url` (必需)**:
    -   **描述**: Open WebUI 后端的地址。
    -   **默认值**: `http://127.0.0.1:8080`

-   **`auth_token` (必需)**:
    -   **描述**: 用于认证的令牌 (支持 JWT 或 API 密钥)。**这是保证 Filter 能读取历史记录中消息时间戳的关键**。
    -   **如何获取**:
        1.  在浏览器中登录 Open WebUI。
        2.  进入“设置” > “账户” > “API密钥”。
        3.  点击“显示”，然后复制“**JWT令牌**”或“**API密钥**”字段的内容。
        4.  将复制的令牌粘贴到这里。
    -   **提示**: 如果看不到 API 密钥，请前往“管理员面板”>“设置”>“通用”，打开“启用 API 密钥”并点击“保存”按钮。

-   **`timezone`**:
    -   **描述**: 你所在的时区 (IANA 标准名称)。
    -   **默认值**: `Asia/Shanghai`
    -   **示例**: `America/New_York`, `Europe/London`

-   **`date_format`**:
    -   **描述**: 日期显示格式。
    -   **默认值**: `ISO`
    -   **可选值**:
        -   `"ISO"` (2025-06-13)
        -   `"DMY_SLASH"` (13/06/2025)
        -   `"MDY_SLASH"` (06/13/2025)
        -   `"DMY_DOT"` (13.06.2025)

-   **`debug_print_request`**:
    -   **描述**: 在 **Open WebUI 后端日志**中打印详细的调试信息，用于排查问题。
    -   **默认值**: `False`

## ⚠️ 注意事项

-   此 Filter 需要 `httpx` 库。如果您是手动部署 Open WebUI（非 Docker），请确保已安装：`pip install httpx`。Docker 用户无需担心，镜像已包含此库。
-   关于 `auth_token`：请注意 **JWT（JSON Web 令牌）是有时效性的**，会过期。如果 Filter 突然停止工作并提示错误，很可能是您的 JWT 过期了。相比之下，**标准的 API 密钥通常不会过期**，除非被手动吊销。为了长期稳定使用，推荐配置 API 密钥。

## 💬 反馈与贡献

如果您遇到任何问题或有改进建议，欢迎随时在 GitHub 上 [提交 Issue](https://github.com/CookSleep/Time-Awareness-Filter-for-Open-WebUI/issues)。

## 📜 许可证

本项目采用 MIT 许可证。
