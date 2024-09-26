import tkinter as tk
from tkinter import Frame, Label, messagebox, Text
import threading
import importlib
import ELYZA_client

#exe化
#pyinstaller MAU_chat.py --onefile --noconsole --add-data "C:\work\win_py_Greeting\venv\Lib\site-packages\unstructured\nlp\english-words.txt;unstructured/nlp" --hidden-import ELYZA_client --optimize 1
#C:\Windows\System32\libomp140.x86_64.dllをMAU_chat.exeと同じフォルダにコピー

class ChatApp:
    def __init__ (self, root):
        self.root = root
        self.root.title('MAU Chat')

        #起動中の画面
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title('召喚')
        self.loading_window.attributes('-topmost', True)

        #起動中のウィンドウサイズを指定
        loading_width = 280
        loading_height = 280
        self.loading_window.geometry(f'{loading_width}x{loading_height}')

        #テキストラベルを追加
        self.loading_label = Label(self.loading_window, text = '召喚中．．．\n数分かかることがあります')
        self.loading_label.pack(expand=True)

        #スレッドを作成してELYZA_cltのインスタンスを作成
        threading.Thread(target=self.initialize_client).start()
    
    def initialize_client(self):
        #ELYZA_cltのインスタンスを作成
        self.ELYZA_clt = importlib.import_module('ELYZA_client').ELYZA_clt()

        #起動中の画面を閉じる
        self.loading_window.destroy()

        #GUIの初期化をメインスレッドで行う
        self.setup_gui()

    def setup_gui(self):
        #IPアドレス入力画面
        self.ip_frame = Frame (root)
        self.ip_frame.pack (pady=20)

        self.ip_label = Label (self.ip_frame, text='Enter IP Address:')
        self.ip_label.pack (side=tk.LEFT)

        self.ip_entry = tk.Entry (self.ip_frame, width=20)
        self.ip_entry.pack (side=tk.LEFT, padx=5)
        self.ip_entry.insert (0, '127.0.0.1')

        self.port_label = Label (self.ip_frame, text='Enter Port Number:')
        self.port_label.pack (side=tk.LEFT)

        self.port_entry = tk.Entry (self.ip_frame, width=5)
        self.port_entry.pack (side=tk.LEFT, padx=5)
        self.port_entry.insert (0, '8000')

        self.connect_button = tk.Button (self.ip_frame, text='Connect', command=self.connect)
        self.connect_button.pack (side=tk.LEFT)

    def connect (self):
        self.ip_address = self.ip_entry.get()
        self.port_number = self.port_entry.get()
        if self.validate_ip (self.ip_address) and self.validate_port (self.port_number):
            self.ip_frame.pack_forget()
            self.create_chat_interface ()
        else:
            messagebox.showerror ('Invalid Input', 'Please enter a valid IP address and port number')

    def validate_ip (self, ip):
        parts = ip.split('.')
        if len (parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not (0 <= int (part) <= 255):
                return False
        return True

    def validate_port (self, port):
        if port.isdigit() and 0 <= int (port) <= 65535:
            return True
        return False

    def create_chat_interface (self):
        #チャット表示エリア
        self.chat_frame = Frame (self.root)
        self.chat_frame.pack (pady=10)

        #画像を読み込む
        self.chat_image = tk.PhotoImage(file='mau.png')
        self.image_label = Label(self.chat_frame, image=self.chat_image)
        self.image_label.pack()

        #Text ウィジェットを使用してチャット表示エリアを作成
        self.chat_area = Text (self.chat_frame, wrap=tk.WORD, height=15, width=50, state='disabled')

        self.chat_area.pack ()

        #フレームを作成してメッセージ入力エリアと送信ボタンを配置
        self.input_frame = Frame (self.root)
        self.input_frame.pack (pady=10)

        #メッセージ入力エリア
        self.message_entry = tk.Entry (self.input_frame, width=40)
        self.message_entry.pack (side=tk.LEFT, padx=5)

        #送信ボタン
        self.send_button = tk.Button (self.input_frame, text='Send', command=self.send_message)
        self.send_button.pack (side=tk.LEFT)

        self.chat_area.tag_configure ('You', justify='right')
        self.chat_area.tag_configure ('MAU', justify='left')

    def send_message (self): 
        message = self.message_entry.get()

        if message:
            self.chat_area.config (state='normal')
            self.chat_area.insert (tk.END, f'You: {message} \n\n', 'You')
            self.chat_area.config (state='disabled')
            self.message_entry.delete (0, tk.END)

            #ボットの応答を生成
            bot_response = self.get_bot_response (message)
            self.chat_area.config (state='normal')
            self.chat_area.insert (tk.END, f'MAU: {bot_response} \n\n', 'MAU')
            self.chat_area. config (state='disabled')

            #最下部にスクロール
            self.chat_area.yview (tk.END)

    def create_message_bubble (self, message):
        self.chat_area.config (state='normal')
        self.chat_area.insert (tk.END, message + '\n')
        self.chat_area.config (state='disabled')

        #最下部にスクロール
        self.chat_area.yview (tk.END)

    def get_bot_response (self, message):
        self.url='http://' + self.ip_address + ':' + self.port_number + '/Utterance'
        response = self.ELYZA_clt.response (self.url, message)

        return response

if __name__ == '__main__':
    root = tk.Tk()
    chat_app = ChatApp (root)
    root. mainloop ()
    print('end')
