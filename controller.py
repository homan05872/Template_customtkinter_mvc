import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from model import AppModel
from views import Page1, Page2
from style_manager import StyleManager

class AppController(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MVC with Page Navigation")
        self.geometry("1000x550")
        
        # テーマ設定
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        # モデルの生成　※データはこのself.modelから取得できるようにする。
        self.model = AppModel()
        
        # Gridレイアウトの設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 全ページのフレームを格納する辞書
        self.frames = {}

        # 各ページの作成と格納
        for F in (Page1, Page2):
            page_name = F.__name__
            frame = F(master=self, controller=self, **StyleManager.transparent_frame)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 起動時にPage1Frameを表示する。
        self.show_frame("Page1")

    def show_frame(self, page_name:str):
        '''ページ切替を行うメソッド'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def msg_output(self, page_num:int):
        '''メッセージを出力するメソッド'''
        data:str = self.model.data
        messagebox.showinfo("Information", f"ページ{page_num}のメッセージです。\n"
                                            + f"モデルから受け取ったデータ:{data}")
