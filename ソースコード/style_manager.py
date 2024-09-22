from enum import Enum

FONT_TYPE = "meiryo"
BASE_COLOR_DARK = "#242424"
BASE_COLOR_LIGHT = "#DBDBDB"

class CommonStyle:
    ''' 共通のスタイルを定義するクラス '''
    def __init__(self) -> None:
        # 文字フォント設定
        self.HEADER_TITLE = (FONT_TYPE, 20, "bold")
        self.FRAME_TITLE = (FONT_TYPE, 17, "bold")
        self.DEFAULT = (FONT_TYPE, 15)
        
        # Windowの背景色
        self.transparent_frame = {
            "fg_color": BASE_COLOR_DARK,
        }
        
        # インラインボタン
        self.inline_btn = {
            "text_color": ("gray10", "#DCE4EE"),
            "fg_color": "transparent",
            "border_width":2,
        }
        
    def change_transparent_frame(self, theme:str):
        if theme == 'dark':
            self.transparent_frame["fg_color"] = BASE_COLOR_DARK
        elif theme == 'light':
            self.transparent_frame["fg_color"] = BASE_COLOR_LIGHT
        elif theme == 'system':
            self.transparent_frame["fg_color"] = BASE_COLOR_LIGHT