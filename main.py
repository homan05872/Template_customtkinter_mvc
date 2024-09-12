from controllers import DiaryController
from windows import MainWindow
from models import DiaryModel
from pages import Page1, Page2
from style_manager import MainStyle

def main() -> None:
    # モデルクラス群を生成
    diary_model = DiaryModel()
    
    # コントローラクラス群の辞書型定義
    main_controllers={
        "diary": DiaryController(diary_model),
    }
    # スタイルクラス群の辞書型定義
    main_styles={
        "main": MainStyle(),
    }
    
    # ビュークラスにページクラス群とコントローラークラス群を渡す
    main_window = MainWindow(main_controllers, main_styles)
    
    # ページクラス配置
    for PageClass in [Page1, Page2]:
        page_name = PageClass.__name__
        page = PageClass(master=main_window, **main_styles['main'].transparent_frame)
        main_window.pages[page_name] = page
        page.grid(row=0, column=0, sticky="nsew")
    
    # アプリケーション開始
    main_window.show_page("Page1") # 最初に表示したいページクラス名を渡す
    main_window.mainloop()

if __name__ == "__main__":
    main()