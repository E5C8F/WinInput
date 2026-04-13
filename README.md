# WinInput

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)

轻量级 Windows 输入模拟库，基于 ctypes 封装 Windows API，无需编译，零依赖。

## ✨ 特性

- 🎯 **三种输入模式**：SendInput（硬件级）、PostMessage（异步）、SendMessage（同步）
- 🖱️ **完整鼠标支持**：移动、点击、滚轮、X 键（前进/后退）
- ⌨️ **完整键盘支持**：按键、组合键、Unicode 输入
- 📺 **高 DPI 适配**：内置 DPI 感知设置，多显示器兼容
- 🔧 **轻量简洁**：纯 Python + ctypes，开箱即用

## 📦 安装

### 从 GitHub 安装

```bash
pip install git+https://github.com/E5C8F/wininput.git
```

### 手动安装

下载 `wininput.py` 文件，放置到你的项目目录中即可。

```python
import wininput
```

## 🚀 快速开始

```python
import wininput

# 初始化 DPI 感知（高 DPI 显示器必需）
wininput.SetDPIAware(2)

# 获取鼠标位置
x, y = wininput.mousepos()
print(f"鼠标位置: ({x}, {y})")

# 移动并点击
wininput.mouse_move_Input(500, 300)
wininput.mouse_leftdown_Input()
wininput.mouse_leftup_Input()

# 输入文本
wininput.string_Input("Hello World!")

# 按下回车
wininput.keydown_Input(wininput.keycode.VK_RETURN)
wininput.keyup_Input(wininput.keycode.VK_RETURN)
```

## 📖 核心概念

本库提供三种不同层次的输入模拟方式：

| 方式 | 函数后缀 | 原理 | 焦点要求 | 适用场景 |
|------|----------|------|----------|----------|
| **SendInput** | `_Input` | 硬件级注入 | ✅ 需要 | 前台自动化，效果最真实 |
| **PostMessage** | `_Post` | 异步消息 | ❌ 不需要 | 后台发送，立即返回 |
| **SendMessage** | `_Send` | 同步消息 | ❌ 不需要 | 后台发送，等待处理结果 |

**选择建议：**
- 操作前台窗口 → 使用 `_Input` 系列
- 向后台窗口发消息 → 使用 `_Post` 或 `_Send` 系列

## 📚 API 文档

### 初始化

#### `SetDPIAware(level: int = 2) -> int`

设置进程 DPI 感知级别。

| 参数 | 类型 | 说明 |
|------|------|------|
| `level` | `int` | `0`=不感知，`1`=系统DPI感知，`2`=每监视器DPI感知（推荐） |

```python
wininput.SetDPIAware(2)  # 程序启动时调用
```

#### `mousepos() -> tuple[int, int]`

获取当前鼠标屏幕绝对坐标。

```python
x, y = wininput.mousepos()
```

---

### ⌨️ 键盘操作

所有键盘函数均支持以下 `keycode` 参数类型：
- `int`：虚拟键码，如 `wininput.keycode.VK_A`
- `str`：单个字符，如 `'A'`（自动转为大写）
- `list`：多个键码，用于组合键

#### 按键操作

| 函数 | 说明 |
|------|------|
| `keydown_Input(keycode)` | 按下按键（SendInput） |
| `keyup_Input(keycode)` | 释放按键（SendInput） |
| `keydown_Post(keycode, hWnd=None)` | 按下按键（PostMessage） |
| `keyup_Post(keycode, hWnd=None)` | 释放按键（PostMessage） |
| `keydown_Send(keycode, hWnd=None)` | 按下按键（SendMessage） |
| `keyup_Send(keycode, hWnd=None)` | 释放按键（SendMessage） |

```python
# 单个按键
wininput.keydown_Input('A')
wininput.keyup_Input('A')

# 组合键（Ctrl+C）
wininput.keydown_Input([wininput.keycode.VK_CONTROL, wininput.keycode.VK_C])
wininput.keyup_Input([wininput.keycode.VK_C, wininput.keycode.VK_CONTROL])

# 发送到指定窗口
hwnd = 0x12345
wininput.keydown_Post(wininput.keycode.VK_ENTER, hwnd)
```

#### 字符串输入

| 函数 | 说明 |
|------|------|
| `string_Input(text: str)` | 输入字符串（SendInput） |
| `string_Post(text: str, hWnd=None)` | 输入字符串（PostMessage） |
| `string_Send(text: str, hWnd=None)` | 输入字符串（SendMessage） |

