import customtkinter as ctk
from style_manager import StyleManager
from typing import Any
        
class MainView(ctk.CTk):
    def __init__(self, pages, controllers: dict[str, Any]) -> None:
        super().__init__()
        
        # テーマ設定
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        # Gridレイアウトの設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("MVC with Page Navigation")
        self.geometry("1000x550")
        
        # ページのフレームを格納する辞書
        self.pages:dict[str] = {}

        # 各ページの作成と格納
        for PageClass in pages:
            page_name = PageClass.__name__
            page = PageClass(master=self, controllers=controllers, **StyleManager.transparent_frame)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")
    
    def show_page(self, page_name:str) -> None:
        '''ページ切替を行うメソッド'''
        page = self.pages[page_name]
        page.tkraise()