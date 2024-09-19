import tkinter as tk
from tkinter import Frame, Label, messagebox, Text
import ELYZA_client

class ChatApp:
    def init (self, root):
        self.root = root
        self.root.title('MAU Chat')
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

        self.ELYZA_clt = ELYZA_client.ELYZA_clt()

    def connect (self):
        self.ip_address = self.ip_entry.get()
        self.port_number = self.port_entry.get()
        if self.validate_ip (self.ip address) and self.validate_port (self.port number):
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
        self.chat_area.tag_configure ('MAU', Justify='left')

    def send_message (self): 
        message = self.message_entry.get()

        if message:
            # self.create_message_bubble ('You:' + message, 'You')
            # self.message_entry.delete (0, tk.END)

            #ボットの応答を生成
            #bot_response = self.get_bot_response (message)
            #self.create_message_bubble ('MAU:'+ bot_response, 'MAU')

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

    def create_message_bubble (self, message, sender):
        # bubble = Frame (self, chat_frame, bg="lightblue' if sender == 'user' else 'lightgreen', padx=10, pady=5)
        # label = Label (bubble, text=message, bg="lightblue" if sender == 'user' else lightgreer, anchor='w if sender == 'bot else 'e')
        # label.pack ()
        # bubble.pack (anchor='e' if sender == 'user' else 'w', pady=5)

        self.chat_area.config (state='normal')
        self.chat_area.insert (tk.END, message + '\n')
        self.chat_area.config (state='disabled')

        #最下部にスクロール
        self.chat_area.yview (tk.END)

    def get_bot_response (self, message):
        self.url='http://' + self.ip_address + ':' + self.port_number + '/Utterance'
        response = self.ELYZA_clt.response (self.url, message)

        return response

    def memorize (self):
        self.ELYZA_clt.memorize()

if __name__ == '__main__':
    root = tk.Tk()
    chat_app = ChatApp (root)
    root. mainloop ()
    print('end')
    #memory保持
    chat_app.memorize()