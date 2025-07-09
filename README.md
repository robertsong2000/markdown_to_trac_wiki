# Markdown to Trac Wiki Converter

这是一个简单的Web应用程序，用于将Markdown格式的文本转换为Trac Wiki格式。

## 项目结构

- `app.py`: Flask后端应用程序，处理Markdown到Trac Wiki的转换逻辑。
- `static/index.html`: 前端用户界面，包含输入和输出文本框以及转换按钮。
- `requirements.txt`: Python依赖列表。

## 功能

- 将Markdown文本转换为Trac Wiki格式。
- 支持基本的Markdown语法，如标题、粗体、斜体、链接、列表和代码块。
- 优化了表格转换，将Markdown的 `|` 转换为 Trac Wiki 的 `||`。

## 安装与运行

请按照以下步骤在本地运行此应用程序：

1.  **克隆仓库 (如果尚未克隆):**

    ```bash
    git clone <repository_url>
    cd markdown_to_trac_wiki
    ```

2.  **创建并激活虚拟环境 (推荐):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    ```

3.  **安装依赖:**

    ```bash
    pip install -r requirements.txt
    # 如果遇到权限问题，可以尝试使用 --break-system-packages
    # pip install -r requirements.txt --break-system-packages
    ```

4.  **运行Flask应用:**

    ```bash
    python3 app.py
    ```

5.  **访问应用:**

    应用程序启动后，在浏览器中打开 `http://127.0.0.1:5000` 即可访问转换工具。

## 使用方法

1.  在左侧的文本框中输入Markdown格式的文本。
2.  点击“Convert to Trac Wiki”按钮。
3.  转换后的Trac Wiki格式文本将显示在右侧的文本框中。

## 改进建议

-   **更强大的Markdown解析：** 考虑使用 `markdown-it-py` 等库进行更健壮的Markdown解析，以支持更复杂的语法和更精确的转换。
-   **错误处理：** 增强后端错误处理和前端用户反馈机制。
-   **自动化测试：** 为转换逻辑和API端点添加单元测试和集成测试。
-   **部署优化：** 在生产环境中使用WSGI服务器（如Gunicorn）和Web服务器（如Nginx）来服务应用和静态文件。