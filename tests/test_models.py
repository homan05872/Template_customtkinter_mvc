import pytest
from src.models import DiaryModel  # 正しいインポート
import sqlite3
from unittest import mock
import os

@pytest.fixture(scope='session')
def setup_db():
    
    # トランザクション開始
    db_path = os.path.join('db',"sample.db")
    conn = sqlite3.connect(db_path, isolation_level = None)
    cursor = conn.cursor()
    
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
    conn, cursor = setup_db  # setup_dbフィクスチャから取得
    
    # モデルクラスのconnectメソッドをモック化
    def mock_connect(self):
        self.conn = conn
        self.cursor = cursor
        # 辞書型で受け取るよう設定
        self.cursor.row_factory = sqlite3.Row
    
    # モデルクラスのcloseメソッドを無効化
    def mock_close(self):
        # DBを閉じない（何もしない）
        pass

    # connectとcloseをモンキーパッチする
    monkeypatch.setattr(DiaryModel, "connect", mock_connect)
    monkeypatch.setattr(DiaryModel, "close", mock_close)

    yield cursor  # テスト用にカーソルを返す


def test_setup_db(mock_db_connection):
    cursor = mock_db_connection
    # データが挿入されたことを確認
    cursor.execute("SELECT * FROM Diary")
    result = cursor.fetchall()
    
    # pytest のアサーションを使用
    assert len(result) == 3
    assert result[0]['title'] == '日記1'
    
    
def test_setup_db():

    # DiaryModel のインスタンス作成
    diary_model = DiaryModel()
    
    diary_model.connect = setup_db(diary_model)

    # get_all メソッドをテスト
    result = diary_model.get_all()
    
    # pytest のアサーションを使用
    assert len(result) == 3
    assert result[0]['title'] == '日記1'