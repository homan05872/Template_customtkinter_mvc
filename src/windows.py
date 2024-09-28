import customtkinter as ctk
from typing import Any, Tuple
from abc import ABC

class BaseWindow(ctk.CTk, ABC):
    def __init__(self, controllers: dict[str, Any], style: Any, **kwargs):
        super().__init__(**kwargs)
        
        # 初期化
        self.theme = 'dark'                 # テーマカラー
        self.style = style                  # スタイルクラス
        self.controllers = controllers      # コントローラ群
        self.pages:dict[str] = {}           # ページのフレームを格納する辞書
        
        # テーマ設定
        self.bg_set(self.theme)
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        # Gridレイアウトの設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def show_page(self, page_name:str) -> None:
        '''ページ切替を行うメソッド'''
        page = self.pages[page_name]
        page.tkraise()
        
    def page_set(self, pages:Any):
        ''' Pageクラスの配置を行うメソッド '''
        # ページクラス配置
        for PageClass in pages:
            page_name = PageClass.__name__
            page = PageClass(master=self, **self.style.transparent_frame)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")
        
    def bg_set(self, theme:str):
        ''' 背景テーマを設定するメソッド '''
        ctk.set_appearance_mode(theme)  # Modes: system (default), light, dark
        self.style.change_transparent_frame(theme)

class MainWindow(BaseWindow):
    def __init__(self, controllers: dict[str, Any], style: Any, **kwargs) -> None:
        super().__init__(controllers, style, **kwargs)

        self.title("MVC with Page Navigation")
        self.geometry("500x400")