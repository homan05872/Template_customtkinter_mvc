from enum import Enum

FONT_TYPE = "meiryo"
BASE_COLOR_DARK = "#242424"

class FontSettings(Enum):
    HEADER_TITLE = (FONT_TYPE, 20, "bold")
    FRAME_TITLE = (FONT_TYPE, 17, "bold")
    DEFAULT = (FONT_TYPE, 15)
    MENU = (FONT_TYPE, 13)
    
class StyleManager:
    
    transparent_frame = {
        "fg_color": BASE_COLOR_DARK,
    }
    
    inline_btn = {
        "text_color": ("gray10", "#DCE4EE"),
        "fg_color": "transparent",
        "border_width":2,
    }