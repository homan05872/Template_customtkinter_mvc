import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class BasePage(ctk.CTkFrame, ABC):
    def __init__(self, master:ctk.CTk|tk.Tk, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.style = self.master.style
    
    @abstractmethod
    def build_ui(self) -> None:
        """UIを構築するための抽象メソッド"""
        ...
    
    def show_page(self, page_name:str) -> None:
        '''ページ遷移するメソッド'''
        self.master.show_page(page_name)
        
class Page1(BasePage):
    def __init__(self, master:ctk.CTk, **kwargs) -> None:
        super().__init__(master, **kwargs)
        # コントローラ設定
        self.diary_controller = self.master.controllers['diary']
        # UI生成
        self.build_ui()
        
    def build_ui(self) -> None:
        '''UI生成するメソッド'''
        # Gridレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.label = ctk.CTkLabel(self, text="ページ１です。")
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.page_btn = ctk.CTkButton(self, text="ページ２へ", command=lambda: self.show_page("Page2"))
        self.page_btn.grid(row=1, column=0, padx=20, pady=40)
        
        self.msg_btn = ctk.CTkButton(self, text="メッセージ表示", command=lambda: self.msg_output(1), **self.style.inline_btn)
        self.msg_btn.grid(row=1, column=1, padx=(0,20), pady=40)
        
    def msg_output(self, page_num:int) -> None:
        '''メッセージを出力するメソッド'''
        data:str = self.diary_controller.get_list_data()
        messagebox.showinfo("Information", f"ページ{page_num}のメッセージです。\n\n"
                            + "Diaryデータ：\n"
                            + f"{data}")

class Page2(BasePage):
    def __init__(self, master:ctk.CTk, **kwargs) -> None:
        super().__init__(master, **kwargs)
        # コントローラ設定
        self.diary_controller = master.controllers['diary']
        # 入力検証用のコマンドを登録　※バリデーションはself.registerを使用して関数登録して使用する必要がある
        self.validate_cmd = self.register(self.validate_numeric_input)
        # UI生成
        self.build_ui()
        
    def build_ui(self) -> None:
        '''UI生成するメソッド'''
        # Gridレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        
        self.label = ctk.CTkLabel(self, text="ページ２です。")
        self.label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # idでレコードデータを取得するためのもの
        self.get_label = ctk.CTkLabel(self, text="idを入力してください")
        self.get_label.grid(row=1, column=0, columnspan=2)
        self.get_input = ctk.CTkEntry(self)
        self.get_input.configure(validate="key", validatecommand=(self.validate_cmd, "%S"))
        self.get_input.grid(row=2, column=0, columnspan=2)

        self.page_btn = ctk.CTkButton(self, text="ページ１へ", command=lambda: self.show_page("Page1"))
        self.page_btn.grid(row=4, column=0, padx=20, pady=40)
        
        self.msg_btn = ctk.CTkButton(self, text="idでデータ取得", command=lambda: self.msg_output(2), **self.style.inline_btn)
        self.msg_btn.grid(row=4, column=1, padx=(0,20), pady=40)
        
    def msg_output(self, page_num:int) -> None:
        '''メッセージを出力するメソッド'''
        id = self.get_input.get()
        if not id:
            self.error_label = ctk.CTkLabel(self, text="※idを入力してください。", text_color="red")
            self.error_label.grid(row=3, column=0, columnspan=2)
        else:
            data:str = self.diary_controller.get_one(id)
            if not data:
                data = '指定idのデータはありません。'
                
            messagebox.showinfo("Information", f"ページ{page_num}のメッセージです。\n\n"
                                + "Diaryデータ：\n"
                                + f"{data}")
        
        
    def validate_numeric_input(self, char: str) -> str:
        """入力を数字のみに制限するメソッド"""
        return "true" if char.isdigit() or char == "" else "false"