import pytest
from src.models import DiaryModel,BaseModel
import sqlite3
import os

# ***************************************************
# フィクスチャ(セットアップ関数)
# ***************************************************
@pytest.fixture(scope='session')
def setup_db():
    '''テストデータを用意するメソッドです。 ※実行されるのは一回のみ'''
    # トランザクション開始
    db_path = os.path.join('db',"sample.db")
    conn = sqlite3.connect(db_path, isolation_level = None)
    cursor = conn.cursor()
    # 辞書型で受け取るよう設定
    cursor.row_factory = sqlite3.Row
    
    # トランザクションの開始
    cursor.execute("BEGIN")
    
    # テストデータを用意
    # テーブルをドロップし、新しいテーブルを作成
    cursor.execute("DROP TABLE IF EXISTS Diary")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            create_at TEXT
        )
    ''')

    # テストデータを挿入
    cursor.execute('''
        INSERT INTO Diary (title, content, create_at) 
        VALUES ('日記1', '内容１', '2024-8-31 16:34'),
                ('日記2', '内容２', '2024-8-31 16:34'),
                ('日記3', '内容３', '2024-8-31 16:34')
    ''')
    
    yield conn, cursor
    
    # テスト後にロールバックしてデータを残さない
    cursor.execute('ROLLBACK')
    conn.close()
    
@pytest.fixture
def mock_db_connection(monkeypatch, setup_db):
    '''
    connectとcloseメソッドをモック化とsetup_dbsetで用意した、cursorオブジェクトを取得するメソッド
    '''
    conn, cursor = setup_db  # setup_dbフィクスチャから取得
    # connectとcloseをモンキーパッチする
    monkeypatch.setattr(BaseModel, "connect", lambda self:mock_connect(self, conn, cursor))
    monkeypatch.setattr(BaseModel, "close", mock_close)
    
    return cursor  # テスト用にカーソルを返す

# ***************************************************
# モック関数
# ***************************************************
def mock_connect(self, conn, cursor):
    '''モデルクラスのconnectメソッドをモック化'''
    self.conn = conn
    self.cursor = cursor

def mock_close(self):
    '''モデルクラスのcloseメソッドをモック化(無効化)'''
    # DBを閉じない（何もしない）
    pass

# ***************************************************
# テスト関数
# ***************************************************
def test_setup_db(mock_db_connection):
    """
    このテストでは、テスト用日記データを正しく登録されていることを確認します。
    データベースには3つの日記があり、それらが正しく返されることをテストします。
    """
    cursor = mock_db_connection
    
    # データが挿入されたことを確認
    cursor.execute("SELECT * FROM Diary")
    result = cursor.fetchall()
    
    # assertメソッドでデータが正しいか確かめる
    # データの数
    assert len(result) == 3
    # 内容のテスト
    assert result[0]['id'] == 1
    assert result[0]['title'] == '日記1'
    assert result[0]['content'] == '内容１'
    assert result[0]['create_at'] == '2024-8-31 16:34'
    assert result[1]['id'] == 2
    assert result[1]['title'] == '日記2'
    assert result[1]['content'] == '内容２'
    assert result[1]['create_at'] == '2024-8-31 16:34'
    assert result[2]['id'] == 3
    assert result[2]['title'] == '日記3'
    assert result[2]['content'] == '内容３'
    assert result[2]['create_at'] == '2024-8-31 16:34'
    

def test_get_all(mock_db_connection):
    """
    このテストでは、get_allメソッドが全ての日記データを正しく取得できるかどうかを確認します。
    データベースには3つの日記があり、それらが正しく返されることをテストします。
    """
    # モックを設定
    mock_db_connection
    # DiaryModel のインスタンス作成
    diary_model = DiaryModel()
    
    # get_all メソッドをテスト
    result = diary_model.get_all()
    # pytest のアサーションを使用
    # データの数
    assert len(result) == 3
    # 内容
    assert result[0]['id'] == 1
    assert result[0]['title'] == '日記1'
    assert result[0]['content'] == '内容１'
    assert result[0]['create_at'] == '2024-8-31 16:34'
    assert result[1]['id'] == 2
    assert result[1]['title'] == '日記2'
    assert result[1]['content'] == '内容２'
    assert result[1]['create_at'] == '2024-8-31 16:34'
    assert result[2]['id'] == 3
    assert result[2]['title'] == '日記3'
    assert result[2]['content'] == '内容３'
    assert result[2]['create_at'] == '2024-8-31 16:34'
    
def test_get_one(mock_db_connection):
    """
    このテストでは、get_oneメソッドの下記２つのテストを実施。
    1. 引数1で渡したidの日記データを正しく取得できるかことを確認します。
    2. 引数1で渡したidの日記データが存在しない場合Noneが返される事を確認します。
    """
    # モックを設定
    mock_db_connection
    # DiaryModel のインスタンス作成
    diary_model = DiaryModel()

    # get_all メソッドをテスト
    result = diary_model.get_one(1)
    
    # idが1のレコードを取得出来ていることを確認
    assert result['id'] == 1
    assert result['title'] == '日記1'
    assert result['content'] == '内容１'
    assert result['create_at'] == '2024-8-31 16:34'
    
    result = diary_model.get_one(2)
    
    # idが2のレコードを取得出来ていることを確認
    assert result['id'] == 2
    assert result['title'] == '日記2'
    assert result['content'] == '内容２'
    assert result['create_at'] == '2024-8-31 16:34'
    
    # idが存在しないレコードの場合はNoneが返される事を確認
    result = diary_model.get_one(0)
    
    assert result == None