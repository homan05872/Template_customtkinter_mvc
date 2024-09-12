from enum import Enum

FONT_TYPE = "meiryo"
BASE_COLOR_DARK = "#242424"

class MainStyle:
    def __init__(self) -> None:
        # 文字フォント設定
        self.HEADER_TITLE = (FONT_TYPE, 20, "bold")
        self.FRAME_TITLE = (FONT_TYPE, 17, "bold")
        self.DEFAULT = (FONT_TYPE, 15)
        self.MENU = (FONT_TYPE, 13)    
        # ウィジットデザイン設定
        self.transparent_frame = {
            "fg_color": BASE_COLOR_DARK,
        }
        
        self.inline_btn = {
            "text_color": ("gray10", "#DCE4EE"),
            "fg_color": "transparent",
            "border_width":2,
        }