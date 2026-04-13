import ctypes
from ctypes import wintypes
from typing import Literal
user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
shcore = ctypes.WinDLL('shcore', use_last_error=True)
def errcheck (result, func, args):
    错误码 = ctypes.set_last_error(0)
    if 错误码:
        raise ctypes.WinError(错误码, fr'result: {result}, func: {func}, args: {args}')
    return result
SetProcessDpiAwareness = shcore.SetProcessDpiAwareness
'''
SetProcessDpiAwareness函数用于设置进程的DPI感知级别。
参数:
    PROCESS_DPI_AWARENESS (int): DPI感知级别. 
        值:
            0: 不感知(DPI unaware). 
            1: 系统DPI感知(System DPI aware). 
            2: 每监视器DPI感知(Per-Monitor DPI aware). 
返回:
    ctypes.c_long: 0(S_OK)表示成功, 负值表示失败. 
注意:
    - Windows 8.1+支持此API, 更早版本需使用SetProcessDPIAware. 
    - 每监视器DPI感知(2)可正确处理多显示器不同DPI的情况. 
            '''
SetProcessDpiAwareness.argtypes = [
    ctypes.c_int
]
SetProcessDpiAwareness.restype = ctypes.c_long
SetProcessDpiAwareness.errcheck = errcheck
def SetDPIAware(PROCESS_DPI_AWARENESS: int = 2) -> ctypes.c_long:
    '''
    设置进程DPI感知级别. 
    
    参数:
        PROCESS_DPI_AWARENESS (int): DPI感知级别. 
            0: 不感知(DPI unaware). 
            1: 系统DPI感知(System DPI aware). 
            2: 每监视器DPI感知(Per-Monitor DPI aware). 
    
    返回:
        ctypes.c_long: 0(S_OK)表示成功, 负值表示失败. 
    
    注意:
        - 建议程序启动时调用并设置为2, 否则高DPI显示器坐标可能错误. 
        - Windows 8.1+支持此API, 更早版本需使用SetProcessDPIAware. 
        - 每监视器DPI感知(2)可正确处理多显示器不同DPI的情况. 
    '''
    return SetProcessDpiAwareness(PROCESS_DPI_AWARENESS)


GetCursorPos = user32.GetCursorPos
'''
获取鼠标光标位置. 
参数:
    lpPoint: 指向POINT结构的指针, 用于接收光标位置. 
返回:
    若函数成功, 则返回非零值, 否则返回零值. 
注意:
    - 建议先调用SetDPIAware(), 否则高DPI下坐标可能缩放错误. 
'''
GetCursorPos.argtypes = [
    ctypes.POINTER(wintypes.POINT)
]
GetCursorPos.restype = wintypes.BOOL
GetCursorPos.errcheck = errcheck

def mousepos() -> tuple[int, int]:
    '''
    获取鼠标光标位置. 
    
    返回:
        tuple[int, int]: 鼠标坐标(x, y), 屏幕绝对坐标. 
    
    注意:
        - 返回屏幕绝对坐标, 非窗口相对坐标. 
        - 建议先调用SetDPIAware(), 否则高DPI下坐标可能缩放错误. 
    参考:
        - https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getcursorpos
    '''
    POINT = wintypes.POINT()
    返回值 = GetCursorPos(ctypes.byref(POINT))
    return (POINT.x, POINT.y)


class keymsg:
    '''
    键盘消息代码常量类
    
    包含Windows系统中与键盘相关的消息代码常量，用于窗口消息处理。
    这些常量对应于Windows API中的WM_*消息。
    
    常量:
        WM_ACTIVATE: 窗口激活或失活
        WM_APPCOMMAND: 应用程序命令（如多媒体键）
        WM_CHAR: 字符输入（来自WM_KEYDOWN转换）
        WM_DEADCHAR: 死键按下（如 ´`^ 等组合键）
        WM_HOTKEY: 热键被按下
        WM_KEYDOWN: 普通键按下
        WM_KEYUP: 普通键释放
        WM_KILLFOCUS: 窗口失去焦点
        WM_SETFOCUS: 窗口获得焦点
        WM_SYSDEADCHAR: 系统死键按下（Alt+死键）
        WM_SYSKEYDOWN: 系统键按下（如Alt）
        WM_SYSKEYUP: 系统键释放
        WM_UNICHAR: Unicode字符输入（需处理）
    '''
    WM_ACTIVATE = 0x0006       # 窗口激活或失活
    WM_APPCOMMAND = 0x0319     # 应用程序命令（如多媒体键）
    WM_CHAR = 0x0102           # 字符输入（来自WM_KEYDOWN转换）
    WM_DEADCHAR = 0x0103       # 死键按下（如 ´`^ 等组合键）
    WM_HOTKEY = 0x0312         # 热键被按下
    WM_KEYDOWN = 0x0100        # 普通键按下
    WM_KEYUP = 0x0101          # 普通键释放
    WM_KILLFOCUS = 0x0008      # 窗口失去焦点
    WM_SETFOCUS = 0x0007       # 窗口获得焦点
    WM_SYSDEADCHAR = 0x0107    # 系统死键按下（Alt+死键）
    WM_SYSKEYDOWN = 0x0104     # 系统键按下（如Alt）
    WM_SYSKEYUP = 0x0105       # 系统键释放
    WM_UNICHAR = 0x0109        # Unicode字符输入（需处理）
class mousemsg:
    '''
    鼠标消息代码常量类
    
    包含Windows系统中与鼠标相关的消息代码常量，用于窗口消息处理。
    这些常量对应于Windows API中的WM_*消息。
    
    常量:
        WM_CAPTURECHANGED: 鼠标捕获更改
        WM_LBUTTONDBLCLK: 鼠标左键双击
        WM_LBUTTONDOWN: 鼠标左键按下
        WM_LBUTTONUP: 鼠标左键释放
        WM_MBUTTONDBLCLK: 鼠标中键双击
        WM_MBUTTONDOWN: 鼠标中键按下
        WM_MBUTTONUP: 鼠标中键释放
        WM_MOUSEACTIVATE: 鼠标激活窗口
        WM_MOUSEHOVER: 鼠标悬停
        WM_MOUSEHWHEEL: 鼠标水平滚轮
        WM_MOUSELEAVE: 鼠标离开
        WM_MOUSEMOVE: 鼠标移动
        WM_MOUSEWHEEL: 鼠标垂直滚轮
        WM_NCHITTEST: 非客户区命中测试（判断鼠标在窗口哪个区域）
        WM_NCLBUTTONDBLCLK: 非客户区左键双击
        WM_NCLBUTTONDOWN: 非客户区左键按下
        WM_NCLBUTTONUP: 非客户区左键释放
        WM_NCMBUTTONDBLCLK: 非客户区中键双击
        WM_NCMBUTTONDOWN: 非客户区中键按下
        WM_NCMBUTTONUP: 非客户区中键释放
        WM_NCMOUSEHOVER: 非客户区鼠标悬停
        WM_NCMOUSELEAVE: 非客户区鼠标离开
        WM_NCMOUSEMOVE: 非客户区鼠标移动
        WM_NCRBUTTONDBLCLK: 非客户区右键双击
        WM_NCRBUTTONDOWN: 非客户区右键按下
        WM_NCRBUTTONUP: 非客户区右键释放
        WM_NCXBUTTONDBLCLK: 非客户区X键双击
        WM_NCXBUTTONDOWN: 非客户区X键按下
        WM_NCXBUTTONUP: 非客户区X键释放
        WM_RBUTTONDBLCLK: 鼠标右键双击
        WM_RBUTTONDOWN: 鼠标右键按下
        WM_RBUTTONUP: 鼠标右键释放
        WM_XBUTTONDBLCLK: X键双击（前进/后退键）
        WM_XBUTTONDOWN: X键按下
        WM_XBUTTONUP: X键释放
    '''
    WM_CAPTURECHANGED = 0x0215     # 鼠标捕获更改
    WM_LBUTTONDBLCLK = 0x0203      # 鼠标左键双击
    WM_LBUTTONDOWN = 0x0201        # 鼠标左键按下
    WM_LBUTTONUP = 0x0202          # 鼠标左键释放
    WM_MBUTTONDBLCLK = 0x0209      # 鼠标中键双击
    WM_MBUTTONDOWN = 0x0207        # 鼠标中键按下
    WM_MBUTTONUP = 0x0208          # 鼠标中键释放
    WM_MOUSEACTIVATE = 0x0021      # 鼠标激活窗口
    WM_MOUSEHOVER = 0x02A1         # 鼠标悬停
    WM_MOUSEHWHEEL = 0x020E        # 鼠标水平滚轮
    WM_MOUSELEAVE = 0x02A3         # 鼠标离开
    WM_MOUSEMOVE = 0x0200          # 鼠标移动
    WM_MOUSEWHEEL = 0x020A         # 鼠标垂直滚轮
    WM_NCHITTEST = 0x0084          # 非客户区命中测试（判断鼠标在窗口哪个区域）
    WM_NCLBUTTONDBLCLK = 0x00A3    # 非客户区左键双击
    WM_NCLBUTTONDOWN = 0x00A1      # 非客户区左键按下
    WM_NCLBUTTONUP = 0x00A2        # 非客户区左键释放
    WM_NCMBUTTONDBLCLK = 0x00A9    # 非客户区中键双击
    WM_NCMBUTTONDOWN = 0x00A7      # 非客户区中键按下
    WM_NCMBUTTONUP = 0x00A8        # 非客户区中键释放
    WM_NCMOUSEHOVER = 0x02A0       # 非客户区鼠标悬停
    WM_NCMOUSELEAVE = 0x02A2       # 非客户区鼠标离开
    WM_NCMOUSEMOVE = 0x00A0        # 非客户区鼠标移动
    WM_NCRBUTTONDBLCLK = 0x00A6    # 非客户区右键双击
    WM_NCRBUTTONDOWN = 0x00A4      # 非客户区右键按下
    WM_NCRBUTTONUP = 0x00A5        # 非客户区右键释放
    WM_NCXBUTTONDBLCLK = 0x00AD    # 非客户区X键双击
    WM_NCXBUTTONDOWN = 0x00AB      # 非客户区X键按下
    WM_NCXBUTTONUP = 0x00AC        # 非客户区X键释放
    WM_RBUTTONDBLCLK = 0x0206      # 鼠标右键双击
    WM_RBUTTONDOWN = 0x0204        # 鼠标右键按下
    WM_RBUTTONUP = 0x0205          # 鼠标右键释放
    WM_XBUTTONDBLCLK = 0x020D      # X键双击（前进/后退键）
    WM_XBUTTONDOWN = 0x020B        # X键按下
    WM_XBUTTONUP = 0x020C          # X键释放