```python
wininput.string_Input("Hello 世界!")      # 前台输入
wininput.string_Post("Hello!", hwnd)      # 后台发送
```

---

### 🖱️ 鼠标操作

#### 鼠标移动

| 函数 | 说明 |
|------|------|
| `mouse_move_Input(x, y, absmove=True)` | 移动鼠标（SendInput） |
| `mouse_move_Post(x, y, hWnd=None)` | 移动鼠标（PostMessage） |
| `mouse_move_Send(x, y, hWnd=None)` | 移动鼠标（SendMessage） |

```python
# 绝对坐标移动
wininput.mouse_move_Input(500, 300)

# 相对坐标移动（偏移量）
wininput.mouse_move_Input(100, 0, absmove=False)  # 向右 100 像素
```

#### 鼠标按键

所有按键函数均有 `Input`、`Post`、`Send` 三个版本。

| 操作 | Input 版 | Post 版 | Send 版 |
|------|----------|---------|---------|
| 左键按下 | `mouse_leftdown_Input` | `mouse_leftdown_Post` | `mouse_leftdown_Send` |
| 左键释放 | `mouse_leftup_Input` | `mouse_leftup_Post` | `mouse_leftup_Send` |
| 右键按下 | `mouse_rightdown_Input` | `mouse_rightdown_Post` | `mouse_rightdown_Send` |
| 右键释放 | `mouse_rightup_Input` | `mouse_rightup_Post` | `mouse_rightup_Send` |
| 中键按下 | `mouse_middledown_Input` | `mouse_middledown_Post` | `mouse_middledown_Send` |
| 中键释放 | `mouse_middleup_Input` | `mouse_middleup_Post` | `mouse_middleup_Send` |

**Input 版参数：**
- `x, y`：坐标（均为 `None` 时不移动）
- `absmove`：是否绝对坐标，默认 `True`

**Post/Send 版参数：**
- `x, y`：窗口客户区坐标
- `hWnd`：目标窗口句柄，默认当前焦点窗口

```python
# 在当前位置点击
wininput.mouse_leftdown_Input()
wininput.mouse_leftup_Input()

# 在指定位置点击
wininput.mouse_rightdown_Input(200, 200)
wininput.mouse_rightup_Input(200, 200)

# 发送到指定窗口
wininput.mouse_leftdown_Post(100, 100, hwnd)
```

#### 鼠标滚轮

| 函数 | 说明 |
|------|------|
| `mouse_wheel_Input(delta, x=None, y=None, absmove=True)` | 垂直滚轮 |
| `mouse_hwheel_Input(delta, x=None, y=None, absmove=True)` | 水平滚轮 |
| `mouse_wheel_Post(delta, x, y, hWnd=None)` | 垂直滚轮（PostMessage） |
| `mouse_wheel_Send(delta, x, y, hWnd=None)` | 垂直滚轮（SendMessage） |
| `mouse_hwheel_Post(delta, x, y, hWnd=None)` | 水平滚轮（PostMessage） |
| `mouse_hwheel_Send(delta, x, y, hWnd=None)` | 水平滚轮（SendMessage） |

`delta` 单位为 `WHEEL_DELTA`(120)：
- 垂直滚轮：正值向上，负值向下
- 水平滚轮：正值向右，负值向左

```python
# 垂直滚轮
wininput.mouse_wheel_Input(120)   # 向上滚动一格
wininput.mouse_wheel_Input(-120)  # 向下滚动一格

# 水平滚轮（需要鼠标支持）
wininput.mouse_hwheel_Input(120)  # 向右滚动
```

#### X 键（浏览器前进/后退）

| 操作 | Input 版 | Post 版 | Send 版 |
|------|----------|---------|---------|
| X1（后退）按下 | `mouse_x1down_Input` | `mouse_x1down_Post` | `mouse_x1down_Send` |
| X1（后退）释放 | `mouse_x1up_Input` | `mouse_x1up_Post` | `mouse_x1up_Send` |
| X2（前进）按下 | `mouse_x2down_Input` | `mouse_x2down_Post` | `mouse_x2down_Send` |
| X2（前进）释放 | `mouse_x2up_Input` | `mouse_x2up_Post` | `mouse_x2up_Send` |

```python
# 浏览器后退
wininput.mouse_x1down_Input()
wininput.mouse_x1up_Input()
```

---

### 🔧 工具函数

#### `GetSystemMetrics(nIndex: int) -> int`

获取系统设置或环境变量的值。

