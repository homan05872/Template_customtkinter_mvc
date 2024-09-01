-- サンプルのDBです。Sqlite3でDB名を「sample.db」として作成し、
-- 下記のクエリを実行してください。

-- table
DROP TABLE IF EXISTS Diary;

CREATE TABLE IF NOT EXISTS Diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content Text,
    create_at TEXT
);

-- data
INSERT INTO Diary (title, content, create_at)
VALUES ('日記1', '内容１', '2024-8-31 16:34');
INSERT INTO Diary (title, content, create_at)
VALUES ('日記2', '内容２', '2024-8-31 16:34');
INSERT INTO Diary (title, content, create_at)
VALUES ('日記3', '内容３', '2024-8-31 16:34');