class keycode:
    '''
    键盘虚拟键码常量类
    
    包含Windows系统中与键盘相关的虚拟键码常量，用于窗口消息处理。
    这些常量对应于Windows API中的VK_*消息。
    
    常量:
        VK_LBUTTON: 鼠标左键
        VK_RBUTTON: 鼠标右键
        VK_CANCEL: 取消键（Ctrl+Break）
        VK_MBUTTON: 鼠标中键
        VK_XBUTTON1: X1鼠标按钮（后退）
        VK_XBUTTON2: X2鼠标按钮（前进）
        VK_BACK: 退格键
        VK_TAB: 制表键
        VK_CLEAR: 清除键（数字键盘5，NumLock关闭时）
        VK_RETURN: 回车键
        VK_SHIFT: Shift键（通用，不分左右）
        VK_CONTROL: Ctrl键（通用，不分左右）
        VK_MENU: Alt键（通用，不分左右）
        VK_PAUSE: 暂停键
        VK_CAPITAL: 大写锁定键
        VK_KANA: 日语假名键（同VK_HANGUL）
        VK_HANGUL: 韩语输入键（同VK_KANA）
        VK_IME_ON: 打开输入法
        VK_JUNJA: 日语输入模式切换
        VK_FINAL: 最终输入键
        VK_HANJA: 韩语汉字转换键（同VK_KANJI）
        VK_KANJI: 日语汉字输入键（同VK_HANJA）
        VK_IME_OFF: 关闭输入法
        VK_ESCAPE: 转义键（ESC）
        VK_CONVERT: 日语输入法转换键
        VK_NONCONVERT: 日语输入法非转换键
        VK_ACCEPT: 接受键（IME接受）
        VK_MODECHANGE: 模式切换键
        VK_SPACE: 空格键
        VK_PRIOR: 页上键（Page Up）
        VK_NEXT: 页下键（Page Down）
        VK_END: 结束键
        VK_HOME: 首页键
        VK_LEFT: 左箭头键
        VK_UP: 上箭头键
        VK_RIGHT: 右箭头键
        VK_DOWN: 下箭头键
        VK_SELECT: 选择键
        VK_PRINT: 打印键
        VK_EXECUTE: 执行键
        VK_SNAPSHOT: 截屏键（Print Screen）
        VK_INSERT: 插入键
        VK_DELETE: 删除键
        VK_HELP: 帮助键
        VK_0: 0键（主键盘区）
        VK_1: 1键（主键盘区）
        VK_2: 2键（主键盘区）
        VK_3: 3键（主键盘区）
        VK_4: 4键（主键盘区）
        VK_5: 5键（主键盘区）
        VK_6: 6键（主键盘区）
        VK_7: 7键（主键盘区）
        VK_8: 8键（主键盘区）
        VK_9: 9键（主键盘区）
        VK_A: A键
        VK_B: B键
        VK_C: C键
        VK_D: D键
        VK_E: E键
        VK_F: F键
        VK_G: G键
        VK_H: H键
        VK_I: I键
        VK_J: J键
        VK_K: K键
        VK_L: L键
        VK_M: M键
        VK_N: N键
        VK_O: O键
        VK_P: P键
        VK_Q: Q键
        VK_R: R键
        VK_S: S键
        VK_T: T键
        VK_U: U键
        VK_V: V键
        VK_W: W键
        VK_X: X键
        VK_Y: Y键
        VK_Z: Z键
        VK_LWIN: 左Windows键
        VK_RWIN: 右Windows键
        VK_APPS: 应用程序键（右键菜单）
        VK_SLEEP: 睡眠键
        VK_NUMPAD0: 数字键盘0
        VK_NUMPAD1: 数字键盘1
        VK_NUMPAD2: 数字键盘2
        VK_NUMPAD3: 数字键盘3
        VK_NUMPAD4: 数字键盘4
        VK_NUMPAD5: 数字键盘5
        VK_NUMPAD6: 数字键盘6
        VK_NUMPAD7: 数字键盘7
        VK_NUMPAD8: 数字键盘8
        VK_NUMPAD9: 数字键盘9
        VK_MULTIPLY: 乘号键（数字键盘*）
        VK_ADD: 加号键（数字键盘+）
        VK_SEPARATOR: 分隔符键
        VK_SUBTRACT: 减号键（数字键盘-）
        VK_DECIMAL: 小数点键（数字键盘.）
        VK_DIVIDE: 除号键（数字键盘/）
        VK_F1: F1键
        VK_F2: F2键
        VK_F3: F3键
        VK_F4: F4键
        VK_F5: F5键
        VK_F6: F6键
        VK_F7: F7键
        VK_F8: F8键
        VK_F9: F9键
        VK_F10: F10键
        VK_F11: F11键
        VK_F12: F12键
        VK_F13: F13键
        VK_F14: F14键
        VK_F15: F15键
        VK_F16: F16键
        VK_F17: F17键
        VK_F18: F18键
        VK_F19: F19键
        VK_F20: F20键
        VK_F21: F21键
        VK_F22: F22键
        VK_F23: F23键
        VK_F24: F24键
        VK_NUMLOCK: 数字锁定键
        VK_SCROLL: 滚动锁定键
        VK_LSHIFT: 左Shift键
        VK_RSHIFT: 右Shift键
        VK_LCONTROL: 左Ctrl键
        VK_RCONTROL: 右Ctrl键
        VK_LMENU: 左Alt键
        VK_RMENU: 右Alt键
        VK_BROWSER_BACK: 浏览器后退键
        VK_BROWSER_FORWARD: 浏览器前进键
        VK_BROWSER_REFRESH: 浏览器刷新键
        VK_BROWSER_STOP: 浏览器停止键
        VK_BROWSER_SEARCH: 浏览器搜索键
        VK_BROWSER_FAVORITES: 浏览器收藏夹键
        VK_BROWSER_HOME: 浏览器主页键
        VK_VOLUME_MUTE: 静音键
        VK_VOLUME_DOWN: 音量减键
        VK_VOLUME_UP: 音量增键
        VK_MEDIA_NEXT_TRACK: 媒体下一首键
        VK_MEDIA_PREV_TRACK: 媒体上一首键
        VK_MEDIA_STOP: 媒体停止键
        VK_MEDIA_PLAY_PAUSE: 媒体播放/暂停键
        VK_LAUNCH_MAIL: 启动邮件键
        VK_LAUNCH_MEDIA_SELECT: 启动媒体选择键
        VK_LAUNCH_APP1: 启动应用程序1键
        VK_LAUNCH_APP2: 启动应用程序2键
        VK_OEM_1: OEM分号键（;:）
        VK_OEM_PLUS: OEM加号键（+）
        VK_OEM_COMMA: OEM逗号键（,）
        VK_OEM_MINUS: OEM减号键（-）
        VK_OEM_PERIOD: OEM句号键（.）
        VK_OEM_2: OEM斜杠键（/?）
        VK_OEM_3: OEM波浪号键（`~）
        VK_OEM_4: OEM左方括号键（[{）
        VK_OEM_5: OEM反斜杠键（\|）
        VK_OEM_6: OEM右方括号键（]}）
        VK_OEM_7: OEM单引号键（'"）
        VK_OEM_8: OEM其他键
        VK_OEM_102: OEM 102键（非美式键盘上的反斜杠）
        VK_PROCESSKEY: 输入法处理键
        VK_PACKET: 数据包键
        VK_ATTN: 注意键
        VK_CRSEL: 光标选择键
        VK_EXSEL: 扩展选择键
        VK_EREOF: 清除EOF键
        VK_PLAY: 播放键
        VK_ZOOM: 缩放键
        VK_NONAME: 无名键
        VK_PA1: PA1键
        VK_OEM_CLEAR: OEM清除键
        VK_GAMEPAD_A: 游戏手柄A键
        VK_GAMEPAD_B: 游戏手柄B键
        VK_GAMEPAD_X: 游戏手柄X键
        VK_GAMEPAD_Y: 游戏手柄Y键
        VK_GAMEPAD_RIGHT_SHOULDER: 游戏手柄右肩键（RB）
        VK_GAMEPAD_LEFT_SHOULDER: 游戏手柄左肩键（LB）
        VK_GAMEPAD_LEFT_TRIGGER: 游戏手柄左扳机键（LT）
        VK_GAMEPAD_RIGHT_TRIGGER: 游戏手柄右扳机键（RT）
        VK_GAMEPAD_DPAD_UP: 游戏手柄方向键上
        VK_GAMEPAD_DPAD_DOWN: 游戏手柄方向键下
        VK_GAMEPAD_DPAD_LEFT: 游戏手柄方向键左
        VK_GAMEPAD_DPAD_RIGHT: 游戏手柄方向键右
        VK_GAMEPAD_MENU: 游戏手柄菜单键（Start）
        VK_GAMEPAD_VIEW: 游戏手柄视图键（Back/Select）
        VK_GAMEPAD_LEFT_THUMBSTICK_BUTTON: 游戏手柄左摇杆按钮（L3）
        VK_GAMEPAD_RIGHT_THUMBSTICK_BUTTON: 游戏手柄右摇杆按钮（R3）
        VK_GAMEPAD_LEFT_THUMBSTICK_UP: 游戏手柄左摇杆向上
        VK_GAMEPAD_LEFT_THUMBSTICK_DOWN: 游戏手柄左摇杆向下
        VK_GAMEPAD_LEFT_THUMBSTICK_RIGHT: 游戏手柄左摇杆向右
        VK_GAMEPAD_LEFT_THUMBSTICK_LEFT: 游戏手柄左摇杆向左
        VK_GAMEPAD_RIGHT_THUMBSTICK_UP: 游戏手柄右摇杆向上
        VK_GAMEPAD_RIGHT_THUMBSTICK_DOWN: 游戏手柄右摇杆向下
        VK_GAMEPAD_RIGHT_THUMBSTICK_RIGHT: 游戏手柄右摇杆向右
        VK_GAMEPAD_RIGHT_THUMBSTICK_LEFT: 游戏手柄右摇杆向左
        
    注意:
        - 部分游戏手柄键码可能不是Windows标准虚拟键码，使用时需要验证
        - 标准的Windows虚拟键码范围在0x01-0xFF之间
        - VK_SHIFT、VK_CONTROL、VK_MENU是通用键，不区分左右
        - VK_LSHIFT/VK_RSHIFT、VK_LCONTROL/VK_RCONTROL、VK_LMENU/VK_RMENU用于区分左右
    '''
    VK_LBUTTON = 0x01
    VK_RBUTTON = 0x02
    VK_CANCEL = 0x03
    VK_MBUTTON = 0x04
    VK_XBUTTON1 = 0x05
    VK_XBUTTON2 = 0x06
    VK_BACK = 0x08
    VK_TAB = 0x09
    VK_CLEAR = 0x0C
    VK_RETURN = 0x0D
    VK_SHIFT = 0x10
    VK_CONTROL = 0x11
    VK_MENU = 0x12
    VK_PAUSE = 0x13
    VK_CAPITAL = 0x14
    VK_KANA = 0x15
    VK_HANGUL = 0x15
    VK_IME_ON = 0x16
    VK_JUNJA = 0x17
    VK_FINAL = 0x18
    VK_HANJA = 0x19
    VK_KANJI = 0x19
    VK_IME_OFF = 0x1A
    VK_ESCAPE = 0x1B
    VK_CONVERT = 0x1C
    VK_NONCONVERT = 0x1D
    VK_ACCEPT = 0x1E
    VK_MODECHANGE = 0x1F
    VK_SPACE = 0x20
    VK_PRIOR = 0x21
    VK_NEXT = 0x22
    VK_END = 0x23
    VK_HOME = 0x24
    VK_LEFT = 0x25
    VK_UP = 0x26
    VK_RIGHT = 0x27
    VK_DOWN = 0x28
    VK_SELECT = 0x29
    VK_PRINT = 0x2A
    VK_EXECUTE = 0x2B
    VK_SNAPSHOT = 0x2C
    VK_INSERT = 0x2D
    VK_DELETE = 0x2E
    VK_HELP = 0x2F
    VK_0 = 0x30
    VK_1 = 0x31
    VK_2 = 0x32
    VK_3 = 0x33
    VK_4 = 0x34
    VK_5 = 0x35
    VK_6 = 0x36
    VK_7 = 0x37
    VK_8 = 0x38
    VK_9 = 0x39
    VK_A = 0x41
    VK_B = 0x42
    VK_C = 0x43
    VK_D = 0x44
    VK_E = 0x45
    VK_F = 0x46
    VK_G = 0x47
    VK_H = 0x48
    VK_I = 0x49
    VK_J = 0x4A
    VK_K = 0x4B
    VK_L = 0x4C
    VK_M = 0x4D
    VK_N = 0x4E
    VK_O = 0x4F
    VK_P = 0x50
    VK_Q = 0x51
    VK_R = 0x52
    VK_S = 0x53
    VK_T = 0x54
    VK_U = 0x55
    VK_V = 0x56
    VK_W = 0x57
    VK_X = 0x58
    VK_Y = 0x59
    VK_Z = 0x5A
    VK_LWIN = 0x5B
    VK_RWIN = 0x5C
    VK_APPS = 0x5D
    VK_SLEEP = 0x5F
    VK_NUMPAD0 = 0x60
    VK_NUMPAD1 = 0x61
    VK_NUMPAD2 = 0x62
    VK_NUMPAD3 = 0x63
    VK_NUMPAD4 = 0x64
    VK_NUMPAD5 = 0x65
    VK_NUMPAD6 = 0x66
    VK_NUMPAD7 = 0x67
    VK_NUMPAD8 = 0x68
    VK_NUMPAD9 = 0x69
    VK_MULTIPLY = 0x6A
    VK_ADD = 0x6B
    VK_SEPARATOR = 0x6C
    VK_SUBTRACT = 0x6D
    VK_DECIMAL = 0x6E
    VK_DIVIDE = 0x6F
    VK_F1 = 0x70
    VK_F2 = 0x71
    VK_F3 = 0x72
    VK_F4 = 0x73
    VK_F5 = 0x74
    VK_F6 = 0x75
    VK_F7 = 0x76
    VK_F8 = 0x77
    VK_F9 = 0x78
    VK_F10 = 0x79
    VK_F11 = 0x7A
    VK_F12 = 0x7B
    VK_F13 = 0x7C
    VK_F14 = 0x7D
    VK_F15 = 0x7E
    VK_F16 = 0x7F
    VK_F17 = 0x80
    VK_F18 = 0x81
    VK_F19 = 0x82
    VK_F20 = 0x83
    VK_F21 = 0x84
    VK_F22 = 0x85
    VK_F23 = 0x86
    VK_F24 = 0x87
    VK_NUMLOCK = 0x90
    VK_SCROLL = 0x91
    VK_LSHIFT = 0xA0
    VK_RSHIFT = 0xA1
    VK_LCONTROL = 0xA2
    VK_RCONTROL = 0xA3
    VK_LMENU = 0xA4
    VK_RMENU = 0xA5
    VK_BROWSER_BACK = 0xA6
    VK_BROWSER_FORWARD = 0xA7
    VK_BROWSER_REFRESH = 0xA8
    VK_BROWSER_STOP = 0xA9
    VK_BROWSER_SEARCH = 0xAA
    VK_BROWSER_FAVORITES = 0xAB
    VK_BROWSER_HOME = 0xAC
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_STOP = 0xB2
    VK_MEDIA_PLAY_PAUSE = 0xB3
    VK_LAUNCH_MAIL = 0xB4
    VK_LAUNCH_MEDIA_SELECT = 0xB5
    VK_LAUNCH_APP1 = 0xB6
    VK_LAUNCH_APP2 = 0xB7
    VK_OEM_1 = 0xBA
    VK_OEM_PLUS = 0xBB
    VK_OEM_COMMA = 0xBC
    VK_OEM_MINUS = 0xBD
    VK_OEM_PERIOD = 0xBE
    VK_OEM_2 = 0xBF
    VK_OEM_3 = 0xC0
    VK_GAMEPAD_A = 0xC3
    VK_GAMEPAD_B = 0xC4
    VK_GAMEPAD_X = 0xC5
    VK_GAMEPAD_Y = 0xC6
    VK_GAMEPAD_RIGHT_SHOULDER = 0xC7
    VK_GAMEPAD_LEFT_SHOULDER = 0xC8
    VK_GAMEPAD_LEFT_TRIGGER = 0xC9
    VK_GAMEPAD_RIGHT_TRIGGER = 0xCA
    VK_GAMEPAD_DPAD_UP = 0xCB
    VK_GAMEPAD_DPAD_DOWN = 0xCC
    VK_GAMEPAD_DPAD_LEFT = 0xCD
    VK_GAMEPAD_DPAD_RIGHT = 0xCE
    VK_GAMEPAD_MENU = 0xCF
    VK_GAMEPAD_VIEW = 0xD0
    VK_GAMEPAD_LEFT_THUMBSTICK_BUTTON = 0xD1
    VK_GAMEPAD_RIGHT_THUMBSTICK_BUTTON = 0xD2
    VK_GAMEPAD_LEFT_THUMBSTICK_UP = 0xD3
    VK_GAMEPAD_LEFT_THUMBSTICK_DOWN = 0xD4
    VK_GAMEPAD_LEFT_THUMBSTICK_RIGHT = 0xD5
    VK_GAMEPAD_LEFT_THUMBSTICK_LEFT = 0xD6
    VK_GAMEPAD_RIGHT_THUMBSTICK_UP = 0xD7
    VK_GAMEPAD_RIGHT_THUMBSTICK_DOWN = 0xD8
    VK_GAMEPAD_RIGHT_THUMBSTICK_RIGHT = 0xD9
    VK_GAMEPAD_RIGHT_THUMBSTICK_LEFT = 0xDA
    VK_OEM_4 = 0xDB
    VK_OEM_5 = 0xDC
    VK_OEM_6 = 0xDD
    VK_OEM_7 = 0xDE
    VK_OEM_8 = 0xDF
    VK_OEM_102 = 0xE2
    VK_PROCESSKEY = 0xE5
    VK_PACKET = 0xE7
    VK_ATTN = 0xF6
    VK_CRSEL = 0xF7
    VK_EXSEL = 0xF8
    VK_EREOF = 0xF9
    VK_PLAY = 0xFA
    VK_ZOOM = 0xFB
    VK_NONAME = 0xFC
    VK_PA1 = 0xFD
    VK_OEM_CLEAR = 0xFE
