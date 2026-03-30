PLC 通用数据采集工具

概述

本工具是一款 工业级PLC数据采集程序，基于Python开发，支持西门子（S7系列）、三菱（FX/Q系列）、欧姆龙（FINS协议）三大主流品牌PLC，实现6种数据类型（bool、int、int64、float、double、string）的读写操作，具备自动重连、配置切换、后台运行等特性，专为开机自启式数据采集场景设计，开箱即用、稳定可靠。

核心特性

- 💡 多品牌支持：西门子（S7-200SMART/1200/1500/300/400）、三菱（FX3U/FX5U/Q/L/R）、欧姆龙（FINS协议）

- 📊 全类型读写：支持 bool（开关量）、int（16位整数）、int64（32位长整数）、float（单精度浮点）、double（双精度浮点，PLC通用4字节）、string（字符串，支持中文）

- 🔌 自动重连：PLC断开连接后，程序自动尝试重新连接，保障采集连续性

- ⚙️ 灵活配置：通过简单修改配置项，即可切换不同品牌PLC，无需修改核心代码

- 🖥️ 后台运行：支持无黑窗口启动，适配开机自启场景

- ✅ 开箱即用：完整封装，无需复杂开发，复制代码即可运行测试

环境准备

1. 运行环境

Python 3.7+（推荐3.9，兼容性最佳，避免过高版本导致依赖安装失败）

系统支持：Windows 7/10/11（适配工业现场常用系统，支持开机自启）

2. 依赖安装

打开终端（CMD/PowerShell），进入程序所在目录，执行以下命令安装依赖（一次性安装所有所需库）：

python -m pip install python-snap7 pymcprotocol omronfins

⚠️ 注意：

- 若使用虚拟环境（如.venv），需先激活虚拟环境，再执行上述命令

- 若安装失败，可尝试更换pip源（如阿里云源）：python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ python-snap7 pymcprotocol omronfins

- 欧姆龙依赖库为 omronfins（无横杠），请勿误安装 omron-fins（不存在该库）

文件说明

文件名

说明

plc_all_master.py

核心程序文件，包含三大PLC读写逻辑、自动重连、全类型支持

README.md

使用说明文档（本文档）

使用配置（核心步骤）

打开 plc_all_master.py，找到【PLC 选择配置】区域，仅需修改以下内容，无需改动其他代码：

# ======================== 【PLC 选择】只改这里 ========================
PLC_TYPE = "S7"            # 选择PLC品牌：S7=西门子 / Mitsubishi=三菱 / Omron=欧姆龙
# PLC_TYPE = "Mitsubishi"  # 注释不需要的PLC品牌
# PLC_TYPE = "Omron"

PLC_IP = "192.168.2.1"    # 你的PLC实际IP地址

# 西门子参数（仅PLC_TYPE="S7"时生效）
S7_RACK = 0                # 机架号（默认0）
S7_SLOT = 1                # 槽号：1200/1500=1，300=2，200SMART=0

# 三菱参数（仅PLC_TYPE="Mitsubishi"时生效）
MITS_PORT = 8000           # 端口：FX3U=8000，Q系列=5002
MITS_MODEL = "fx3u"        # PLC型号：fx3u/fx5u/q/l/r

# 欧姆龙参数（仅PLC_TYPE="Omron"时生效）
OMRON_PORT = 9600          # 端口（默认9600）
OMRON_NODE = 1             # FINS节点号（默认1）
# ======================================================================

配置说明（必看）

- PLC_TYPE：只能选择 "S7"、"Mitsubishi"、"Omron" 三者之一，不需要的品牌请用 # 注释

- PLC_IP：必须与PLC在同一网段（如PLC IP为192.168.2.100，电脑IP需为192.168.2.X），否则无法连接

- 槽号/端口/节点号：需与PLC实际配置一致，默认值适配大多数工业现场场景，若连接失败可核对PLC参数

使用方法

1. 基础运行（测试用）

1. 修改好配置项（PLC_TYPE、PLC_IP等）

2. 打开终端，进入程序所在目录，执行命令：python plc_all_master.py

3. 程序启动后，会自动连接PLC，并执行全类型读写测试，终端会输出测试结果（如BOOL值、整数、字符串等）

2. 开机自启（生产用）

实现电脑开机后，程序后台无窗口运行，自动采集PLC数据：

1. 将 plc_all_master.py 重命名为 plc_all_master.pyw（.pyw后缀可实现无黑窗口运行）

2. 按 Win + R，输入 shell:startup，打开开机启动文件夹

3. 右键桌面 → 新建 → 快捷方式，位置填写：pythonw.exe D:\你的程序路径\plc_all_master.pyw（替换为实际路径）

4. 将创建的快捷方式，拖入步骤2打开的开机启动文件夹，重启电脑即可自动运行

3. 自定义采集逻辑

修改程序中【测试：三大PLC全类型读写演示】区域，可自定义采集点位和频率：

