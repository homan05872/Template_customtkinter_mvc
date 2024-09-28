# ************************************************************
# 下記の手順でDBを用意
# １．スクリプトを実行し、DB(sample.db)を作成する
# ２．ルートディレクトリにdbフォルダを作成
# ３．dbフォルダに作成されたsample.dbを配置する
# ************************************************************

import sqlite3

# データベースに接続（ファイルが存在しない場合は自動で作成される）
conn = sqlite3.connect('sample.db')

# カーソルオブジェクトを作成
cur = conn.cursor()

# SQLクエリを実行
sql_query = '''
-- table
DROP TABLE IF EXISTS Diary;

CREATE TABLE IF NOT EXISTS Diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    create_at TEXT
);

-- data
INSERT INTO Diary (title, content, create_at)
VALUES ('日記1', '内容１', '2024-8-31 16:34'),
       ('日記2', '内容２', '2024-8-31 16:34'),
       ('日記3', '内容３', '2024-8-31 16:34');
'''

# SQLクエリの実行
try:
    cur.executescript(sql_query)
    print("テーブルの作成およびデータの挿入が成功しました。")
except sqlite3.Error as e:
    print(f"エラーが発生しました: {e}")
finally:
    # コミットしてデータを保存
    conn.commit()

    # 接続を閉じる
    conn.close()
