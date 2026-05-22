"""窗口基础组件"""
from PySide6.QtWidgets import QApplication  # 应用程序实例
from PySide6.QtWidgets import QWidget  # 基础窗口容器
from PySide6.QtWidgets import QSystemTrayIcon  # 系统托盘图标
from PySide6.QtWidgets import QInputDialog  # 输入弹窗
from PySide6.QtWidgets import QLabel  # 文本/图片标签
from PySide6.QtWidgets import QMenu  # 菜单
from PySide6.QtWidgets import QTextEdit  # 文本气泡控件
from PySide6.QtWidgets import QVBoxLayout  # 垂直布局工具
from PySide6.QtWidgets import QHBoxLayout  # 水平布局工具
import ctypes
# from ctypes import wintypes  用于调用winAPI

"""动画与鼠标交互"""
from PySide6.QtGui import QMovie  # GIF动画播放
from PySide6.QtGui import QMouseEvent  # 鼠标事件处理
from PySide6.QtGui import QCursor  # 鼠标光标
from PySide6.QtGui import QIcon  # 图标资源
from PySide6.QtGui import QAction  # 菜单/快捷动作
from PySide6.QtGui import QTextOption  # 用于智能换行
from random import randint, choice  # 用于随机表情
# ImageQt模块用于在PIL图像与Qt图像类型之间进行转换的功能
from PIL.ImageQt import QPixmap

"""核心功能与计时器"""
from PySide6.QtCore import QTimer  # 定时器
from PySide6.QtCore import QPoint  # 坐标点数据
from PySide6.QtCore import Qt  # 全局变量与枚举