```python
SM_CXSCREEN = 0   # 主显示器宽度
SM_CYSCREEN = 1   # 主显示器高度

width = wininput.GetSystemMetrics(SM_CXSCREEN)
height = wininput.GetSystemMetrics(SM_CYSCREEN)
print(f"屏幕尺寸: {width} x {height}")
```

#### 坐标转换

| 函数 | 说明 |
|------|------|
| `ClientToScreen(hWnd, x, y)` | 窗口坐标 → 屏幕坐标 |
| `ScreenToClient(hWnd, x, y)` | 屏幕坐标 → 窗口坐标 |

```python
# 屏幕坐标转窗口坐标
client_x, client_y = wininput.ScreenToClient(hwnd, 500, 300)

# 窗口坐标转屏幕坐标
screen_x, screen_y = wininput.ClientToScreen(hwnd, 100, 100)
```

---

## ⚡ 高级技巧

> 以下函数封装程度较低，直接映射 Windows API，使用难度较高但灵活性更大。适合需要精细控制的场景。

### `mouse_Input(dx, dy, mouseData, dwFlags, time, dwExtraInfo)`

直接调用 `SendInput` 模拟鼠标事件。

| 参数 | 类型 | 说明 |
|------|------|------|
| `dx, dy` | `int` | 坐标/偏移量 |
| `mouseData` | `int` | 滚轮数据或 X 按钮标识 |
| `dwFlags` | `int` | 事件标志位组合 |
| `time` | `int` | 时间戳，`0` 为系统自动 |
| `dwExtraInfo` | `int` | 附加信息，通常为 `0` |

```python
# 绝对坐标移动到 (500, 300) 并左键按下
flags = (wininput.MOUSEINPUT.MOUSEEVENTF_MOVE |
         wininput.MOUSEINPUT.MOUSEEVENTF_ABSOLUTE |
         wininput.MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK |
         wininput.MOUSEINPUT.MOUSEEVENTF_LEFTDOWN)

# 坐标需要映射到 0~65535 范围
wininput.mouse_Input(dx, dy, 0, flags, 0, 0)
```

### `key_Input(wVk, wScan, dwFlags, time, dwExtraInfo)`

直接调用 `SendInput` 模拟键盘事件。

| 参数 | 类型 | 说明 |
|------|------|------|
| `wVk` | `int` | 虚拟键码 |
| `wScan` | `int` | 扫描码 |
| `dwFlags` | `int` | 事件标志位组合 |
| `time` | `int` | 时间戳，`0` 为系统自动 |
| `dwExtraInfo` | `int` | 附加信息，通常为 `0` |

```python
# Unicode 字符输入
flags = wininput.KEYBDINPUT.KEYEVENTF_UNICODE
wininput.key_Input(0, ord('中'), flags, 0, 0)          # 按下
wininput.key_Input(0, ord('中'), flags | 0x0002, 0, 0) # 释放
```

### `PostMessage(hWnd, msg, wParam, lParam)` / `SendMessage(hWnd, msg, wParam, lParam)`

直接向目标窗口发送消息。

```python
hWnd = wininput.user32.GetForegroundWindow()
scan_code = wininput.user32.MapVirtualKeyW(wininput.keycode.VK_A, 0)
lParam = (scan_code << 16) | 1

wininput.PostMessage(hWnd, wininput.keymsg.WM_KEYDOWN, wininput.keycode.VK_A, lParam)
```
### `SendInput(cInputs, pInputs, cbSize)`
用SendInput模拟硬件级输入事件到系统，注入系统底层输入队列，效果最接近真实硬件输入。
参数:
    cInputs (int): 输入事件数。
    pInputs (POINTER(INPUT)): 输入事件结构体(INPUT)组成的列表(C语言数组)。
    cbSize (int): 输入事件结构体大小，默认为sizeof(INPUT)。
---

## 💡 使用示例

### 示例 1：自动填写表单

```python
import wininput
import time

wininput.SetDPIAware(2)

# 等待用户切换到目标窗口
time.sleep(3)

# 输入用户名
wininput.string_Input("username")
wininput.keydown_Input(wininput.keycode.VK_TAB)
wininput.keyup_Input(wininput.keycode.VK_TAB)

# 输入密码
wininput.string_Input("password123")
wininput.keydown_Input(wininput.keycode.VK_RETURN)
wininput.keyup_Input(wininput.keycode.VK_RETURN)
```

### 示例 2：自动连点器

