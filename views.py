import customtkinter as ctk
import tkinter as tk

from typing import Any

class Page(ctk.CTkFrame):
    def __init__(self, master:ctk.CTk|tk.Tk, controller:Any, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
class Page1(Page):
    def __init__(self, master:ctk.CTk, controller:Any, **kwargs):
        super().__init__(master, controller, **kwargs)

        # Gridレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.label = ctk.CTkLabel(self, text="ページ１です。")
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.page_btn = ctk.CTkButton(self, text="ページ２へ", command=lambda: controller.show_frame("Page2"))
        self.page_btn.grid(row=1, column=0, padx=20)
        
        self.msg_btn = ctk.CTkButton(self, text="メッセージ表示", command=lambda: controller.msg_output(1))
        self.msg_btn.grid(row=1, column=1, padx=(0,20))

class Page2(Page):
    def __init__(self, master:ctk.CTk, controller:Any, **kwargs):
        super().__init__(master, controller, **kwargs)

        # Gridレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        
        self.label = ctk.CTkLabel(self, text="ページ２です。")
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.page_btn = ctk.CTkButton(self, text="ページ１へ", command=lambda: controller.show_frame("Page1"))
        self.page_btn.grid(row=1, column=0, padx=20)
        
        self.msg_btn = ctk.CTkButton(self, text="メッセージ表示", command=lambda: controller.msg_output(2))
        self.msg_btn.grid(row=1, column=1, padx=(0,20))
