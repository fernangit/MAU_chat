import psutil
import time
import tkinter as tk
import threading
from PIL import Image, ImageTk
from screeninfo import get_monitors
import queue

class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path, width=None, height=NotImplemented):
        super().__init__(master)
        self.gif = Image.open(gif_path)
        self.frames = []
        self.width = width
        self.height = height

        #GIFの各フレームを読み込み、リサイズ
        try:
            while True:
                frame = self.gif.copy()
                if self.width and self.height:
                    frame = frame.resize((self.width, self.height), Image.LANCZOS)
                    self.frames.append(ImageTk.PhotoImage(frame))
                    self.gif.seek(len(self.frames))
        except EOFError:
            pass #GIFの最後に達したら終了

        self.current_frame = 0
        self.display_frame()

    def display_frame(self):
        # 現在のフレームを表示
        self.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames) #次のフレームに移動
        self.after(80, self.display_frame) #80ms後に次のフレームを表示

def display_gif(q, gif_path, width=None, height=None, x=None, y=None):
    root = tk.Tk()
    root.title("Animated GIF Viewer")
    root.overrideredirect(True) #ヘッダーを非表示にする

    # ウィンドウのサイズと位置を指定
    if width and height:
        root.geometry(f"{width}x{height}+{x}+{y}")   #幅、高さ、X座標、Y座標を指定

    animated_gif = AnimatedGIF(root, gif_path, width, height)
    animated_gif.pack()

    def check_queue():
        try:
            message = q.get_nowait()
            if message == "quit":
                root.quit()
        except queue.Empty:
            pass
        root.after(100, check_queue) #100ms毎にキューをチェック

    check_queue()
    root.mainloop()
    
def get_monitor_center():
    monitors = get_monitors()
    for monitor in monitors:
        center_x = monitor.x + monitor.width // 2
        center_y = monitor.y + monitor.height // 2

    return center_x, center_y

def display_splash(q):
    # GIFファイルのパスを指定
    gif_file_path = "MAUChat_splash.gif"
    center_x, center_y = get_monitor_center()
    display_gif(q, gif_file_path, width=300, height=300, x=center_x, y=center_y)    # 幅300px、高さ300pxに設定

def watch_process(procname):
    while True:
        proccnt = 0
        for proc in psutil.process_iter():
            try:
                #proc.name()でプロセスの名前を取得
                if procname == proc.name():
                    proccnt += 1
                    info = {"pid":proc.pid, "name":proc.name(), "status":proc.status()}
                    print(f"Process {proc.name()}:{info}")
                    if proccnt >= 2:
                        print("2つのプロセスが見つかりました")
                        return # watch_processを終了
            except (AttributeError, Exception):
                continue
        time.sleep(5)

# tkinterのウィンドウを作成
q = queue.Queue()
popup_thread = threading.Thread(target=display_splash, args=(q,))
popup_thread.start()

# # プロセス監視を実行
# watch_process("MAU_chat_newGUI.exe")

# # tkinterのメインループを終了
# time.sleep(30) # 30秒待機
# q.put("quit") # メインスレッドから終了要求を送信
# # ポップアップスレッドが終了するのを待つ
# popup_thread.join()
# print("プログラムを終了します")