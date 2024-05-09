from argparse import ArgumentParser
from os import getcwd, getenv, listdir
from os.path import isabs, join, realpath
from re import search
from secrets import token_urlsafe

from flask import (
    Flask,
    abort,
    render_template,
    request,
    send_from_directory,
    session,
)

from files import get_current_path, get_files_data

DEFAULT_PATH = "./"
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"

# 创建项目以及初始化一些关键信息
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)
# 这里是预先将值存储在系统环境变量中了
app.secret_key = getenv("SECRET_KEY")
# 匹配移动端设备的正则表达式
MATCH_EXP = "Android|webOS|iPhone|iPad|iPod|BlackBerry"


def mobile_check() -> bool:
    """
    设备类型检查
    """
    try:
        return session.mobile  # type: ignore[reportAttributeAccessIssue, attr-defined]
    except AttributeError:
        if search(MATCH_EXP, request.headers.get("User-Agent", DEFAULT_UA)):
            session.mobile = True  # type: ignore[reportAttributeAccessIssue, attr-defined]
        else:
            session.mobile = False  # type: ignore[reportAttributeAccessIssue, attr-defined]
        return session.mobile  # type: ignore[reportAttributeAccessIssue, attr-defined]


def url_format(device_isMobile, default_load_url) -> str:
    """
    根据设备类型返回对应的资源 url
    """
    if device_isMobile:
        return "./h5/m_" + default_load_url
    else:
        return default_load_url


def url_random_arg():
    """
    url添加一个随机参数，防止浏览器缓存
    """
    return token_urlsafe(16)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    """
    共享文件主页
    """
    device_isMobile = mobile_check()
    if request.method == "GET":
        # GET 模式下，永远访问主页
        return render_template(
            url_format(device_isMobile, "index.html"),
            data={
                "files": get_files_data(DEFAULT_PATH),
                "currentPath": DEFAULT_PATH,
            },
            randomArg=url_random_arg(),
        )
    else:
        # POST 请求下获取传递的路径信息，并返回相应数据
        if request.form.get("pathText"):
            path_text = request.form.get("pathText")
            return render_template(
                url_format(device_isMobile, "index.html"),
                data={
                    "files": get_files_data(path_text),
                    "currentPath": get_current_path(),
                },
                randomArg=url_random_arg(),
            )
        else:
            abort(404)


@app.route("/download_file/<filename>")
def file_content(filename):
    """
    下载文件
    """
    # 若文件存在
    if filename in listdir(get_current_path()):
        # 发送文件 参数：路径，文件名
        return send_from_directory(get_current_path(), filename)
    else:
        # 否则返回错误页面
        device_isMobile = mobile_check()
        return render_template(
            url_format(device_isMobile, "download_error.html"),
            filename=filename,
            randomArg=url_random_arg(),
        )


def parse_args():
    parser = ArgumentParser("app.py")
    parser.add_argument("-d", "--directory", help="指定项目根目录")
    parser.add_argument(
        "-p",
        "--port",
        required=True,
        help="指定服务器端口",
        type=int,
    )
    args = parser.parse_args()
    global DEFAULT_PATH
    if isabs(args.directory):
        DEFAULT_PATH = realpath(args.directory)
    else:
        DEFAULT_PATH = realpath(join(getcwd(), args.directory or ""))  # noqa: F841
    return args.port


if __name__ == "__main__":
    # 监听在所有 IP 地址上
    p = parse_args()
    app.run(host="0.0.0.0", port=p, load_dotenv=True)
