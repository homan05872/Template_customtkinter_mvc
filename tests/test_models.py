import pytest
from source_code.models import DiaryModel  # 正しいインポート
import sqlite3
from unittest import mock
import os

@pytest.fixture
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
    
    yield conn
    
    # テスト後にロールバックしてデータを残さない
    cursor.execute('ROLLBACK')
    conn.close()


def test_setup_db(setup_db):

    conn = setup_db
    cursor = conn.cursor()
    # 辞書型で受け取るよう設定
    cursor.row_factory = sqlite3.Row
    # データが挿入されたことを確認
    cursor.execute("SELECT * FROM Diary")
    result = cursor.fetchall()
    
    # pytest のアサーションを使用
    assert len(result) == 3
    assert result[0]['title'] == '日記1'
    
    
# def test_setup_db():

#     # DiaryModel のインスタンス作成
#     diary_model = DiaryModel()
    
#     diary_model.connect = setup_db(diary_model)

#     # get_all メソッドをテスト
#     result = diary_model.get_all()
    
#     # pytest のアサーションを使用
#     assert len(result) == 3
#     assert result[0]['title'] == '日記1'