# SimpletexC

基于 Flet 的 SimpleTex 公式识别桌面客户端。支持剪贴板粘贴图片，自动识别 LaTeX 公式并实时预览。

## 功能

- **Ctrl+V 粘贴** — 从剪贴板粘贴截图，自动识别公式
- **实时预览** — 识别结果以 Markdown/LaTeX 格式实时渲染
- **自动复制** — 识别后自动将结果复制到剪贴板

## 使用

```bash
uv run flet run
```

首次使用前，在设置页填入你的 SimpleTex UAT（访问 [simpletex.cn](https://simpletex.cn) 获取）。

## 项目结构

```
src/
├── main.py      # 主界面和交互逻辑
├── mathocr.py   # SimpleTex API 调用封装
└── assets/      # 资源文件
```

## 开发

### 环境要求

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 初始化

```bash
uv sync
```

### 运行

```bash
uv run flet run
```

Web 模式：

```bash
uv run flet run --web
```

### 项目结构

```
src/
├── main.py        # 主界面和交互逻辑
├── mathocr.py     # SimpleTex API 调用封装
└── assets/        # 资源文件（图标等）
```

### 开发说明

- `main.py` 中 `main()` 函数是应用入口，使用 `ft.run(main)` 启动
- 页面通过 `NavigationBar` 切换首页和设置页
- 设置通过 `settings.json` 持久化，启动时自动加载
- OCR 调用在后台线程执行（`asyncio.to_thread`），不阻塞 UI

### 依赖

核心依赖定义在 `pyproject.toml` 的 `[project] dependencies` 中，开发依赖在 `[dependency-groups] dev` 下。

## 打包为 Windows 应用

### 前提

安装 [NSIS](https://nsis.sourceforge.io/Download)（打包安装程序用），并确保 `makensis.exe` 在系统 PATH 中。

### 打包命令

```bash
flet build windows -v
```

打包后的文件输出到 `dist/` 目录。

如需指定应用图标、产品名等，在 `pyproject.toml` 的 `[tool.flet]` 中配置：

```toml
[tool.flet]
org = "com.mycompany"
product = "simpletexc"
company = "Flet"
copyright = "Copyright (C) 2023-2026 by Flet"

[tool.flet.app]
path = "src"
```

更多配置项参考 [Flet Windows 打包指南](https://flet.dev/docs/publish/windows/)。

其他平台（Android / iOS / macOS / Linux / Web）打包方式见 [Flet 打包文档](https://flet.dev/docs/publish)。

## 技术栈

- [Flet](https://flet.dev/) — GUI 框架
- [SimpleTex API](https://simpletex.cn/) — 公式识别服务
- [requests](https://requests.readthedocs.io/) — HTTP 客户端