```python
import wininput
import time

def auto_clicker(interval: float = 0.1):
    """按 Ctrl+F8 开始，Ctrl+F9 停止"""
    import keyboard
    
    clicking = False
    print("Ctrl+F8: 开始, Ctrl+F9: 停止, Esc: 退出")
    
    while True:
        if keyboard.is_pressed('ctrl+f8'):
            clicking = True
            print("开始连点")
        elif keyboard.is_pressed('ctrl+f9'):
            clicking = False
            print("停止连点")
        elif keyboard.is_pressed('esc'):
            break
            
        if clicking:
            wininput.mouse_leftdown_Input()
            wininput.mouse_leftup_Input()
            time.sleep(interval)
```

### 示例 3：向后台窗口发送文本

```python
import wininput

# 获取目标窗口句柄（以记事本为例）
hwnd = wininput.user32.FindWindowW(None, "无标题 - 记事本")

if hwnd:
    wininput.string_Post("Hello from background!", hwnd)
else:
    print("未找到目标窗口")
```

---

## 📋 常量参考

### 常用虚拟键码

| 常量 | 值 | 按键 |
|------|-----|------|
| `VK_A` ~ `VK_Z` | `0x41`~`0x5A` | A~Z |
| `VK_0` ~ `VK_9` | `0x30`~`0x39` | 0~9 |
| `VK_F1` ~ `VK_F12` | `0x70`~`0x7B` | F1~F12 |
| `VK_RETURN` | `0x0D` | 回车 |
| `VK_SPACE` | `0x20` | 空格 |
| `VK_TAB` | `0x09` | Tab |
| `VK_ESCAPE` | `0x1B` | ESC |
| `VK_BACK` | `0x08` | 退格 |
| `VK_SHIFT` | `0x10` | Shift |
| `VK_CONTROL` | `0x11` | Ctrl |
| `VK_MENU` | `0x12` | Alt |
| `VK_LWIN` | `0x5B` | 左 Win |
| `VK_RWIN` | `0x5C` | 右 Win |
| `VK_LEFT` | `0x25` | 左箭头 |
| `VK_UP` | `0x26` | 上箭头 |
| `VK_RIGHT` | `0x27` | 右箭头 |
| `VK_DOWN` | `0x28` | 下箭头 |
| `VK_DELETE` | `0x2E` | Delete |
| `VK_INSERT` | `0x2D` | Insert |
| `VK_HOME` | `0x24` | Home |
| `VK_END` | `0x23` | End |
| `VK_PRIOR` | `0x21` | Page Up |
| `VK_NEXT` | `0x22` | Page Down |

### 鼠标消息常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `WM_MOUSEMOVE` | `0x0200` | 鼠标移动 |
| `WM_LBUTTONDOWN` | `0x0201` | 左键按下 |
| `WM_LBUTTONUP` | `0x0202` | 左键释放 |
| `WM_RBUTTONDOWN` | `0x0204` | 右键按下 |
| `WM_RBUTTONUP` | `0x0205` | 右键释放 |
| `WM_MBUTTONDOWN` | `0x0207` | 中键按下 |
| `WM_MBUTTONUP` | `0x0208` | 中键释放 |
| `WM_MOUSEWHEEL` | `0x020A` | 垂直滚轮 |
| `WM_MOUSEHWHEEL` | `0x020E` | 水平滚轮 |
| `WM_XBUTTONDOWN` | `0x020B` | X 键按下 |
| `WM_XBUTTONUP` | `0x020C` | X 键释放 |

### 键盘消息常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `WM_KEYDOWN` | `0x0100` | 按键按下 |
| `WM_KEYUP` | `0x0101` | 按键释放 |
| `WM_CHAR` | `0x0102` | 字符输入 |
| `WM_SYSKEYDOWN` | `0x0104` | 系统键按下 |
| `WM_SYSKEYUP` | `0x0105` | 系统键释放 |

---

## ⚠️ 注意事项

### DPI 感知

高 DPI 显示器（如 4K 屏幕）上，务必在程序启动时调用：

```python
wininput.SetDPIAware(2)
```

否则坐标可能缩放错误。

### UIPI 限制

Windows Vista 及以上版本，低权限进程无法向高权限窗口发送输入。

**解决方案：**
- 以管理员权限运行程序
- 或为目标程序添加 UIAccess 清单

### 鼠标加速度

`SendInput` 相对移动受系统"提高指针精确度"设置影响，实际移动距离可能被加倍。如需精确控制，请使用绝对坐标模式：

```python
wininput.mouse_move_Input(x, y, absmove=True)
```

### PostMessage/SendMessage 的局限性

- 部分窗口可能拦截或丢弃消息
- `keydown_Send` 不会自动生成 `WM_CHAR` 消息，字符串输入请使用 `string_Send`

---