PostMessage = user32.PostMessageW
'''
用PostMessage异步发送消息到指定窗口。

参数:
    hWnd (int): 目标窗口句柄。
    msg (int): 消息类型，使用keymsg或mousemsg类常量。
    wParam (int): 消息附加参数，键盘消息为虚拟键码，鼠标消息为按键状态标志。
    lParam (int): 消息附加参数，键盘消息含扫描码，鼠标消息含坐标。

返回:
    bool: 成功返回True。

注意:
    - 异步发送，消息放入队列后立即返回，不等待处理。
    - 后台窗口可能拦截或丢弃消息，导致操作无效。
    - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    - 建议先调用SetDPIAware()，避免坐标缩放问题。
    - 键盘消息lParam构造：扫描码(位16-23)|重复计数(位0-15)。
    - 鼠标消息lParam构造：Y坐标(位16-31)|X坐标(位0-15)。
'''
PostMessage.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
]
PostMessage.restype = wintypes.BOOL
PostMessage.errcheck = errcheck


SendMessage = user32.SendMessageW
'''
用SendMessage同步发送消息到指定窗口。

参数:
    hWnd (int): 目标窗口句柄。
    msg (int): 消息类型，使用keymsg或mousemsg类常量。
    wParam (int): 消息附加参数，键盘消息为虚拟键码，鼠标消息为按键状态标志。
    lParam (int): 消息附加参数，键盘消息含扫描码，鼠标消息含坐标。

返回:
    int: 目标窗口消息处理结果，具体含义取决于消息类型。

注意:
    - 同步发送，等待目标窗口处理完成才返回，可能阻塞。
    - 后台窗口可能拦截或丢弃消息，导致操作无效。
    - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    - 建议先调用SetDPIAware()，避免坐标缩放问题。
    - 字符串输入应使用WM_CHAR而非WM_KEYDOWN。
    - 键盘消息lParam构造：扫描码(位16-23)|重复计数(位0-15)。
    - 鼠标消息lParam构造：Y坐标(位16-31)|X坐标(位0-15)。
'''