import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数,用于初始化父类基础属性

        def find_project_root():
            script_dir:str = os.path.dirname(os.path.abspath(__file__))
            target_folder = "images"
            project_root = "Table pet"

            current: str = script_dir

            while current != os.path.dirname(current):
                if target_folder in os.listdir(current):
                    return current
                elif project_root in os.listdir(current):
                    return os.path.join(current, project_root)
                current = os.path.dirname(current)
            return current

        self.path = find_project_root()
        """窗口属性"""
        self.setWindowTitle("Toble pet")
        self.setFixedSize(280, 120)

        # 设置窗口图标
        self.windowIcon = QIcon(os.path.join(self.path, "images/haqian.gif"))
        self.setWindowIcon(self.windowIcon)
        # 设置窗口特性 无边框 Qt.WindowType.FramelessWindowHint | 置顶
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # 设置窗口属性 背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # 设置窗口穿透
        self.test_bool = False
        self.set_window_hit_test_visible(not self.test_bool)  # 不进行窗口穿透
        # 设置窗口在屏幕位置
        self.screen_rect = QApplication.primaryScreen().availableGeometry()  # 获取屏幕大小
        self.move(int(self.screen_rect.width() - self.width()), int(self.screen_rect.height() * 0.8))
        # 设置透明度
        self.window_opacity = 1.0
        self.setWindowOpacity(self.window_opacity)

        """托盘属性"""
        self.tray = None  # 托盘实例
        self.tray_opacity_menu = None  # 透明度
        self.customization_op = None  # 自定义窗口透明度
        self.op_actions = {}  # 透明度子菜单
        self.tray_toggle_hit = None  # 窗口穿透选项

        self.tray_top = None  # 窗口置顶选项
        self.initTray()  # 托盘初始化

        """动画"""
        self.label = QLabel(self)  # 初始化GIF播放组件
        self.label.setFixedSize(120, 120)  # 动画大小
        self.label.setScaledContents(True)  # 使内容自适应窗口大小

        # 气泡
        self.bubble_bg = QLabel(self)
        self.bubble_bg.setPixmap(QPixmap(os.path.join(self.path, "images/bubble_bg.png")))
        self.bubble_bg.setScaledContents(True)
        self.bubble_bg.setFixedSize(140, 85)
        self.bubble_bg.move(8, 0)
        self.bubble_bg.hide()
        self.bubble_text = QTextEdit(self.bubble_bg)
        self.bubble_text.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere) # 自动换行
        self.bubble_text.setReadOnly(True)  # 只读
        self.bubble_text.hide()
        self.bubble_text.setStyleSheet("""
            QTextEdit {
                color : white;
                font-size: 12px;
                font-family: 微软雅黑;
                font-height: 12px;
                background-color: transparent;  /* 透明背景，不遮挡气泡图 */
                border: none;  /* 去掉边框 */
                padding: 0px;  /* 取消内边距，靠布局控制位置 */
            }
        """)
        #  控制文字位置  居中+内边距
        # 创建垂直布局 控制上下间距
        bubble_Vlayout = QVBoxLayout(self.bubble_bg)
        bubble_Vlayout.setContentsMargins(12, 15, 14, 0)
        bubble_Vlayout.setSpacing(0)

        # 创建水平布局 控制左右居中
        bubble_Hlayout = QHBoxLayout()
        bubble_Hlayout.addWidget(self.bubble_text)
        bubble_Hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)   # 绝对居中
        bubble_Vlayout.addLayout(bubble_Hlayout)    # 嵌套布局格式

        # 调整动画在窗口位置
        label_layout = QHBoxLayout(self)
        label_layout.setContentsMargins(0, 0, 0, 0)  # 去除所有内边距
        label_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.setLayout(label_layout)  # 应用到窗口

        # 动画资源
        self.movie_eat = QMovie(os.path.join(self.path, "images/eat.gif"))
        self.movie_eat.name = 'eat'
        self.movie_eat.start()  # 播放动画
        self.label.setMovie(self.movie_eat)

        self.movie_left = QMovie(os.path.join(self.path, "images/left.gif"))
        self.movie_left.name = 'left'
        self.movie_left.start()

        self.movie_cahan = QMovie(os.path.join(self.path, "images/cahan.gif"))
        self.movie_cahan.name = 'cahan'
        self.movie_cahan.start()

        self.movie_sleep = QMovie(os.path.join(self.path, "images/sleep.gif"))
        self.movie_sleep.name = 'sleep'
        self.movie_sleep.start()

        self.movie_angry = QMovie(os.path.join(self.path, "images/angry.gif"))
        self.movie_angry.name = 'angry'
        self.movie_angry.start()

        self.movie_liulei = QMovie(os.path.join(self.path, "images/liulei.gif"))
        self.movie_liulei.name = 'liulei'
        self.movie_liulei.start()

        # 随机气泡
        self.dialog_texts = {
            "eat": [
                "今天天气真好呀～(≧∇≦)ﾉ",
                "你在忙什么呢？(・ω・)",
                "好无聊哦，陪我玩～(｡•́︿•̀｡)",
                "我饿啦，要吃零食！(๑´ڡ`๑)",
                "你鸟鸟我呗(✿◕‿◕✿)"
            ],
            "sleep": [
                "呼～呼～(￣o￣) . z Z",
                "不要吵我睡觉啦～",
                "zzzzzz……"
            ],
            "angry": [
                "哼！不理你了(｀^´)",
                "离我远一点！",
                "再碰我就生气啦！"
            ],
            "liulei": [
                "呜呜呜没人理我(Ｔ▽Ｔ)",
                "我好委屈……",
                "抱抱我好不好～",
                "你怎么不鸟我o(TヘTo)"
            ],
            "left": [
                "我走啦我走啦～",
                "向左走～向右走～",
                "跑咯跑咯！"
            ],
            "hei": [
                "嘿嘿抓到你啦～",
                "被我发现了吧！",
                "嘻嘻嘻(≧∇≦)ﾉ"
            ]
        }

        # 属性
        self.is_move = False    # 是否可移动
        self.is_left = False     # 是否在最左边
        self.max_move_x = 350
        self.move_x = 0

        # 动画计时器
        # 回到原图的计时器
        self.initial_time_number = 5
        self.initial_gifTime = QTimer(self)
        self.initial_gifTime.setSingleShot(True)
        self.initial_gifTime.setInterval(self.initial_time_number * 1000)
        self.initial_gifTime.timeout.connect(self.to_initial_gif)
        # 移动
        self.move_time = QTimer(self)
        self.move_time.timeout.connect(self.pikaMove)
        self.move_time.setInterval(50)
        # 显示气泡计时器 全局
        self.showBubble_time_number = 12
        self.showBubble_time = QTimer(self)
        self.showBubble_time.setInterval(self.showBubble_time_number * 1000)
        self.showBubble_time.start()
        self.showBubble_time.timeout.connect(self.show_bubble)
        # 隐藏气泡的计时器
        self.hideBubble_time_number = 3
        self.hideBubble_time = QTimer(self)
        self.hideBubble_time.setSingleShot(True)
        self.hideBubble_time.setInterval(self.hideBubble_time_number * 1000)
        self.hideBubble_time.timeout.connect(self.hide_bubble)

        # 随机表情的计时器
        self.randomLook_time_number = 25
        self.randomLook_time = QTimer(self)
        self.randomLook_time.setInterval(self.randomLook_time_number * 1000)
        self.randomLook_time.start()
        self.randomLook_time.timeout.connect(self.play_random_look)

        """鼠标相关属性"""
        self.is_follow_mouse = False  # 窗口跟随鼠标移动
        self.mouse_drag_pos = QPoint()  # 记录鼠标拖动起点

        """右键菜单"""
        self.op_actionsR = {}
        self.menuRight = QMenu(self)

        self.Rleft_action = QAction("左", self)
        self.Rleft_action.triggered.connect(self.RLeft)
        self.menuRight.addAction(self.Rleft_action)

        self.right_opacity_menu = QMenu("调整窗口透明度", self)
        self.right_opacity_op = QAction("自定义透明度", self)
        self.right_opacity_op.setCheckable(True)
        self.right_opacity_op.triggered.connect(self.set_opacity_custom)
        self.right_opacity_menu.addAction(self.right_opacity_op)
        values = [100, 75, 50, 25]
        for v in values:
            opacity_action = QAction(f"透明度:{v}%", self, checkable=True)
            opacity_action.triggered.connect(lambda checked, val=v: self.opacity_action_set_opacity(val))
            self.right_opacity_menu.addAction(opacity_action)
            self.op_actionsR[v] = opacity_action
            if v == self.window_opacity * 100:
                opacity_action.setChecked(True)

        self.menuRight.addMenu(self.right_opacity_menu)

        self.right_top = QAction("取消置顶", self)
        self.right_top.triggered.connect(self.toggle_window_top)
        self.menuRight.addAction(self.right_top)

        self.menuRight.addSeparator()

        self.right_quit = QAction("退出", self)
        self.right_quit.triggered.connect(app.quit)
        self.menuRight.addAction(self.right_quit)

    """ 切换动画(动画自带属性) """
    def ImageEat(self):
        self.is_move = False
        self.is_follow_mouse = False
        self.label.setMovie(self.movie_eat)

    def ImageLeft(self):
        self.is_move = True
        self.is_left = False
        self.move_time.start()

        self.label.setMovie(self.movie_left)

    def ImageCahan(self):
        self.is_follow_mouse = True
        self.is_move = False
        self.label.setMovie(self.movie_cahan)

    def ImageSleep(self):
        self.label.setMovie(self.movie_sleep)

    def ImageAngry(self):
        self.label.setMovie(self.movie_angry)

    def ImageLiulei(self):
        self.label.setMovie(self.movie_liulei)

    """系统托盘"""
    def initTray(self):
        self.tray = QSystemTrayIcon(self)  # 托盘实例
        menu = QMenu(self)  # 菜单实例
        self.tray.setContextMenu(menu)  # 托盘与菜单关联
        tray_Icon = QIcon("images/haqian.gif")
        self.tray.setIcon(tray_Icon)  # 设置托盘图标

        """窗口透明度"""
        self.tray_opacity_menu = QMenu("调整窗口透明度", self)
        self.customization_op = QAction("自定义透明度")
        self.customization_op.setCheckable(True)
        self.customization_op.triggered.connect(self.set_opacity_custom)
        self.tray_opacity_menu.addAction(self.customization_op)
        values = [100, 75, 50, 25]
        for v in values:
            opacity_action = QAction(f"透明度:{v}%", self, checkable=True)
            opacity_action.triggered.connect(lambda checked, val=v: self.opacity_action_set_opacity(val))
            self.tray_opacity_menu.addAction(opacity_action)
            self.op_actions[v] = opacity_action
            if v == self.window_opacity * 100:
                opacity_action.setChecked(True)

        menu.addMenu(self.tray_opacity_menu)  # 添加此子菜单到主菜单

        self.tray_top = QAction("取消置顶")
        self.tray_top.triggered.connect(self.toggle_window_top)
        menu.addAction(self.tray_top)

        self.tray_toggle_hit = QAction("窗口穿透", self)
        self.tray_toggle_hit.triggered.connect(self.toggle_window_hit)
        menu.addAction(self.tray_toggle_hit)

        menu.addSeparator()  # 分割线

        tray_quit = QAction("退出", self)
        tray_quit.triggered.connect(app.quit)
        menu.addAction(tray_quit)

        self.tray.activated.connect(self.on_tray_activated)  # 调用弹出菜单
        self.tray.show()  # 显示托盘

    # 自定义透明度输入
    def set_opacity_custom(self):
        # 标题 提示 范围 默认值 步长
        dialog = QInputDialog(self)
        dialog.setWindowTitle("自定义透明度输入框")
        dialog.setLabelText("请输入10~100之间的整数")
        dialog.setIntRange(25, 100)
        dialog.setIntValue(100)
        dialog.setIntStep(1)
        dialog.setOkButtonText("确认")
        dialog.setCancelButtonText("取消")

        if dialog.exec():
            value = dialog.intValue()
            self.set_opacity(value)
            if value in self.op_actions.keys():
                self.opacity_action_set_opacity(value)
            else:
                self.update_opacity_check()
                self.customization_op.setText(f"自定义透明度:{value}%")
                self.right_opacity_op.setText(f"自定义透明度:{value}%")
    # 调整透明度
    def set_opacity(self, value):
        # 更新self透明度
        print(f"调整透明度到:{value}%")
        self.window_opacity = value / 100
        self.setWindowOpacity(self.window_opacity)
    # 托盘菜单透明度
    def opacity_action_set_opacity(self, value):
        self.set_opacity(value)
        self.update_opacity_check()

        self.customization_op.setChecked(False)
        self.customization_op.setText("自定义透明度")
        self.right_opacity_op.setChecked(False)
        self.right_opacity_op.setText("自定义透明度")
    # 更新菜单透明度勾选
    def update_opacity_check(self):
        # 全部取消
        for v, action in self.op_actions.items():
            action.setChecked(False)
        for v, action in self.op_actionsR.items():
            action.setChecked(False)
        # 勾选当前
        try:
            self.op_actions[self.window_opacity * 100].setChecked(True)
            self.op_actionsR[self.window_opacity * 100].setChecked(True)
        except KeyError:
            self.customization_op.setChecked(True)
            self.right_opacity_op.setChecked(True)

    # 左右键弹出托盘菜单
    def on_tray_activated(self, reason):
        # reason 是枚举类型 QSystemTrayIcon.ActivationReason
        if reason == QSystemTrayIcon.ActivationReason.Trigger or reason == QSystemTrayIcon.ActivationReason.Context:  # 左右键点击
            self.tray.contextMenu().popup(QCursor.pos() + QPoint(10, -80))  # 弹出右键菜单

    """窗口移动"""
    # 鼠标按下
    def mousePressEvent(self, event: QMouseEvent):
        # 鼠标左键按下时,记录初始位置
        if event.button() == Qt.MouseButton.LeftButton:
            self.ImageCahan()
            # 使用鼠标处于屏幕的绝对位置减去窗口左上角在窗口的绝对位置得到鼠标处于窗口内的的位置
            self.mouse_drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

            print("拖动")

        if event.button() == Qt.MouseButton.RightButton:
            self.menuRight.exec(QCursor.pos())

    # 鼠标移动
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_follow_mouse:
            # 使用鼠标处于屏幕的绝对位置减去上一次记录的相对位置,得到目标位置
            target_pos = event.globalPosition().toPoint() - self.mouse_drag_pos
            # 确保不超过左/上边
            target_x = max(target_pos.x(), 0 - (self.width() - self.label.width()))
            target_y = max(target_pos.y(), 0)
            target_x = min(target_x, self.screen_rect.width() - self.width())
            target_y = min(target_y, self.screen_rect.height() - self.height())

            self.move(QPoint(target_x, target_y))

            # 如果已启动就重置闲置计时器
            if self.randomLook_time.isActive():
                self.randomLook_time.start()

    # 鼠标松手
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.ImageEat()
            self.mouse_drag_pos = QPoint()

    """窗口穿透"""
    def set_window_hit_test_visible(self, visible: bool):
        """
        设置窗口是否可被鼠标点击  穿透/非穿透 
        :param visible: True=可点击  取消穿透 ，False=穿透  不可点击 
        """
        # 1. Qt层面设置鼠标事件透明
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, not visible)

        hwnd = self.winId()  # 获取窗口句柄
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        GWL_EXSTYLE = -20  # 修改窗口高级样式
        WS_EX_LAYERED = 0x00080000  # 透明效果
        WS_EX_TRANSPARENT = 0x00000020  # 鼠标 / 触摸事件穿透
        ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)  # 获取当前扩展样式
        # Windows API层面设置窗口穿透  仅Windows生效 
        if not visible:
            # 设置窗口扩展样式：WS_EX_LAYERED  分层窗口  + WS_EX_TRANSPARENT  穿透 
            new_ex_style = ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_ex_style)
        else:
            # 移除穿透样式
            new_ex_style = ex_style & ~WS_EX_TRANSPARENT
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_ex_style)
    def toggle_window_hit(self):
        """调整窗口穿透状态->托盘菜单"""
        # 读取当前是否开启了鼠标透明
        is_transparent = self.testAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        if is_transparent:
            # 取消穿透  可点击 
            self.set_window_hit_test_visible(True)
            self.test_bool = False   # 改变后
            self.tray_toggle_hit.setText("窗口穿透")
            print("调整窗口穿透 -> 关闭窗口穿透")
        else:
            # 开启穿透  不可点击 
            self.set_window_hit_test_visible(False)
            self.test_bool = True    # 改变后
            self.tray_toggle_hit.setText("关闭窗口穿透")
            print("调整窗口穿透 -> 窗口穿透")

    """窗口置顶"""
    def window_top(self, current_flags):
        """置顶状态改变"""
        self.setWindowFlags(current_flags ^ Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def toggle_window_top(self):
        """窗口置顶->托盘菜单"""
        # 开启窗口穿透时不能更改置顶状态
        if not self.test_bool:
            current_flags = self.windowFlags()
            self.window_top(current_flags)
            visible = current_flags & Qt.WindowType.WindowStaysOnTopHint != 0
            if not visible:
                # 置顶取消
                self.tray_top.setText("取消置顶")
                self.right_top.setText("取消置顶")
                print("调整置顶 -> 置顶")
            else:
                self.tray_top.setText("置顶")
                self.right_top.setText("置顶")
                print("调整置顶 -> 未置顶")
        else:
            print("开启窗口穿透时不能更改置顶状态!!!")
            # 需要在鼠标处弹窗,一秒后关闭

    """ 动画 """
    # 移动窗口
    def pikaMove(self):
        if not self.is_move:
            return

        if self.pos().x() >= self.screen_rect.right() - self.width():
            self.is_left = False
        if self.pos().x() <= self.screen_rect.left() - (self.width() -self.label.width()):
            self.is_left = True

        if self.is_left and self.is_move:
            # 右
            self.move(self.pos() + QPoint(5, 0))
        else:
            # 左
            self.move(self.pos() + QPoint(-5, 0))
            self.label.setMovie(self.movie_left)
        self.move_x += 5
        if self.max_move_x:
            if self.move_x >= self.max_move_x:
                self.move_x = 0
                self.ImageEat()
                self.move_time.stop()

    # 向左
    def RLeft(self):
        self.is_move = True
        self.is_left = False
        self.move_time.start()

        self.randomLook_time.stop()
        print("向左")

    # 回到默认图
    def to_initial_gif(self):
        self.initial_gifTime.stop()

        self.initial_time_number = 5
        self.initial_gifTime.setInterval(self.initial_time_number * 1000)

        if not self.randomLook_time.isActive():
            self.randomLook_time.start()

        movie = self.label.movie()
        # 因为移动处有回到默认,所以这里不需要
        if hasattr(movie, "name"):
            if movie.name == 'left' or movie.name == 'eat':
                return
        self.ImageEat()

    # 随机气泡
    def random_text(self)->str:

        current_movie = self.label.movie()

        if current_movie and hasattr(current_movie, "name"):
            name = current_movie.name
        else:
            name = "eat"

        while True:
            text = choice(self.dialog_texts.get(name, self.dialog_texts['eat']))
            if text != self.bubble_text.toPlainText():
                return text

    # 显示气泡
    def show_bubble(self):
        text = self.random_text()
        self.bubble_text.setText(f"{text}")
        self.bubble_bg.show()
        self.bubble_text.show()
        self.showBubble_time_number = randint(15, 35)
        print(f"随机气泡: {text} ({self.showBubble_time_number}秒后再次显示)")

        self.showBubble_time.setInterval(self.showBubble_time_number * 1000)
        self.showBubble_time.stop()
        if not self.hideBubble_time.isActive():
            self.hideBubble_time.start()
    # 隐藏气泡
    def hide_bubble(self):
        self.bubble_bg.hide()
        self.bubble_text.hide()
        if not self.showBubble_time.isActive():
            self.showBubble_time.start()
    
    # 随机一个表情
    def random_look(self):
        """
        随机一个表情,并设置相应的回到默认图的时长等属性 激活回到默认的计时器
        :return: 
        """
        function_list = [self.ImageEat, self.ImageLeft,
                         self.ImageSleep, self.ImageAngry,
                         self.ImageLiulei,
                    ]
        look_dict = {
            self.ImageEat.__name__: {
                "name": 'eat',
                "initial_time_number": None,
            },
            self.ImageLeft.__name__: {
                "name": 'left',
                "initial_time_number": None,
            },
            self.ImageSleep.__name__: {
                "name": 'sleep',
                "initial_time_number": 20,
            },
            self.ImageAngry.__name__: {
                "name": "angry",
                "initial_time_number": 8,
            },
            self.ImageLiulei.__name__: {
                "name": "liulei",
                "initial_time_number": 10,
            },
        }
        now_movie_name = self.label.movie()
        if hasattr(now_movie_name, "name"):
            name = now_movie_name.name
        else:
            name = "eat"

        while True:
            random_function = choice(function_list)
            ldict = look_dict.get(random_function.__name__, look_dict[self.ImageEat.__name__])
            random_name = ldict.get("name")
            if random_name != name:
                break


        l_time_num = ldict.get("initial_time_number", 5)
        # 如果有值就改变回到默认的时间并激活
        if l_time_num:
            self.initial_time_number:int = l_time_num
            self.initial_gifTime.setInterval(self.initial_time_number * 1000) # type: ignore
            # 激活回到原图的计时器
            self.initial_gifTime.start()
            print(f"{l_time_num}秒后回到原图的", end='')
        else:
            self.initial_gifTime.start()

        return random_function
    
    # 随机表情时更改当前气泡
    def change_bubble(self):
        text = self.bubble_text.toPlainText()
        movie = self.label.movie()
        if movie and hasattr(movie, "name"):
            name = movie.name
        else:
            name = "eat"
        
        bubble_list = self.dialog_texts.get(name, 'eat')
        if text in bubble_list:
            return
        else:
            self.show_bubble()
        
    # 随机表情
    def play_random_look(self):
        random_function = self.random_look()
        
        self.randomLook_time_number = randint(30, 60)
        print(f"随机表情: {random_function.__name__}({self.randomLook_time_number}秒后再次切换)")
        random_function()
        self.change_bubble()

        # 关闭随机计时(回到默认时激活)
        self.randomLook_time.setInterval(self.randomLook_time_number * 1000)
        self.randomLook_time.stop()


app = QApplication()
window = MainWindow()
window.show()
app.exec()
""" 随机切换后改变显示气泡 """