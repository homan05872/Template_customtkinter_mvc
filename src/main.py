from controllers import DiaryController
from windows import MainWindow
from models import DiaryModel
from pages import Page1, Page2
from style_manager import CommonStyle

def main() -> None:
    # 各クラスのインスタンス生成
    app = App()
    # アプリ起動
    app.run()
    
class App:
    def __init__(self) -> None:
        ''' 各クラスの連携(インスタンス生成) '''
        # モデルクラス群を生成
        self.diary_model = DiaryModel()
        
        # コントローラクラス群の辞書型定義
        self.main_controllers={
            "diary": DiaryController(self.diary_model),
        }
        # スタイルクラス群を生成
        self.main_style=CommonStyle()     # MainWindowクラスで使用
        
        # ウィンドウクラスにコントローラークラス群を渡す
        self.main_window = MainWindow(self.main_controllers, self.main_style)
        
        # ページクラス配置
        self.main_window.page_set([Page1, Page2])      # ← 配置したいPageクラスを配列で渡す
        
    def run(self) -> None:
        ''' アプリ起動処理 '''
        self.main_window.show_page("Page1") # 最初に表示したいページクラス名を渡す
        self.main_window.mainloop()         # 起動

if __name__ == "__main__":
    main()