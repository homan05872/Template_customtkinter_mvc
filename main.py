from controllers import DiaryController
from views import MainView
from models import DiaryModel
from pages import Page1, Page2

def main():
    # モデルを生成
    diary_model = DiaryModel()
    
    # コントローラーを生成
    diary_controller = DiaryController(diary_model)
    
    # ビューにページとコントローラーを設定　※MainViewに関連するすべてのコントローラを渡す
    main_view = MainView(pages=[Page1, Page2], controllers={
        "diary": diary_controller,
    })
    
    # アプリケーション開始
    main_view.show_page("Page1") # 最初に表示したいページを表示
    main_view.mainloop()

if __name__ == "__main__":
    main()