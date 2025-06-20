# 51Neo-V2

51Neo-V2 是一个第三方项目，旨在为 51school 提供 Neo UI 界面。该项目通过逆向工程技术获取 51 校园平台的数据，并通过 API 与之进行交互。与前一个版本相比，V2 版本将原先的后端架构由基于 JavaScript 的 `worker.js` 重写为 Python 后端，提供更高的性能和灵活性。项目的核心目标是作为一个概念演示，向开发者展示如何通过逆向获取和处理 51school 的数据，以及如何与其 API 进行高效的交互。

## 项目介绍

51Neo-V2是基于Python重写的后端系统以及一套现代化的UI，旨在提供与51school平台的数据交互接口。该项目通过逆向API技术获取51校园中的各种数据，帮助用户更便捷地访问校园资源。通过该系统，用户可以轻松查询学生的基本信息、大头照、通讯码、UUID等数据，提升校园查询的效率与便利性。

### 特点

- **全新Python后端**：V2版本完全重写了后端，采用了Python编写，提升了代码可维护性与稳定性。
- **逆向API获取数据**：通过逆向API接口，获取51school上的学生数据与其他相关信息。
- **概念演示**：本项目仅用于概念验证和学习交流，不应用于商业化或者恶意用途。

## 安装与运行

### 前提条件

- Python 3.8及以上
- 必要的Python库（可以通过`requirements.txt`文件安装）
```
dotenv==0.9.9
python-dotenv==1.0.1
```

### 安装步骤

1. 克隆该项目：
```bash
git clone https://github.com/jijingxing/51Neo-v2.git
cd 51Neo-V2
```

2. 创建虚拟环境：
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4 启动后端服务：
```bash
python3 app.py
```

5. 默认情况下，服务将在`http://localhost:8000`启动，您可以通过浏览器或API客户端访问。

## 使用说明

1. 打开浏览器，访问`http://localhost:8000`，您将看到51Neo WebUI界面。
2. 在WebUI中，您可以查看与51school平台相关的各种数据（例如大头照，学生信息等）。
3. 该项目的API端点允许用户请求和获取51school的数据（详细的API文档将在后续版本中提供）。

## 警告

**请注意**，该项目仅为概念演示和技术研究目的而设计，任何恶意使用都可能对51school平台和其他用户造成危害。请勿滥用此工具，确保遵守平台的使用协议与道德规范。

### 切勿将本项目用于任何非法或破坏性的活动。我们对因滥用本项目而导致的任何后果不承担责任。

## 贡献

如果您有兴趣参与该项目，欢迎提交Issue或Pull Request。

## 许可协议

该项目遵循[MIT许可证](LICENSE)。
```
MIT License

Copyright (c) 2025 景
```
---

**免责声明**：该项目与51school官方无关，所有与51school相关的名称和标志均为其版权所有。
