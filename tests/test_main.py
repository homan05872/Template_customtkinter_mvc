# Appクラスが定義されているモジュールをインポート
from src.main import App, main
from src.controllers import DiaryController
from src.windows import MainWindow
from src.models import DiaryModel
from src.style_manager import CommonStyle
from unittest.mock import MagicMock, patch
from src.pages import Page1, Page2
import customtkinter as ctk


# ***************************************************
# テスト関数
# ***************************************************
# Page1, Page2をモックに置き換えるテスト
def test_initialization_App(monkeypatch):
    """
    Appクラスのコンストラクタが正しく動作しているかテスト
    1. 各クラスがインスタンス化されている事
    2. page_setメソッドがコンストラクタ内で呼び出されている事
    """
    
    # ページクラスのモック
    mock_page_set = MagicMock()
    # monkeypatchを使ってpage_setメソッドをモックに置き換える
    monkeypatch.setattr('src.windows.MainWindow.page_set', mock_page_set)
    
    app = App()
    # DiaryModelがインスタンス化されているか確認
    assert isinstance(app.diary_model, DiaryModel)
    
    # コントローラ辞書が正しく設定されているか確認
    assert "diary" in app.main_controllers
    assert isinstance(app.main_controllers["diary"], DiaryController)
    
    # スタイルクラスがインスタンス化されているか確認
    assert isinstance(app.main_style, CommonStyle)
    
    # MainWindowが正しくインスタンス化されているか確認
    assert isinstance(app.main_window, MainWindow)
    
    # ページが正しく設定されているか確認
    # main_window.page_setが呼び出されたことを確認
    app.main_window.page_set.assert_called_once_with([Page1, Page2])
    
# runメソッドのテスト
def test_run_App(monkeypatch):
    """
    Appクラスのrunメソッドの実行をテスト
    1. show_pageとmock_mainloopメソッドが実行される事を確認
    """
    # モック化されたMainWindowのインスタンスを作成
    mock_show_page = MagicMock()
    mock_mainloop = MagicMock()
    
    monkeypatch.setattr(MainWindow, 'show_page', mock_show_page)
    monkeypatch.setattr(ctk.CTk, 'mainloop', mock_mainloop)
    
    # Appクラスのインスタンスを作成
    app = App()
    
    # runメソッドを呼び出し
    app.run()

    # show_pageが"Page1"で呼び出されたことを確認
    mock_show_page.assert_called_once_with("Page1")

    # mainloopが1回呼び出されたことを確認
    mock_mainloop.assert_called_once()
    
def test_main(monkeypatch):
    '''
    1. Appのインスタンスが生成されたことを確認
    2. Appのrunメソッドが呼ばれたことを確認 
    '''
    # MagicMockでAppクラスをモック化
    mock_app_class = MagicMock()
    mock_app_instance = MagicMock()

    # Appクラスのコンストラクタをモックに置き換え、モックインスタンスを返す
    mock_app_class.return_value = mock_app_instance
    monkeypatch.setattr('src.main.App', mock_app_class)

    # main関数を呼び出す
    main()

    # Appのインスタンスが生成されたことを確認
    mock_app_class.assert_called_once()

    # Appのrunメソッドが呼ばれたことを確認
    mock_app_instance.run.assert_called_once()