SendMessage.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
]
SendMessage.restype = ctypes.c_long
SendMessage.errcheck = errcheck


class MOUSEINPUT(ctypes.Structure):
    '''
    鼠标输入结构体, 用于SendInput模拟鼠标事件. 
    
    字段:
        dx (LONG): X坐标/偏移量. 绝对模式: 0-65535映射到虚拟桌面；相对模式: 像素偏移(正右负左). 
        dy (LONG): Y坐标/偏移量. 规则同dx(正下负上). 
        mouseData (DWORD): 滚轮移动量(单位WHEEL_DELTA=120)或X按钮标识(XBUTTON1/XBUTTON2), 其他情况为0. 
        dwFlags (DWORD): 事件标志位组合, 可按位或. 
        time (DWORD): 时间戳(ms), 0表示系统自动提供. 
        dwExtraInfo (ULONG_PTR): 附加信息, 通常为0. 
    
    常量:
        dwFlags:
            MOUSEEVENTF_MOVE(0x0001): 移动. 
            MOUSEEVENTF_LEFTDOWN(0x0002): 左键按下. 
            MOUSEEVENTF_LEFTUP(0x0004): 左键释放. 
            MOUSEEVENTF_RIGHTDOWN(0x0008): 右键按下. 
            MOUSEEVENTF_RIGHTUP(0x0010): 右键释放. 
            MOUSEEVENTF_MIDDLEDOWN(0x0020): 中键按下. 
            MOUSEEVENTF_MIDDLEUP(0x0040): 中键释放. 
            MOUSEEVENTF_XDOWN(0x0080): X键按下. 
            MOUSEEVENTF_XUP(0x0100): X键释放. 
            MOUSEEVENTF_WHEEL(0x0800): 垂直滚轮. 
            MOUSEEVENTF_HWHEEL(0x1000): 水平滚轮(Vista+). 
            MOUSEEVENTF_MOVE_NOCOALESCE(0x2000): 不合并WM_MOUSEMOVE消息. 
            MOUSEEVENTF_VIRTUALDESK(0x4000): 映射到虚拟桌面(需配合ABSOLUTE). 
            MOUSEEVENTF_ABSOLUTE(0x8000): 使用绝对坐标. 
        mouseData:
            XBUTTON1(0x0001): X按钮1(后退). 
            XBUTTON2(0x0002): X按钮2(前进). 
    
    注意:
        - 绝对坐标需配合MOUSEEVENTF_ABSOLUTE|MOUSEEVENTF_VIRTUALDESK, 映射到整个虚拟桌面. 
        - 相对移动受系统鼠标加速度设置影响, 实际移动可能被加倍(最多4倍). 
        - 滚轮正值向前/右滚动, 负值向后/左滚动, 单位为WHEEL_DELTA(120). 
        - X按钮事件需同时指定MOUSEEVENTF_XDOWN/XUP和mouseData(XBUTTON1/XBUTTON2). 
        - 受UIPI限制, 低权限进程无法向高权限窗口发送输入. 
    '''
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong),
    ]
    XBUTTON1 = 0x0001 # 鼠标X按钮1
    XBUTTON2 = 0x0002 # 鼠标X按钮2
    MOUSEEVENTF_MOVE = 0x0001 # 发生移动. 
    MOUSEEVENTF_LEFTDOWN = 0x0002 # 已按下左按钮. 
    MOUSEEVENTF_LEFTUP = 0x0004 # 左按钮已释放. 
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # 已按下右按钮. 
    MOUSEEVENTF_RIGHTUP = 0x0010 # 已释放右侧按钮. 
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # 已按下中间按钮. 
    MOUSEEVENTF_MIDDLEUP = 0x0040 # 中间按钮已释放. 
    MOUSEEVENTF_XDOWN = 0x0080 # 按下了 X 按钮. 
    MOUSEEVENTF_XUP = 0x0100 # 已释放 X 按钮. 
    MOUSEEVENTF_WHEEL = 0x0800 # 滚轮已移动, 如果鼠标有滚轮.  在 mouseData 中指定移动量. 
    MOUSEEVENTF_HWHEEL = 0x1000 # 如果鼠标有滚轮, 则方向盘水平移动.  在 mouseData 中指定移动量. 
    MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000 # 不会合并WM_MOUSEMOVE消息.  默认行为是合并 WM_MOUSEMOVE 消息. 
    MOUSEEVENTF_VIRTUALDESK = 0x4000 # 将坐标映射到整个桌面.  必须与 MOUSEEVENTF_ABSOLUTE一起使用, 如果指定 了MOUSEEVENTF_VIRTUALDESK , 坐标将映射到整个虚拟桌面. 
    MOUSEEVENTF_ABSOLUTE = 0x8000 # dx 和 dy 成员包含规范化的绝对坐标.  如果未设置标志,  dx 和 dy 将包含相对数据（自上次报告位置以来的位置变化）.  无论哪种类型的鼠标或其他指向设备（如果有）都连接到系统, 都可以设置或未设置此标志.  如果指定 了MOUSEEVENTF_ABSOLUTE 值,  则 dx 和 dy 包含介于 0 和 65,535 之间的规范化绝对坐标.  事件过程将这些坐标映射到显示图面.  坐标 （0,0） 映射到显示图面的左上角：坐标 （65535,65535） 映射到右下角.  在多监视器系统中, 坐标映射到主监视器. 如果未指定 MOUSEEVENTF_ABSOLUTE 值,  则 dx 和 dy 指定相对于上一个鼠标事件（上一个报告位置）的移动.  正值表示鼠标向右移动（或向下）：负值表示鼠标向左移动（或向上移动）. 
