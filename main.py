import base64
import io
import os
import threading
from enum import nonmember
from socket import socket, AF_INET, SOCK_STREAM

from customtkinter import *
from tkinter import filedialog
from PIL import Image


class MainWindow(Frame):
    def __init__(self):
        super().__init__()

        self.geometry('400x300')
        self.title('Chat Client')

        self.username = 'Artem'


        self.Label = None
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu=False
        self.speed_animate_menu = -20
        self.btn = CTkButton(self, text='▶️', command=self.toogle_show_menu, width=30)
        self.btn.place(x=0, y=0)


        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.place(x=0, y=0)


        self.message_entry = CTkEntry(self, placeholder_text='Введить повідомлення', height=40 )
        self.message_entry.place(x=0, y=0)
        self.send_button = CTkButton(self, text='>', width=50, height=40, command=self.send_message)
        self.send_button.place(x=0, y=0)

        self.open_img_button = CTkButton(self, text='📂', width=50, height=40, command=self.open_image)
        self.open_img_button.place(x=0, y=0)

        self.adaptive_ui()

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 8080))
            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату!\n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитися до сервера: {e}")

