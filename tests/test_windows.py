import pytest
import customtkinter as ctk 
from unittest.mock import MagicMock, patch
from src.windows import MainWindow,BaseWindow  # クラスがあるモジュールをインポート


# ***************************************************
# セットアップ関数
# ***************************************************
@pytest.fixture
def get_ins():
    '''
    MainWidnowクラスのインスタンス生成の引数に必要なインスタンスをモック化
    '''
    # モックのスタイルとコントローラを用意
    mock_style = MagicMock()
    # mock_style.transparent_frame = {"bg_color": "white"}
    mock_style.change_transparent_frame = MagicMock()
    mock_controllers = {"controller1": MagicMock()}
    
    return mock_style, mock_controllers


# ***************************************************
# テスト関数
# ***************************************************
# テスト関数にget_window fixtureを渡す
def test_initialization_BaseWindow(get_ins, monkeypatch):
    '''
    MainWidnowクラスの__init__メソッドテスト
    1. インスタンス変数の初期ができているかの確認
    2. BaseWindowクラス内で各メソッドが呼び出されていることを確認
    '''
    # MainWindowの引数に必要なモック取得
    mock_style, mock_controllers = get_ins
    
    # MainWindowクラス内で呼び出されているメソッドのモック作成
    mock_bg_set = MagicMock()
    mock_set_default_color_theme = MagicMock()
    mock_grid_rowconfigure = MagicMock()
    mock_grid_columnconfigure = MagicMock()
    
    monkeypatch.setattr(MainWindow, 'bg_set', mock_bg_set)
    monkeypatch.setattr(ctk, 'set_default_color_theme', mock_set_default_color_theme)
    monkeypatch.setattr(ctk.CTk, 'grid_rowconfigure', mock_grid_rowconfigure)
    monkeypatch.setattr(ctk.CTk, 'grid_columnconfigure', mock_grid_columnconfigure)
    
    # ウィンドウのインスタンスを生成
    window = MainWindow(controllers=mock_controllers, style=mock_style)
    
    # 初期化されているかを確認
    assert window.theme == 'dark'
    assert window.controllers == mock_controllers
    assert window.pages == {}
    assert window.style == mock_style
    
    # 各メソッドが呼び出されていることを確認
    mock_bg_set.assert_called_with(window.theme)
    mock_set_default_color_theme.assert_called_with('blue')
    mock_grid_rowconfigure.assert_called_once_with(0, weight=1)
    mock_grid_columnconfigure.assert_called_once_with(0, weight=1)
    

def test_show_page_BaseWindow(get_ins):
    '''
    show_pageメソッド実行時、tkraiseメソッドに指定のページクラスが渡されるテスト
    '''
    # MainWindowの引数に必要なモック取得
    mock_style, mock_controllers = get_ins
    # ウィンドウのインスタンスを生成
    window = MainWindow(controllers=mock_controllers, style=mock_style)

    # ページモックを用意
    mock_page = MagicMock()
    window.pages = {"TestPage": mock_page}

    # ページ表示メソッドを実行
    window.show_page("TestPage")

    # ページのtkraiseが呼ばれているか確認
    mock_page.tkraise.assert_called_once()

def test_page_set_BaseWindow(get_ins):
    '''
    page_setメソッドによって下記が実現できていることを確認
    1. 引数のページクラスのインスタンス生成をしていることを確認
    2. インタンスへ変数(pages)に設定されたページクラスが追加されていることを確認
    3. ページクラスがgridメソッドで配置されていることを確認
    '''
    # MainWindowの引数に必要なモック取得
    mock_style, mock_controllers = get_ins
    # ウィンドウのインスタンスを生成
    window = MainWindow(controllers=mock_controllers, style=mock_style)

    # ページクラスのモック
    mock_page_class1 = MagicMock()
    mock_page_class1.__name__ = "TestPage1"
    mock_page_class2 = MagicMock()
    mock_page_class2.__name__ = "TestPage2"

    # ページをセット
    window.page_set([mock_page_class1,mock_page_class2])

    # ページクラスのインスタンス生成されていることを確認
    mock_page_class1.assert_called_once_with(master=window, **mock_style.transparent_frame)
    mock_page_class2.assert_called_once_with(master=window, **mock_style.transparent_frame)
    # インタンスへ変数(pages)に設定されたページクラスが追加されていることを確認
    assert "TestPage1" in window.pages
    assert "TestPage2" in window.pages
    # ページクラスがgridメソッドで配置されていることを確認
    window.pages["TestPage1"].grid.assert_called_once_with(row=0, column=0, sticky="nsew")
    window.pages["TestPage2"].grid.assert_called_once_with(row=0, column=0, sticky="nsew")

def test_bg_set_BaseWindow(get_ins):
    # MainWindowの引数に必要なモック取得
    mock_style, mock_controllers = get_ins
    # ウィンドウのインスタンスを生成
    window = MainWindow(controllers=mock_controllers, style=mock_style)

    # テーマ変更をテスト
    with patch('customtkinter.set_appearance_mode') as mock_set_appearance_mode:
        window.bg_set("light")

        # テーマが設定されているか確認
        mock_set_appearance_mode.assert_called_once_with("light")
        mock_style.change_transparent_frame.assert_called_with("light")


def test_initialization_MainWindow(get_ins, monkeypatch):
    
    # MainWindowの引数に必要なモック取得
    mock_style, mock_controllers = get_ins
    
    # MainWindowクラス内で呼び出されているメソッドのモック作成
    mock__init__ = MagicMock()
    mock_geometry = MagicMock()
    mock_title = MagicMock()
    
    # MainWindowの__init__で呼び出し
    monkeypatch.setattr(BaseWindow, '__init__', mock__init__)
    monkeypatch.setattr(ctk.CTk, 'title', mock_title)
    monkeypatch.setattr(ctk.CTk, 'geometry', mock_geometry)
    
    # ウィンドウのインスタンスを生成
    window = MainWindow(controllers=mock_controllers, style=mock_style)
    
    # titleメソッドが呼ばれているかを確認
    mock__init__.assert_called_with(mock_controllers, mock_style, **{})
    mock_title.assert_called_with("MVC with Page Navigation")
    # geometryメソッドが呼ばれているかを確認
    mock_geometry.assert_called_with("500x400")