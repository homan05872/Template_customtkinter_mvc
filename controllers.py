from models import BaseModel
from typing import Any

class DiaryController:
    def __init__(self, diary_model:BaseModel) -> None:
        super().__init__()
        # モデル変数用意
        self.diary_model = diary_model

    def get_list_data(self) -> str:
        '''Diaryデータを取得するメソッド'''
        # モデルからデータ取得
        data_list:list[Any] = self.diary_model.get_all()
        # データを文字列へ成形する
        data_str_list:list[str] = [
            f"id: {data['id']} title: {data['title']} content: {data['content']} create_at: {data['create_at']}"
            for data in data_list
        ]
        # リストを改行で結合して、一つの文字列にする
        data_str:str = "\n".join(data_str_list)
        
        return data_str
    
    def get_one(self, id:int) -> str:
        '''idでレコ―ドデータを取得'''
        # 初期化
        data_str = ""
        # モデルからデータ取得
        data:list[Any] = self.diary_model.get_one(id)
        # データを文字列へ成形する
        if data:
            data_str:str = f"id: {data['id']} title: {data['title']} content: {data['content']} create_at: {data['create_at']}"
        
        return data_str