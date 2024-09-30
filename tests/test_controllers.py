import pytest

# DiaryControllerクラスのインポート
from src.controllers import DiaryController

# ***************************************************
# モッククラス
# ***************************************************
class MockDiaryModel:
    '''テスト用のDiaryModelモッククラス'''
    def get_all(self):
        '''get_allのモックメソッド'''
        return [
            {'id': 1, 'title': '日記1', 'content': '内容1', 'create_at': '2024-09-01 10:00'},
            {'id': 2, 'title': '日記2', 'content': '内容2', 'create_at': '2024-09-02 11:00'}
        ]
        
    def get_one(self, id:int):
        '''get_oneのモックメソッド'''
        if id == 1:
            return {'id': 1, 'title': '日記1', 'content': '内容1', 'create_at': '2024-09-01 10:00'}
        elif id == 2:
            return {'id': 2, 'title': '日記2', 'content': '内容2', 'create_at': '2024-09-02 11:00'}
        else:
            return None
        

# ***************************************************
# テスト関数
# ***************************************************
def test_diary_controller_init():
    '''DiaryControllerの__init__メソッドのテスト'''
    # モックDiaryModelを作成
    mock_diary_model = MockDiaryModel()

    # DiaryControllerのインスタンスを作成
    controller = DiaryController(diary_model=mock_diary_model)

    # インスタンス変数に正しいモデルが割り当てられているか確認
    assert controller.diary_model == mock_diary_model


def test_get_list_data():
    '''
    get_list_dataメソッドのテスト
    
    '''
    # モックDiaryModelを作成
    mock_diary_model = MockDiaryModel()

    # DiaryControllerのインスタンスを作成
    controller = DiaryController(diary_model=mock_diary_model)

    # get_list_dataメソッドを実行して結果を取得
    result = controller.get_list_data()

    # 期待される文字列を作成
    expected = (
        "id: 1 title: 日記1 content: 内容1 create_at: 2024-09-01 10:00\n"
        "id: 2 title: 日記2 content: 内容2 create_at: 2024-09-02 11:00"
    )

    # 返り値が期待通りか確認
    assert result == expected
    
def test_get_one():
    '''
    get_oneメソッドのテスト
    
    '''
    # モックDiaryModelを作成
    mock_diary_model = MockDiaryModel()

    # DiaryControllerのインスタンスを作成
    controller = DiaryController(diary_model=mock_diary_model)

    # get_list_dataメソッドを実行して結果を取得
    # idが1の場合
    result = controller.get_one(1)
    # 期待される文字列を作成
    expected = "id: 1 title: 日記1 content: 内容1 create_at: 2024-09-01 10:00"
    # 返り値が期待通りか確認
    assert result == expected
    
    # idが2の場合
    result = controller.get_one(2)
    expected = "id: 2 title: 日記2 content: 内容2 create_at: 2024-09-02 11:00"
    assert result == expected
    
    # idデータが存在しない場合
    result = controller.get_one(0)
    expected = ""
    assert result == expected