class KEYBDINPUT(ctypes.Structure):
    '''
    键盘输入结构体, 用于SendInput模拟键盘事件. 
    
    字段:
        wVk (WORD): 虚拟键码(1-254). 使用KEYEVENTF_UNICODE时必须为0. 
        wScan (WORD): 扫描码. 使用KEYEVENTF_SCANCODE或KEYEVENTF_UNICODE时有效. 
        dwFlags (DWORD): 事件标志位组合, 可按位或. 
        time (DWORD): 时间戳(ms), 0表示系统自动提供. 
        dwExtraInfo (ULONG_PTR): 附加信息, 通常为0. 
    
    常量:
        dwFlags:
            KEYEVENTF_EXTENDEDKEY(0x0001): 扩展键(右侧Alt/Ctrl等), 扫描码前缀0xE0. 
            KEYEVENTF_KEYUP(0x0002): 键释放. 未指定则表示键按下. 
            KEYEVENTF_UNICODE(0x0004): Unicode字符输入, wVk必须为0, wScan为Unicode码点. 
            KEYEVENTF_SCANCODE(0x0008): 使用扫描码, 忽略wVk. 
    
    注意:
        - 虚拟键码优先于扫描码, 除非指定KEYEVENTF_SCANCODE. 
        - KEYEVENTF_UNICODE模式下需发送按下和释放两个事件. 
        - Unicode输入时wVk必须为0, wScan为字符的Unicode码点. 
        - 扩展键包括右侧Alt、右侧Ctrl、数字键盘上的Enter等. 
        - 扫描码可通过MapVirtualKeyW(vk, 0)从虚拟键码获取. 
        - 受UIPI限制, 低权限进程无法向高权限窗口发送输入. 
    '''
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong),
    ]
    KEYEVENTF_EXTENDEDKEY = 0x0001 # 如果指定,  wScan 扫描代码由两个字节序列组成, 其中第一个字节的值为0xE0.  有关详细信息 , 请参阅Extended-Key 标志 . 
    KEYEVENTF_KEYUP = 0x0002 # 如果指定, 则释放密钥.  如果未指定, 则按下该键. 
    KEYEVENTF_SCANCODE = 0x0008 # 如果指定,  wScan 将标识密钥并忽略 wVk . 
    KEYEVENTF_UNICODE = 0x0004 # 如果指定, 系统将合成 VK_PACKET 击键.  wVk 参数必须为零.  此标志只能与 KEYEVENTF_KEYUP 标志结合使用. 
class HARDWAREINPUT(ctypes.Structure):
    '''
    硬件输入结构体, 用于SendInput模拟非标准硬件输入. 
    
    字段:
        uMsg (DWORD): 硬件消息类型. 
        wParamL (WORD): 硬件消息参数低位. 
        wParamH (WORD): 硬件消息参数高位. 
    
    注意:
        - 用于模拟非键盘非鼠标的硬件输入, 如游戏手柄等. 
        - 一般情况下不常用, 多数场景使用MOUSEINPUT或KEYBDINPUT. 
        - 受UIPI限制, 低权限进程无法向高权限窗口发送输入. 
    '''
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]
class INPUT_UNION(ctypes.Union):
    '''
    输入联合体, 用于INPUT结构体中存储不同类型的输入数据. 
    
    字段:
        mi (MOUSEINPUT): 鼠标输入数据, type=INPUT_MOUSE时使用. 
        ki (KEYBDINPUT): 键盘输入数据, type=INPUT_KEYBOARD时使用. 
        hi (HARDWAREINPUT): 硬件输入数据, type=INPUT_HARDWARE时使用. 
    
    注意:
        - 联合体字段共享内存, 根据INPUT.type选择使用哪个字段. 
        - 同时只能使用一个字段, 其他字段值无效. 
    '''
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]
class INPUT(ctypes.Structure):
    '''
    输入结构体, 用于SendInput发送输入事件. 
    
    字段:
        type (DWORD): 输入类型. INPUT_MOUSE(0)、INPUT_KEYBOARD(1)、INPUT_HARDWARE(2). 
        union (INPUT_UNION): 输入数据联合体, 根据type选择对应字段. 
    
    常量:
        type:
            INPUT_MOUSE(0): 鼠标输入, 使用union.mi. 
            INPUT_KEYBOARD(1): 键盘输入, 使用union.ki. 
            INPUT_HARDWARE(2): 硬件输入, 使用union.hi. 
    
    注意:
        - type必须正确设置, 否则SendInput无法正确处理. 
        - cbSize参数必须为sizeof(INPUT). 
        - 受UIPI限制, 低权限进程无法向高权限窗口发送输入. 
        - SendInput返回成功插入的事件数, 失败时返回0. 
    '''
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION),
    ]
SendInput = user32.SendInput
'''
用SendInput模拟硬件级输入事件到系统，注入系统底层输入队列，效果最接近真实硬件输入。
参数:
    cInputs (int): 输入事件数。
    pInputs (POINTER(INPUT)): 输入事件结构体(INPUT)组成的列表(C语言数组)。
    cbSize (int): 输入事件结构体大小，默认为sizeof(INPUT)。
返回:
    成功插入的事件数。
注意:
    - 建议使用前 SetDPIAware, 否则很可能出现DPI问题, 已提供 SetDPIAware 函数 方便调用。
    - 发送SendInput消息, 不会被窗口拦截或丢弃, 但却是全局输入无法对无焦点后台窗口生效。
    - 本函数使用难度较高, 建议查询微软官方文档 或 使用本库提供的 高度封装的 键盘/鼠标操作函数。
参考:
    微软官方文档：SendInput function
    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
'''
SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
SendInput.restype = wintypes.UINT
SendInput.errcheck = errcheck

GetSystemMetrics = user32.GetSystemMetrics
'''
获取系统设置或环境变量的值。
参数:
    nIndex: 要获取的系统设置或环境变量的索引。
返回:
    系统设置或环境变量的值。
注意:
    - 受UIPI限制，低权限进程无法调用。
参考:
    微软官方文档：GetSystemMetrics function
    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
'''
GetSystemMetrics.argtypes = [ctypes.c_int]
GetSystemMetrics.restype = ctypes.c_int
GetSystemMetrics.errcheck = errcheck



ClientToScreen = user32.ClientToScreen
'''
转换窗口坐标到屏幕坐标。
参数:
    hWnd: 目标窗口句柄。
    pt: 窗口坐标(x,y)元组。
返回:
    屏幕坐标(x,y)元组。
注意:
    - 受UIPI限制，低权限进程无法调用。
参考:
    微软官方文档：ClientToScreen function
    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-clienttoscreen'''
ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
ClientToScreen.restype = wintypes.BOOL
ClientToScreen.errcheck = errcheck


ScreenToClient = user32.ScreenToClient
'''
转换屏幕坐标到窗口坐标。
参数:
    hWnd: 目标窗口句柄。
    pt: 屏幕坐标(x,y)元组。
返回:
    窗口坐标(x,y)元组。
注意:
    - 受UIPI限制，低权限进程无法调用。
参考:
    微软官方文档：ScreenToClient function
    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-screentoclient
'''
ScreenToClient.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
ScreenToClient.restype = wintypes.BOOL
ScreenToClient.errcheck = errcheck




def key_Input(wVk, wScan, dwFlags, time, dwExtraInfo):
    '''
    用SendInput模拟硬件级键盘输入事件，注入系统底层输入队列，效果最接近真实物理按键。
    参数:
        wVk (int): 虚拟键码，范围1-254，使用KEYEVENTF_UNICODE时必须为0。
        wScan (int): 扫描码，使用KEYEVENTF_SCANCODE或KEYEVENTF_UNICODE时有效。
        dwFlags (int): 事件标志位组合，可按位或，常用值：
            - KEYEVENTF_EXTENDEDKEY(0x0001): 扩展键(右侧Alt/Ctrl等)。
            - KEYEVENTF_KEYUP(0x0002): 键释放，未指定则表示键按下。
            - KEYEVENTF_UNICODE(0x0004): Unicode字符输入，wVk必须为0。
            - KEYEVENTF_SCANCODE(0x0008): 使用扫描码，忽略wVk。
        time (int): 事件时间戳(毫秒)，0表示系统自动提供。
        dwExtraInfo (int): 附加信息，通常为0。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于 SendInput 实现，注入系统底层输入队列，效果最接近真实物理按键。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用 SetDPIAware() 避免DPI相关问题。
        - 虚拟键码优先于扫描码，除非指定KEYEVENTF_SCANCODE。
        - Unicode输入时wVk必须为0，wScan为字符的Unicode码点，需发送按下和释放两个事件。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
    参考:
        微软官方文档：KEYBDINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-keybdinput
    '''
    INPUT结构体 = INPUT()
    INPUT_KEYBOARD = 1 # 键盘输入
    INPUT结构体.type = INPUT_KEYBOARD
    ki = INPUT结构体.union.ki
    ki.wVk = wVk
    ki.wScan = wScan
    ki.dwFlags = dwFlags
    ki.time = time
    ki.dwExtraInfo = dwExtraInfo
    pInputs = (INPUT * 1)(INPUT结构体)
    cInputs = len(pInputs)
    cbSize = ctypes.sizeof(INPUT)
    return SendInput(cInputs, pInputs, cbSize)
