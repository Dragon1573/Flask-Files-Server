# Flask 文件共享

## 简介

基于原生 JavaScript 前端和 Python Flask 后端的文件服务器。

## 功能

- [x] 目录浏览
- [x] 文件下载
- [x] HTML5 移动端适配

## 使用方法

### 获取项目

```shell
# HTTPS 仓库地址
git clone --progress https://github.com/Dragon1573/Flask-Files-Server.git
# SSH 仓库地址
git clone --progress git@github.com:Dragon1573/Flask-Files-Server.git

# 初始化虚拟环境
cd Flask-Files-Server/
python -m venv .venv

# 激活虚拟环境（Powershell）
& ./.venv/Scripts/Activate.ps1

# 安装必要的依赖项
python -m pip install -U flask
```

### 配置项目

在测试环境下，创建 `.env` 配置文件并添加如下内容，你应当使用「密码学安全的随机数生成器」（Cryptography-safety RNG）产生足够强度的服务器根密钥。

```dotenv
SECRET_KEY = "50me_raNdOM1y_9eneraTed_t0keN"
```

> [!CAUTION]
>
> 在生产环境下，你应当将其配置到环境变量中，而非使用 `.env` 文件提供临时环境变量！

### 帮助文档

```text
usage: app.py [-h] [-d DIRECTORY] -p PORT

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        指定项目根目录
  -p PORT, --port PORT  指定服务器端口
```

## 部署

本项目可借助 *CGI* （比如 [`wfastcgi`](https://pypi.org/project/wfastcgi/) 或 [`waitress`](https://pypi.org/project/waitress/) ）与常见的 Web 服务器进行集成，但更推荐使用 [`HttpPlatformHandler`](https://www.iis.net/downloads/microsoft/httpplatformhandler) 与 [Windows IIS](https://www.iis.net/) 集成。

> [!TIP]
>
> 你可以参考 [为 Python Web 应用配置 IIS](https://learn.microsoft.com/zh-cn/visualstudio/python/configure-web-apps-for-iis-windows?view=vs-2022) 。
