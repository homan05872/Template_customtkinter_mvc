import sqlite3
from abc import ABC
from typing import Optional

# 接続DB名
DB_NAME = 'sample.db'

class BaseModel(ABC):
    def __init__(self) -> None:
        # 接続のためのオブジェクト変数用意
        self.conn:Optional[sqlite3.Connection] = None
        self.cursor:Optional[sqlite3.Cursor] = None
    
    def connect(self) -> None:
        '''DBへの接続を開くメソッド'''
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
            # ↓辞書型でフィールドデータを取得するための指定
            self.cursor.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Connection error: {e}")
            raise
        
    def close(self) -> None:
        '''DBへの接続を閉じるメソッド'''
        self.conn.close()
        self.conn = None
        self.cursor = None

class DiaryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.t_diary = 'Diary'
    
    def get_all(self) -> list[sqlite3.Row]:
        '''Diaryテーブルから全てのデータを取得するメソッド'''
        data = []
        try :
            # 接続を確立
            self.connect()
            # データ取得の例
            self.cursor.execute(f'SELECT * FROM {self.t_diary}')
            data = self.cursor.fetchall()
        except Exception as e:
            print(f'Error{e}')
        finally:
            if self.conn:
                # 接続を閉じる
                self.close()
        return data
    
    def get_one(self, id:int) -> list[sqlite3.Row]:
        '''Diaryテーブルから全てのデータを取得するメソッド'''
        data = []
        try :
            # 接続を確立
            self.connect()
            # データ取得の例
            self.cursor.execute(f'SELECT * FROM {self.t_diary} WHERE id = ?', (id,))
            data = self.cursor.fetchone()
        except Exception as e:
            print(f'Error{e}')
        finally:
            if self.conn:
                # 接続を閉じる
                self.close()
        return data

# ****************************************************************************
# 下記メソッドは現状使用なし 使い方の例です。
# ****************************************************************************
    def update_record(self, id: int, title: str, content: str) -> None:
        '''Diaryテーブルの指定されたIDのレコードを更新するメソッド'''
        try:
            self.connect()
            self.cursor.execute(f'UPDATE {self.t_diary} SET title = ?, content = ? WHERE id = ?', (title, content, id))
            self.conn.commit()  # 変更を保存
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.close()
    
    def insert_record(self, title: str, content: str) -> None:
        '''Diaryテーブルに新しいレコードを挿入するメソッド'''
        try:
            self.connect()
            self.cursor.execute(f'INSERT INTO {self.t_diary} (title, content) VALUES (?, ?)', (title, content))
            self.conn.commit()  # 変更を保存
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.close()