def keydown_Post(keycode: int | str | list[int], hWnd: int = None):
    '''
    用PostMessage异步发送键盘按下消息(WM_KEYDOWN)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        keycode: 按键标识，支持多种类型:
            - 字符串: 支持多个字符，每个字符自动转为大写后取其Unicode码点作为虚拟键码(如'A'->65)，仅支持ASCII字符。
            - 整数: 虚拟键码，建议使用keycode命名空间常量(如keycode.VK_A)。
            - 列表: 按键列表，每个元素为虚拟键码，建议使用keycode命名空间常量(如[keycode.VK_A, keycode.VK_B])。
        hWnd: 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        无返回值。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致按键无效。
        - 多个字符时依次发送按下事件，不会自动添加延时。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_KEYDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-keydown
    '''
    if isinstance(keycode, str):
        keycode = [ord(c) for c in keycode.upper()]
    elif isinstance(keycode, int):
        keycode = [keycode]
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    for vk in keycode:
        PostMessage(hWnd, keymsg.WM_KEYDOWN, vk, (user32.MapVirtualKeyW(vk, 0) << 16) | 1)
def keydown_Send(keycode: int | str | list[int], hWnd: int = None):
    '''
    用SendMessage同步发送键盘按下消息(WM_KEYDOWN)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        keycode: 按键标识，支持多种类型:
            - 字符串: 支持多个字符，每个字符自动转为大写后取其Unicode码点作为虚拟键码(如'A'->65)，仅支持ASCII字符。
            - 整数: 虚拟键码，建议使用keycode命名空间常量(如keycode.VK_A)。
            - 列表: 按键列表，每个元素为虚拟键码，建议使用keycode命名空间常量(如[keycode.VK_A, keycode.VK_B])。
        hWnd: 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 无返回值。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致按键无效。
        - 多个字符时依次发送按下事件，不会自动添加延时。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 不建议使用该函数向窗口输入字符串，因为此时使用SendMessage系统不会自动将WM_KEYDOWN转换为WM_CHAR导致输入失效，建议使用string_Send()函数。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_KEYDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-keydown
    '''
    if isinstance(keycode, str):
        keycode = [ord(c) for c in keycode.upper()]
    elif isinstance(keycode, int):
        keycode = [keycode]
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    for vk in keycode:
        SendMessage(hWnd, keymsg.WM_KEYDOWN, vk, (user32.MapVirtualKeyW(vk, 0) << 16) | 1) 
def keydown_Input(keycode: int | str | list[int]):
    '''
    用SendInput模拟硬件级键盘按下事件，注入系统底层输入队列，效果最接近真实物理按键。
    参数:
        keycode: 按键标识，支持多种类型:
            - 字符串: 支持多个字符，每个字符自动转为大写后取其Unicode码点作为虚拟键码(如'A'->65)，仅支持ASCII字符。
            - 整数: 虚拟键码，建议使用keycode命名空间常量(如keycode.VK_A)。
            - 列表: 按键列表，每个元素为虚拟键码，建议使用keycode命名空间常量(如[keycode.VK_A, keycode.VK_B])。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实物理按键。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 多个字符时依次发送按下事件，不会自动添加延时。
        - 无需hWnd参数，全局生效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
    参考:
        微软官方文档：KEYBDINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-keybdinput
    '''
    if isinstance(keycode, str):
        keycode = [ord(c) for c in keycode.upper()]
    elif isinstance(keycode, int):
        keycode = [keycode]
    pInputs = []
    for vk in keycode:
        INPUT结构体 = INPUT()
        INPUT结构体.type = 1
        ki = INPUT结构体.union.ki
        ki.wVk = vk
        ki.wScan = user32.MapVirtualKeyW(vk, 0)
        ki.dwFlags = 0
        ki.time = 0
        ki.dwExtraInfo = 0
        pInputs.append(INPUT结构体)
    pInputs = (INPUT * len(pInputs))(*pInputs)
    cInputs = len(pInputs)
    cbSize = ctypes.sizeof(INPUT)
    return SendInput(cInputs, pInputs, cbSize)
def keyup_Post(keycode: int | str | list[int], hWnd: int = None):
    '''
    用PostMessage异步发送键盘弹起消息(WM_KEYUP)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        keycode: 按键标识，支持多种类型:
            - 字符串: 支持多个字符，每个字符自动转为大写后取其Unicode码点作为虚拟键码(如'A'->65)，仅支持ASCII字符。
            - 整数: 虚拟键码，建议使用keycode命名空间常量(如keycode.VK_A)。
            - 列表: 按键列表，每个元素为虚拟键码，建议使用keycode命名空间常量(如[keycode.VK_A, keycode.VK_B])。
        hWnd: 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        无返回值。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致按键无效。
        - 多个字符时依次发送弹起事件，不会自动添加延时。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_KEYUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-keyup
    '''
    if isinstance(keycode, str):
        keycode = [ord(c) for c in keycode.upper()]
    elif isinstance(keycode, int):
        keycode = [keycode]
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    for vk in keycode:
        PostMessage(hWnd, keymsg.WM_KEYUP, vk, (user32.MapVirtualKeyW(vk, 0) << 16) | 1 | (1 << 30) | (1 << 31))
def keyup_Send(keycode: int | str | list[int], hWnd: int = None):
    '''
    用SendMessage同步发送键盘弹起消息(WM_KEYUP)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        keycode: 按键标识，支持多种类型:
            - 字符串: 支持多个字符，每个字符自动转为大写后取其Unicode码点作为虚拟键码(如'A'->65)，仅支持ASCII字符。
            - 整数: 虚拟键码，建议使用keycode命名空间常量(如keycode.VK_A)。
            - 列表: 按键列表，每个元素为虚拟键码，建议使用keycode命名空间常量(如[keycode.VK_A, keycode.VK_B])。
        hWnd: 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        无返回值。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致按键无效。
        - 多个字符时依次发送弹起事件，不会自动添加延时。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 不建议使用该函数向窗口输入字符串，因为此时使用SendMessage系统不会自动将WM_KEYDOWN转换为WM_CHAR导致输入失效，建议使用string_Send()函数。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_KEYUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-keyup
    '''
    if isinstance(keycode, str):
        keycode = [ord(c) for c in keycode.upper()]
    elif isinstance(keycode, int):
        keycode = [keycode]
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    for vk in keycode:
        SendMessage(hWnd, keymsg.WM_KEYUP, vk, (user32.MapVirtualKeyW(vk, 0) << 16) | 1 | (1 << 30) | (1 << 31))
def keyup_Input(keycode: int | str | list[int]):
    '''
    用SendInput模拟硬件级键盘弹起事件，注入系统底层输入队列，效果最接近真实物理按键。
    参数:
        keycode: 按键标识，支持多种类型:
            - 字符串: 支持多个字符，每个字符自动转为大写后取其Unicode码点作为虚拟键码(如'A'->65)，仅支持ASCII字符。
            - 整数: 虚拟键码，建议使用keycode命名空间常量(如keycode.VK_A)。
            - 列表: 按键列表，每个元素为虚拟键码，建议使用keycode命名空间常量(如[keycode.VK_A, keycode.VK_B])。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实物理按键。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 多个字符时依次发送弹起事件，不会自动添加延时。
        - 无需hWnd参数，全局生效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
    参考:
        微软官方文档：KEYBDINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-keybdinput
    '''
    if isinstance(keycode, str):
        keycode = [ord(c) for c in keycode.upper()]
    elif isinstance(keycode, int):
        keycode = [keycode]
    pInputs = []
    for vk in keycode:
        INPUT结构体 = INPUT()
        INPUT结构体.type = 1
        ki = INPUT结构体.union.ki
        ki.wVk = vk
        ki.wScan = user32.MapVirtualKeyW(vk, 0)
        ki.dwFlags = 0x0002
        ki.time = 0
        ki.dwExtraInfo = 0
        pInputs.append(INPUT结构体)
    pInputs = (INPUT * len(pInputs))(*pInputs)
    cInputs = len(pInputs)
    cbSize = ctypes.sizeof(INPUT)
    return SendInput(cInputs, pInputs, cbSize) 
def string_Post(string: str, hWnd: int = None):
    '''
    用PostMessage异步发送字符串(WM_CHAR)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        string (str): 要发送的字符串。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        无返回值。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致按键无效。
        - 多个字符时依次发送输入事件，不会自动添加延时。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:    
        微软官方文档：WM_CHAR message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-char
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    for c in string:
        PostMessage(hWnd, keymsg.WM_CHAR, ord(c), (user32.MapVirtualKeyW(ord(c), 0) << 16) | 1)
def string_Send(string: str, hWnd: int = None):
    '''
    用SendMessage同步发送字符串(WM_CHAR)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        string (str): 要发送的字符串。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        无返回值。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致按键无效。
        - 多个字符时依次发送输入事件，不会自动添加延时。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_CHAR message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-char
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    for c in string:
        SendMessage(hWnd, keymsg.WM_CHAR, ord(c), (user32.MapVirtualKeyW(ord(c), 0) << 16) | 1)
