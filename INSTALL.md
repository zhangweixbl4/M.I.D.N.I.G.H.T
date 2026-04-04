# 安装 M.I.D.N.I.G.H.T

此文档介绍如何安装 M.I.D.N.I.G.H.T 项目

## 先决条件

- Python 3.12.10
- 《魔兽世界》正式服客户端
- Git

### 安装Python 3.12.10

- 检测：如果`python -V`提示已安装3.12以上版本，本环节跳过。
- 下载：`https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe`
- 安装：`python-3.12.10-amd64.exe /passive InstallAllUsers=0 PrependPath=1`

### 定位《魔兽世界》正式服客户端

- 检查注册表`HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Blizzard Entertainment\World of Warcraft` KEY为 InstallPath
- 路径应该是 `X:\Path_to_WOW\_retail_\`

### 安装Git

- 检测：如果`git --version`提示已安装任意版本，本环节跳过。
- 下载`https://github.com/git-for-windows/git/releases/download/v2.53.0.windows.2/Git-2.53.0.2-64-bit.exe`
- 安装


## 安装 M.I.D.N.I.G.H.T

### 从github克隆 M.I.D.N.I.G.H.T repo
- `git clone https://github.com/liantian-cn/M.I.D.N.I.G.H.T.git D:\MIDNIGHT`

### 安装Terminal组件的依赖

- `cd D:\MIDNIGHT\Terminal`
- `pip install -r requirements.txt`
- 验证，执行`python main.py`

### 复制DejaVu组件到游戏插件目录

- 安装：若《魔兽世界》正式服客户端的安装路径是`X:\Path_to_WOW\_retail_\`，则插件路径是`X:\Path_to_WOW\_retail_\Interface\AddOns\`。
- 验证：将D:\MIDNIGHT\DejaVu目录复制到插件路径后，检测`X:\Path_to_WOW\_retail_\Interface\AddOns\DejaVu\DejaVu.toc`文件是否存在。


## 升级

- 通过git更新M.I.D.N.I.G.H.T repo
- 重新复制DejaVu到插件目录，并覆盖旧文件。
