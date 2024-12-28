import tkinter as tk
from tkinter import Frame
import customtkinter as ctk
#import threading
from PIL import Image, ImageTk, ImageSequence
import ELYZA_client
import killProcess

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title('MAU Chat')
        self.root.geometry("300x500")

        self.show_loading_screen()
        # threading.Thread(target=self.initialize_client).start()
        self.initialize_client()
        self.resize_timer = None

        # スプラッシュ画面の終了
        killProcess.kill("watchProcess.exe")

    def show_loading_screen(self):
        """起動中の画面を表示"""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title('召喚')
        self.loading_window.attributes('-topmost', True)
        self.loading_window.geometry('280x280')

        self.loading_label = tk.Label(self.loading_window, text='召喚中．．．\n数分かかることがあります')
        self.loading_label.pack(expand=True)

    def initialize_client(self):
        """ELYZA_cltのインスタンスを作成"""
        self.ELYZA_clt = ELYZA_client.ELYZA_clt()
        self.loading_window.destroy()
        self.setup_gui()

    def setup_gui(self):
        """GUIの初期設定"""
        self.create_ip_entry_frame()

    def create_ip_entry_frame(self):
        """IPアドレスとポート番号の入力フレームを作成"""
        self.ip_frame = ctk.CTkFrame(self.root)
        self.ip_frame.pack(pady=20)

        self.ip_entry = self.create_label_and_entry(self.ip_frame, 'IP Address:', '127.0.0.1', width=80)
        self.port_entry = self.create_label_and_entry(self.ip_frame, 'Port Number:', '8000', width=40)

        self.connect_button = ctk.CTkButton(self.ip_frame, text='Connect', command=self.connect, font=('Helvetica', 10))
        self.connect_button.pack(side=tk.LEFT)

    def create_label_and_entry(self, parent, label_text, default_text, width):
        """ラベルとエントリを作成"""
        label = ctk.CTkLabel(parent, text=label_text, font=('Helvetica', 10))
        label.pack(side=tk.LEFT)
        entry = ctk.CTkEntry(parent, width=width, font=('Helvetica', 10))
        entry.pack(side=tk.LEFT, padx=5)
        entry.insert(0, default_text)
        return entry

    def connect(self):
        """IPアドレスとポート番号のバリデーションを行い、チャットインターフェースを作成"""
        self.ip_address = self.ip_entry.get()
        self.port_number = self.port_entry.get()
        if self.validate_ip(self.ip_address) and self.validate_port(self.port_number):
            self.ip_frame.pack_forget()
            self.create_chat_interface()
        else:
            tk.messagebox.showerror('Invalid Input', 'Please enter a valid IP address and port number')

    def validate_ip(self, ip):
        """IPアドレスのバリデーション"""
        parts = ip.split('.')
        return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

    def validate_port(self, port):
        """ポート番号のバリデーション"""
        return port.isdigit() and 0 <= int(port) <= 65535

    def create_chat_interface(self):
        """チャットインターフェースを作成"""
        self.create_gif_display()
        self.create_chat_display()
        self.create_entry_frame()
        self.setup_grid_weights()

    def create_gif_display(self):
        """GIF表示エリアを作成"""
        self.gif_frame = Frame(self.root)
        self.gif_frame.grid(row=0, column=0, pady=10)

        self.frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open('Mau.gif'))]
        self.image_label = tk.Label(self.gif_frame, bg="#2B2B2B")
        self.image_label.pack(pady=10)
        self.update_frame(0)

    def create_chat_display(self):
        """チャット表示エリアを作成"""
        self.chat_canvas = tk.Canvas(self.root, bg="#2B2B2B")
        self.chat_frame = ctk.CTkFrame(self.chat_canvas, fg_color="#2B2B2B")
        self.scrollbar = ctk.CTkScrollbar(self.root, command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas_frame_id = self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor='nw', width=self.root.winfo_width())
        self.chat_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.chat_frame.bind("<Configure>", self.on_frame_configure)
        self.root.bind("<Configure>", self.on_root_resize)

        self.sender_labels = []
        self.receiver_labels = []

    def create_entry_frame(self):
        """ユーザの入力フィールドと送信ボタンのフレームを作成"""
        self.entry_frame = ctk.CTkFrame(self.root)
        self.entry_frame.grid(row=2, column=0, sticky="ew")

        self.user_entry = ctk.CTkEntry(self.entry_frame, width=200)
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        self.user_entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10))

        self.user_entry.focus_set()

    def setup_grid_weights(self):
        """行と列の重みを設定"""
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def update_frame(self, idx):
        """GIFフレームを更新"""
        frame = self.frames[idx]
        self.image_label.configure(image=frame)
        idx = (idx + 1) % len(self.frames)
        self.root.after(80, self.update_frame, idx)

    def on_mousewheel(self, event):
        """マウスホイールでキャンバスをスクロール"""
        self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self, event):
        """キャンバスのスクロール領域を更新"""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.itemconfig(self.canvas_frame_id, width=event.width)

    def on_root_resize(self, event):
        """ウィンドウリサイズ時の処理"""
        if self.resize_timer is not None:
            self.root.after_cancel(self.resize_timer)
        self.resize_timer = self.root.after(100, self.configure_canvas_and_update_labels)

    def configure_canvas_and_update_labels(self):
        """キャンバスの幅とラベルの折り返し長さを更新"""
        self.configure_canvas_width()
        self.update_label_wraplength()

    def configure_canvas_width(self, event=None):
        """キャンバスの幅を設定"""
        current_width = self.root.winfo_width()
        self.chat_canvas.itemconfig(self.canvas_frame_id, width=current_width)

    def update_label_wraplength(self):
        """ラベルの折り返し長さを更新"""
        wraplength = self.root.winfo_width() - 200
        for label in self.sender_labels + self.receiver_labels:
            label.configure(wraplength=wraplength, anchor=ctk.W, justify='left')

    def send_message(self, event=None):
        """メッセージを送信"""
        user_text = self.user_entry.get()
        if user_text.strip():
            self.display_message(user_text, 'あなた', self.sender_labels, 'e', "#0a84ff")
            bot_response = self.get_bot_response(user_text)
            self.display_message(bot_response, 'まう', self.receiver_labels, 'w', "#30d158")
            self.chat_canvas.update_idletasks()
            self.chat_canvas.yview_moveto(1)
            self.user_entry.delete(0, tk.END)

    def display_message(self, message, sender, label_list, anchor, color):
        """メッセージを表示"""
        frame = ctk.CTkFrame(self.chat_frame, corner_radius=10)
        frame.pack(padx=10, pady=2, anchor=anchor)
        label = ctk.CTkLabel(frame, text=f'{sender}: {message}', fg_color=color, text_color="white",
                             justify='left', anchor=ctk.W, corner_radius=10, wraplength=self.root.winfo_width() - 200)
        label.pack(padx=10, pady=5)
        label_list.append(label)

    def get_bot_response(self, message):
        """ボットの応答を取得"""
        self.url = 'http://' + self.ip_address + ':' + self.port_number + '/Utterance'
        response = self.ELYZA_clt.response(self.url, message)
        return response

if __name__ == '__main__':
    root = ctk.CTk()
    chat_app = ChatApp(root)
    root.mainloop()
    print('end')