def string_Input(string: str):
    '''
    用SendInput模拟硬件级键盘输入事件，注入系统底层输入队列，效果最接近真实物理按键。
    参数:
        string (str): 要输入的字符串。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实物理按键。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 多个字符时依次发送输入事件，不会自动添加延时。
        - 无需hWnd参数，全局生效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
    参考:
        微软官方文档：KEYBDINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-keybdinput
    '''
    pInputs = []
    for c in string:
        INPUT结构体 = INPUT()
        INPUT结构体.type = 1
        ki = INPUT结构体.union.ki
        ki.wVk = 0
        ki.wScan = ord(c)
        ki.dwFlags = KEYBDINPUT.KEYEVENTF_UNICODE
        ki.time = 0
        ki.dwExtraInfo = 0
        pInputs.append(INPUT结构体)
        INPUT结构体 = INPUT()
        INPUT结构体.type = 1
        ki = INPUT结构体.union.ki
        ki.wVk = 0
        ki.wScan = ord(c)
        ki.dwFlags = KEYBDINPUT.KEYEVENTF_UNICODE | KEYBDINPUT.KEYEVENTF_KEYUP
        ki.time = 0
        ki.dwExtraInfo = 0
        pInputs.append(INPUT结构体)
    pInputs = (INPUT * len(pInputs))(*pInputs)
    cInputs = len(pInputs)
    cbSize = ctypes.sizeof(INPUT)
    return SendInput(cInputs, pInputs, cbSize)
def mouse_Input(dx, dy, mouseData, dwFlags, time, dwExtraInfo):
    '''
    用SendInput模拟硬件级鼠标输入事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        dx (int): 鼠标移动量。
            - 若dwFlags包含MOUSEEVENTF_ABSOLUTE：范围为0~65535的绝对坐标，映射到整个屏幕（0,0左上角，65535,65535右下角）。
            - 若未包含绝对标志：相对上次位置的像素偏移量，正数表示右/下，负数表示左/上。
        dy (int): 鼠标移动量，规则同dx。
        mouseData (int): 鼠标滚轮或X按钮数据，取决于dwFlags：
            - MOUSEEVENTF_WHEEL/MOUSEEVENTF_HWHEEL：滚轮移动量，单位为WHEEL_DELTA(120)，正数向前/向右，负数向后/向左。
            - MOUSEEVENTF_XDOWN/MOUSEEVENTF_XUP：X按钮标识，如XBUTTON1(0x0001)、XBUTTON2(0x0002)。
            - 其他情况：必须为0。
        dwFlags (int): 鼠标事件标志位组合（可按位或），常用值：
            - 移动：MOUSEEVENTF_MOVE(0x0001)
            - 绝对坐标：MOUSEEVENTF_ABSOLUTE(0x8000)
            - 左键：MOUSEEVENTF_LEFTDOWN(0x0002)/LEFTUP(0x0004)
            - 右键：MOUSEEVENTF_RIGHTDOWN(0x0008)/RIGHTUP(0x0010)
            - 中键：MOUSEEVENTF_MIDDLEDOWN(0x0020)/MIDDLEUP(0x0040)
            - X键：MOUSEEVENTF_XDOWN(0x0080)/XUP(0x0100)
            - 垂直滚轮：MOUSEEVENTF_WHEEL(0x0800)
            - 水平滚轮：MOUSEEVENTF_HWHEEL(0x1000)(Vista+)
            - 不合并移动消息：MOUSEEVENTF_MOVE_NOCOALESCE(0x2000)(XP+)
            - 映射到虚拟桌面：MOUSEEVENTF_VIRTUALDESK(0x4000)(需配合绝对坐标)
        time (int): 事件时间戳（毫秒）。为0时由系统自动提供。
        dwExtraInfo (int): 附加信息，可通过GetMessageExtraInfo()获取，通常设为0。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则可能无法接收输入（受UIPI和窗口消息过滤影响）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 该函数使用难度较高，需手动构造标志位和计算坐标。强烈建议使用高度封装的辅助函数（如mouse_move()，mouse_leftdown()等）。
        - 相对移动受系统鼠标"提高指针精确度"（加速度）设置影响，实际移动距离可能被系统加倍（最多4倍）。如需精确控制，请使用绝对坐标模式（MOUSEEVENTF_ABSOLUTE）。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    INPUT结构体 = INPUT()
    INPUT_MOUSE = 0 # 鼠标输入
    INPUT结构体.type = INPUT_MOUSE
    mi = INPUT结构体.union.mi
    mi.dx = dx
    mi.dy = dy
    mi.mouseData = mouseData
    mi.dwFlags = dwFlags
    mi.time = time
    mi.dwExtraInfo = dwExtraInfo
    pInputs = (INPUT * 1)(INPUT结构体)
    cInputs = len(pInputs)
    cbSize = ctypes.sizeof(INPUT)
    return SendInput(cInputs, pInputs, cbSize)
def mouse_move_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标移动消息(WM_MOUSEMOVE)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标失效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_MOUSEMOVE message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mousemove
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    return PostMessage(hWnd, mousemsg.WM_MOUSEMOVE, 0, (y << 16) | (x & 0xFFFF))
def mouse_move_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标移动消息(WM_MOUSEMOVE)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标失效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_MOUSEMOVE message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mousemove
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    return SendMessage(hWnd, mousemsg.WM_MOUSEMOVE, 0, (y << 16) | (x & 0xFFFF))
def mouse_move_Input(x: int, y: int, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标移动事件，注入系统底层输入队列，效果最接近真实物理按键。
    参数:
        x (int): 鼠标的X坐标。
        y (int): 鼠标的Y坐标。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实物理按键。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    if absmove:
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
        dwFlags = MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_MOVE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK
    else:
        dwFlags = MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_leftdown_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标左键按下消息(WM_LBUTTONDOWN)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标失效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_LBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-lbuttondown
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_LBUTTON = 0x0001
    return PostMessage(hWnd, mousemsg.WM_LBUTTONDOWN, MK_LBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_leftdown_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标左键按下消息(WM_LBUTTONDOWN)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标失效。
        - 建议先调用SetDPIAware()避免DPI相关问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
    参考:
        微软官方文档：WM_LBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-lbuttondown
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_LBUTTON = 0x0001
    return SendMessage(hWnd, mousemsg.WM_LBUTTONDOWN, MK_LBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_leftdown_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标左键按下事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接按下左键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接按下左键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_LEFTDOWN
    if x is None and y is None:
        dx = dy = 0
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_leftup_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标左键弹起消息(WM_LBUTTONUP)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_LBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-lbuttonup
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_LBUTTON = 0x0001
    return PostMessage(hWnd, mousemsg.WM_LBUTTONUP, MK_LBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_leftup_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标左键弹起消息(WM_LBUTTONUP)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_LBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-lbuttonup
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_LBUTTON = 0x0001
    return SendMessage(hWnd, mousemsg.WM_LBUTTONUP, MK_LBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_leftup_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标左键弹起事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接释放左键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接释放左键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_LEFTUP
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_rightdown_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标右键按下消息(WM_RBUTTONDOWN)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_RBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-rbuttondown
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_RBUTTON = 0x0002
    return PostMessage(hWnd, mousemsg.WM_RBUTTONDOWN, MK_RBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_rightdown_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标右键按下消息(WM_RBUTTONDOWN)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_RBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-rbuttondown
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_RBUTTON = 0x0002
    return SendMessage(hWnd, mousemsg.WM_RBUTTONDOWN, MK_RBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_rightdown_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标右键按下事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接按下右键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接按下右键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_RIGHTDOWN
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_rightup_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标右键弹起消息(WM_RBUTTONUP)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_RBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-rbuttonup
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_RBUTTON = 0x0002
    return PostMessage(hWnd, mousemsg.WM_RBUTTONUP, MK_RBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_rightup_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标右键弹起消息(WM_RBUTTONUP)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_RBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-rbuttonup
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_RBUTTON = 0x0002
    return SendMessage(hWnd, mousemsg.WM_RBUTTONUP, MK_RBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_rightup_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标右键弹起事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接释放右键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接释放右键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_RIGHTUP
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_middledown_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标中键按下消息(WM_MBUTTONDOWN)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mbuttondown
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0010
    return PostMessage(hWnd, mousemsg.WM_MBUTTONDOWN, MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_middledown_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标中键按下消息(WM_MBUTTONDOWN)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mbuttondown
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0010
    return SendMessage(hWnd, mousemsg.WM_MBUTTONDOWN, MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_middledown_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标中键按下事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接按下中键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接按下中键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_MIDDLEDOWN
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_middleup_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标中键弹起消息(WM_MBUTTONUP)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mbuttonup
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0010
    return PostMessage(hWnd, mousemsg.WM_MBUTTONUP, MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_middleup_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标中键弹起消息(WM_MBUTTONUP)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mbuttonup
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0010
    return SendMessage(hWnd, mousemsg.WM_MBUTTONUP, MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_middleup_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标中键弹起事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接释放中键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接释放中键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_MIDDLEUP
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, 0, dwFlags, 0, 0)
def mouse_wheel_Post(delta: int, x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标垂直滚轮消息(WM_MOUSEWHEEL)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        delta (int): 滚轮滚动量，单位为WHEEL_DELTA(120)。正数向前滚动，负数向后滚动。
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MOUSEWHEEL message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mousewheel
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0000  # 滚轮消息wParam通常不包含按键标志
    return PostMessage(hWnd, mousemsg.WM_MOUSEWHEEL, (delta << 16) | MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_wheel_Send(delta: int, x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标垂直滚轮消息(WM_MOUSEWHEEL)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        delta (int): 滚轮滚动量，单位为WHEEL_DELTA(120)。正数向前滚动，负数向后滚动。
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MOUSEWHEEL message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mousewheel
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0000
    return SendMessage(hWnd, mousemsg.WM_MOUSEWHEEL, (delta << 16) | MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_wheel_Input(delta: int, x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标垂直滚轮事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        delta (int): 滚轮滚动量，单位为WHEEL_DELTA(120)。正数向前滚动，负数向后滚动。
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接滚动滚轮。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接滚动滚轮。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_WHEEL
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, delta, dwFlags, 0, 0)
def mouse_hwheel_Post(delta: int, x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标水平滚轮消息(WM_MOUSEHWHEEL)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        delta (int): 滚轮滚动量，单位为WHEEL_DELTA(120)。正数向右滚动，负数向左滚动。
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MOUSEHWHEEL message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mousehwheel
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0000
    return PostMessage(hWnd, mousemsg.WM_MOUSEHWHEEL, (delta << 16) | MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_hwheel_Send(delta: int, x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标水平滚轮消息(WM_MOUSEHWHEEL)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        delta (int): 滚轮滚动量，单位为WHEEL_DELTA(120)。正数向右滚动，负数向左滚动。
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_MOUSEHWHEEL message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-mousehwheel
    '''
    if hWnd is None:hWnd = ctypes.windll.user32.GetForegroundWindow()
    MK_MBUTTON = 0x0000
    return SendMessage(hWnd, mousemsg.WM_MOUSEHWHEEL, (delta << 16) | MK_MBUTTON, (y << 16) | (x & 0xFFFF))