# 示例：自定义采集西门子PLC点位
plc.write("M1.0", False, "bool")  # 写入M1.0为False
plc.write("DB1.DBW10", 5678, "int")  # 写入DB1.DBW10为5678
# 读取自定义点位
m1_0 = plc.read("M1.0", "bool")
db1_w10 = plc.read("DB1.DBW10", "int")
print("M1.0 =", m1_0)
print("DB1.DBW10 =", db1_w10)

# 调整采集频率（默认1秒1次）
time.sleep(0.5)  # 改为0.5秒采集1次

全类型读写示例（按品牌区分）

1. 西门子（S7）

# 写入
plc.write("M0.0", True, "bool")          # 位（开关量）
plc.write("DB1.DBW0", 1234, "int")      # 16位整数
plc.write("DB1.DBD4", 987654321, "int64")# 32位长整数
plc.write("DB1.DBD8", 33.99, "float")   # 浮点数
plc.write("DB1.DBD12", "你好Python", "string", 20)# 字符串（长度20）

# 读取
print(plc.read("M0.0", "bool"))          # 读取M0.0（bool）
print(plc.read("DB1.DBW0", "int"))       # 读取DB1.DBW0（int）
print(plc.read("DB1.DBD4", "int64"))     # 读取DB1.DBD4（int64）
print(plc.read("DB1.DBD8", "float"))     # 读取DB1.DBD8（float）
print(plc.read("DB1.DBD12", "string", 20))# 读取DB1.DBD12（string）

2. 三菱

# 写入
plc.write("M0", True, "bool")            # 位（开关量）
plc.write("D0", 1234, "int")            # 16位整数
plc.write("D2", 987654321, "int64")     # 32位长整数
plc.write("D4", 33.99, "float")         # 浮点数
plc.write("D10", "你好Python", "string", 20)# 字符串（长度20）

# 读取
print(plc.read("M0", "bool"))            # 读取M0（bool）
print(plc.read("D0", "int"))             # 读取D0（int）
print(plc.read("D2", "int64"))           # 读取D2（int64）
print(plc.read("D4", "float"))           # 读取D4（float）
print(plc.read("D10", "string", 20))     # 读取D10（string）

3. 欧姆龙

# 写入
plc.write("CIO0.00", True, "bool")       # 位（开关量）
plc.write("D0", 1234, "int")            # 16位整数
plc.write("D2", 987654321, "int64")     # 32位长整数
plc.write("D4", 33.99, "float")         # 浮点数
plc.write("D10", "你好Python", "string", 20)# 字符串（长度20）

# 读取
print(plc.read("CIO0.00", "bool"))       # 读取CIO0.00（bool）
print(plc.read("D0", "int"))             # 读取D0（int）
print(plc.read("D2", "int64"))           # 读取D2（int64）
print(plc.read("D4", "float"))           # 读取D4（float）
print(plc.read("D10", "string", 20))     # 读取D10（string）

常见问题与解决方案

错误现象

原因

解决方案

pip安装依赖时，提示“Could not find a version that satisfies the requirement omron-fins”

库名错误，不存在omron-fins，正确库名为omronfins

执行命令：python -m pip install omronfins

启动程序提示“连接失败：ConnectionRefusedError”

PLC IP错误、电脑与PLC不在同一网段、PLC未开启以太网通信

1. 核对PLC IP；2. 确保电脑与PLC网段一致；3. 检查PLC以太网配置

读取/写入失败，提示“connected = False”

PLC连接断开、配置参数错误（如槽号、端口）

1. 核对PLC配置参数；2. 重启PLC和程序；3. 关闭电脑防火墙

字符串读取乱码

编码格式不匹配，程序默认使用gbk编码

将代码中“gbk”改为“utf-8”（需与PLC字符串编码一致）

开机自启失败

快捷方式路径错误、未修改为.pyw后缀

1. 确认快捷方式中pythonw.exe和程序路径正确；2. 确保程序后缀为.pyw

注意事项

- 运行程序前，需关闭电脑防火墙（或允许Python程序通过防火墙），否则会拦截PLC连接

- PLC需开启对应通信协议：西门子开启S7协议、三菱开启MC协议、欧姆龙开启FINS协议

- 采集频率不宜过高（建议0.1-10秒/次），避免占用过多PLC和电脑资源

- 若需长期运行，建议定期检查程序运行状态，可添加日志保存功能（可联系作者添加）

- 字符串读写时，需指定长度（默认10），长度需大于等于实际字符串长度，避免截断

扩展功能（可定制）

若需要以下功能，可联系作者定制：

- 数据保存：将采集到的数据保存到CSV/Excel文件

- 数据库上传：将数据上传到SQLite/MySQL/PostgreSQL数据库

- 异常告警：PLC连接失败、数据异常时，触发弹窗/声音告警

- 多点位批量采集：配置采集点位列表，批量读写多个点位

- 数据可视化：简单界面展示采集数据、连接状态
