import customtkinter as ctk
from typing import Any
        
class MainWindow(ctk.CTk):
    def __init__(self, controllers: dict[str, Any], styles: dict[str, Any]) -> None:
        super().__init__()
        
        # 初期化
        self.controllers = controllers
        self.styles = styles
        
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
    
    def show_page(self, page_name:str) -> None:
        '''ページ切替を行うメソッド'''
        page = self.pages[page_name]
        page.tkraise()