def mouse_hwheel_Input(delta: int, x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标水平滚轮事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        delta (int): 滚轮滚动量，单位为WHEEL_DELTA(120)。正数向右滚动，负数向左滚动。
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接滚动滚轮。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接滚动滚轮。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_HWHEEL
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, delta, dwFlags, 0, 0)
def mouse_x1down_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标X1按下消息(WM_XBUTTONDOWN)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttondown
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON1 = 0x0001  # X按钮编号
    MK_XBUTTON1 = 0x0020  # 按键状态标志
    wParam = (XBUTTON1 << 16) | MK_XBUTTON1
    return PostMessage(hWnd, mousemsg.WM_XBUTTONDOWN, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x1down_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标X1按下消息(WM_XBUTTONDOWN)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow()).
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttondown
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON1 = 0x0001  # X按钮编号
    MK_XBUTTON1 = 0x0020  # 按键状态标志
    wParam = (XBUTTON1 << 16) | MK_XBUTTON1
    return SendMessage(hWnd, mousemsg.WM_XBUTTONDOWN, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x1down_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标X1键（后退键）按下事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接按下X1键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接按下X1键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_XDOWN
    mouseData = MOUSEINPUT.XBUTTON1
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, mouseData, dwFlags, 0, 0)
def mouse_x1up_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标X1弹起消息(WM_XBUTTONUP)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttonup
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON1 = 0x0001  # X按钮编号
    MK_XBUTTON1 = 0x0020  # 按键状态标志
    wParam = (XBUTTON1 << 16) | MK_XBUTTON1
    return PostMessage(hWnd, mousemsg.WM_XBUTTONUP, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x1up_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标X1弹起消息(WM_XBUTTONUP)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttonup
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON1 = 0x0001  # X按钮编号
    MK_XBUTTON1 = 0x0020  # 按键状态标志
    wParam = (XBUTTON1 << 16) | MK_XBUTTON1
    return SendMessage(hWnd, mousemsg.WM_XBUTTONUP, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x1up_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标X1键（后退键）弹起事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接释放X1键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接释放X1键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_XUP
    mouseData = MOUSEINPUT.XBUTTON1
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, mouseData, dwFlags, 0, 0)
def mouse_x2down_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标X2按下消息(WM_XBUTTONDOWN)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttondown
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON2 = 0x0002  # X按钮编号
    MK_XBUTTON2 = 0x0040  # 按键状态标志
    wParam = (XBUTTON2 << 16) | MK_XBUTTON2
    return PostMessage(hWnd, mousemsg.WM_XBUTTONDOWN, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x2down_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标X2按下消息(WM_XBUTTONDOWN)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONDOWN message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttondown
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON2 = 0x0002  # X按钮编号
    MK_XBUTTON2 = 0x0040  # 按键状态标志
    wParam = (XBUTTON2 << 16) | MK_XBUTTON2
    return SendMessage(hWnd, mousemsg.WM_XBUTTONDOWN, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x2down_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标X2键（前进键）按下事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接按下X2键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接按下X2键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_XDOWN
    mouseData = MOUSEINPUT.XBUTTON2
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, mouseData, dwFlags, 0, 0)
def mouse_x2up_Post(x: int, y: int, hWnd: int = None):
    '''
    用PostMessage异步发送鼠标X2弹起消息(WM_XBUTTONUP)到指定窗口，消息放入队列后立即返回，不等待处理。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        bool: 成功返回True，失败返回False。
    注意:
        - 基于PostMessage实现，异步发送，消息放入队列后立即返回，不等待处理。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttonup
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON2 = 0x0002  # X按钮编号
    MK_XBUTTON2 = 0x0040  # 按键状态标志
    wParam = (XBUTTON2 << 16) | MK_XBUTTON2
    return PostMessage(hWnd, mousemsg.WM_XBUTTONUP, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x2up_Send(x: int, y: int, hWnd: int = None):
    '''
    用SendMessage同步发送鼠标X2弹起消息(WM_XBUTTONUP)到指定窗口，等待目标窗口处理完成才返回。
    参数:
        x (int): 鼠标相对窗口的X坐标。
        y (int): 鼠标相对窗口的Y坐标。
        hWnd (int): 目标窗口句柄，默认为当前焦点窗口(GetForegroundWindow())。
    返回:
        int: 目标窗口消息处理结果，具体含义取决于消息类型。
    注意:
        - 基于SendMessage实现，同步发送，等待目标窗口处理完成才返回，可能阻塞。
        - 后台窗口可能拦截或丢弃消息，导致鼠标操作无效。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标缩放问题。
        - 该函数仅有限改变窗口内部对鼠标的感知，不会改变真实鼠标状态。
        - 受UIPI限制，低权限进程无法向高权限窗口发送消息。
        - 坐标应为窗口客户区相对坐标，而非屏幕绝对坐标。
    参考:
        微软官方文档：WM_XBUTTONUP message
        https://learn.microsoft.com/zh-cn/windows/win32/inputdev/wm-xbuttonup
    '''
    if hWnd is None:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
    XBUTTON2 = 0x0002  # X按钮编号
    MK_XBUTTON2 = 0x0040  # 按键状态标志
    wParam = (XBUTTON2 << 16) | MK_XBUTTON2
    return SendMessage(hWnd, mousemsg.WM_XBUTTONUP, wParam, (y << 16) | (x & 0xFFFF))
def mouse_x2up_Input(x: int = None, y: int = None, absmove: bool = True):
    '''
    用SendInput模拟硬件级鼠标X2键（前进键）弹起事件，注入系统底层输入队列，效果最接近真实硬件输入。
    参数:
        x (int): 鼠标的X坐标。当x和y均为None时，不移动鼠标直接释放X2键。
        y (int): 鼠标的Y坐标。当x和y均为None时，不移动鼠标直接释放X2键。
        absmove (bool): 是否采用绝对坐标移动，默认为True。
            - True: 使用绝对坐标模式，坐标映射到整个虚拟桌面(0-65535范围)。
            - False: 使用相对坐标模式，坐标表示相对于当前位置的像素偏移量。
    返回:
        int: 成功插入的事件数，失败时返回0。
    注意:
        - 基于SendInput实现，注入系统底层输入队列，效果最接近真实硬件输入。
        - 目标窗口必须处于前台并具有焦点，否则无法接收输入（受UIPI限制）。
        - 建议先调用SetDPIAware()，避免在高DPI屏幕下坐标映射错误。
        - 相对移动受系统鼠标加速度设置影响，实际移动距离可能被系统加倍。
        - 受UIPI限制，低权限进程无法向高权限窗口发送输入。
        - 该操作需要UIAccess权限或运行在管理员权限下才可跨进程模拟高完整性级别窗口。
    参考:
        微软官方文档：MOUSEINPUT structure
        https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-mouseinput
    '''
    dwFlags = MOUSEINPUT.MOUSEEVENTF_XUP
    mouseData = MOUSEINPUT.XBUTTON2
    if x is None and y is None:
        dx = dy = 0
        
    elif absmove:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_ABSOLUTE | MOUSEINPUT.MOUSEEVENTF_VIRTUALDESK | MOUSEINPUT.MOUSEEVENTF_MOVE
        SM_XVIRTUALSCREEN = 76  # 虚拟桌面左边缘在整个屏幕坐标系中的 X 坐标值
        SM_YVIRTUALSCREEN = 77  # 虚拟桌面上边缘在整个屏幕坐标系中的 Y 坐标值
        SM_CXVIRTUALSCREEN = 78  # 虚拟屏幕的宽度
        SM_CYVIRTUALSCREEN = 79  # 虚拟屏幕的高度
        # 映射到 0~65535 范围
        dx = int((x - GetSystemMetrics(SM_XVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CXVIRTUALSCREEN)))
        dy = int((y - GetSystemMetrics(SM_YVIRTUALSCREEN)) * 0x10000 / (GetSystemMetrics(SM_CYVIRTUALSCREEN)))
    else:
        dwFlags |= MOUSEINPUT.MOUSEEVENTF_MOVE
        dx = x
        dy = y
    return mouse_Input(dx, dy, mouseData, dwFlags, 0, 0)
