import pytest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
from src.pages import Page1, Page2  # Page1とPage2のインポートを適宜調整してください。

@pytest.fixture
def mock_master():
    """Mocked master object for tests."""
    mock_master = ctk.CTk()
    mock_style = MagicMock()
    mock_master.style = mock_style
    mock_show_page = MagicMock()
    mock_master.show_page = mock_show_page
    # コントローラを持つモックを設定
    mock_master.controllers = {
        'diary': MagicMock()  # diaryコントローラのモックを追加
    }
    return mock_master

@pytest.fixture
def page1(mock_master):
    """Fixture for Page1."""
    with patch('customtkinter.CTkLabel'), patch('customtkinter.CTkButton'):
        return Page1(master=mock_master)

@pytest.fixture
def page2(mock_master):
    """Fixture for Page2."""
    with patch('customtkinter.CTkLabel'), patch('customtkinter.CTkButton'), patch('customtkinter.CTkEntry'):
        return Page2(master=mock_master)

def test_page1_build_ui(page1):
    assert hasattr(page1, 'label')
    assert hasattr(page1, 'page_btn')
    assert hasattr(page1, 'msg_btn')

def test_page1_show_page(page1, mock_master):
    page1.show_page('Page2')
    mock_master.show_page.assert_called_once_with('Page2')

@patch('tkinter.messagebox.showinfo')
def test_page1_msg_output(mock_showinfo, page1):
    page1.diary_controller.get_list_data = MagicMock(return_value="Test data")
    page1.msg_output(1)
    mock_showinfo.assert_called_once_with("Information", "ページ1のメッセージです。\n\nDiaryデータ：\nTest data")

def test_page2_build_ui(page2):
    assert hasattr(page2, 'label')
    assert hasattr(page2, 'get_label')
    assert hasattr(page2, 'get_input')
    assert hasattr(page2, 'page_btn')
    assert hasattr(page2, 'msg_btn')

@patch('tkinter.messagebox.showinfo')
def test_page2_msg_output_with_valid_id(mock_showinfo, page2):
    page2.get_input.get = MagicMock(return_value="1")
    page2.diary_controller.get_one = MagicMock(return_value="Diary entry 1")
    page2.msg_output(2)
    mock_showinfo.assert_called_once_with("Information", "ページ2のメッセージです。\n\nDiaryデータ：\nDiary entry 1")

@patch('tkinter.messagebox.showinfo')
def test_page2_msg_output_with_empty_id(mock_showinfo, page2):
    page2.get_input.get = MagicMock(return_value="")
    page2.msg_output(2)
    assert hasattr(page2, 'error_label')  # エラーメッセージが表示されたか確認