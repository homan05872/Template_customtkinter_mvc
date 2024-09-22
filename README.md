# Template_customtkinter_mvc
customtkinterのmvcパターン開発のテンプレートです。

## 環境
- 言語:python
- 外部モジュール：customtkinter
- DB:sqlite3
- OS:windows11

## アーキテクチャ
 mvcパターンを採用しており、それぞれ下記のモジュールにそれぞれのクラスを定義します。
 - ビュー：views.py & pages.py(Presentation Layer)
 - コントローラ：controllers.py(Business Logic Layer)
 - モデル：models.py(DataAccess Layer)

![alt text](設計/images/アーキテクチャ図_architecture.png)

## クラス
主なクラス構成は下記のようになっております。

| クラス名 | 種類 | 説明 | 備考 |
| -- | -- | -- | -- |
| MainWindowクラス | ビュー | メインウィンドウ表示 & Pageクラスを管理 | ページの表示・遷移など |
| Pageクラス | ビュー | 画面UIの生成 & UI更新担当 | 抽象クラス有 |
| Contorllerクラス | コントローラ | ビジネスロジックを担当 |  |
| Modelクラス | モデル | DB連携を担当 | 抽象クラス有 |
| CommonStyeleクラス | ビュー | ウィジェットのスタイル保持する(共通化したいものなど) ||
| Appクラス | ビュー | 各クラスの連携やアプリ起動を担当 |下記のクラス図には載せていません。|

![alt text](設計\images\クラス図.drawio.svg)

## モジュール構成
基本的に作成した各クラスをmain.py(エントリポイント)で生成し、それぞれ書くクラス独立した状態を保ちつつ連携を行います。

![alt text](設計/images/モジュール構成図_module.png)

## 画面
- ページ１
ボタンを押すとメッセージでDBから取得した一覧データが表示されます。
![alt text](設計\images\ページ１.png)
- ページ２
ボタンを押すとメッセージボックスに入力したIDのレコードデータが表示されます。
![alt text](設計\images\ページ２.png)

## 事前準備
下記のスクリプトを実行し、「sample.db」を作成し、ルートディレクトリに配置してください。
create_DB.py
```python
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

```

作成されるDiaryテーブルとサンプルデータ
![alt text](設計\images\Diaryテーブル.png)


## 使い方
※下記はmain.pyです。
1. モデルとコントローラはアプリDBの使用するテーブルごとに作成する。

1. 作成したコントローラはmain()関数でAppクラスをインスタンス化し、run()メソッドでアプリ起動する仕組みになっています。
    ```python
    def main() -> None:
        # 各クラスのインスタンス生成
        app = App()
        # アプリ起動
        app.run()
    ```
1. 各クラス間の連携はAppクラスのコンストラクタで行う。
    ```python
    class App:
    def __init__(self) -> None:
        ''' 各クラスの連携(インスタンス生成) '''
        # モデルクラス群を生成
        self.diary_model = DiaryModel()
        
        # コントローラクラス群の辞書型定義
        self.main_controllers={
            "diary": DiaryController(self.diary_model),
        }
        # スタイルクラス群を生成
        self.main_style=CommonStyle()     # 共通スタイル定義クラス
        
        # ウィンドウクラスにコントローラークラス群とスタイルクラスを渡す
        self.main_window = MainWindow(self.main_controllers, self.main_style)
        
        # ページクラス配置
        self.main_window.page_set([Page1, Page2])      # ← 配置したいPageクラスを配列で渡す
    ```
1. BaseWindowクラス(抽象クラス)のpage_setメソッドに各ウィンドウで表示したいPageクラスの配列を渡して配置する。（Appクラスのコンストラクタで呼び出しています。）
    ```python
    def page_set(self, pages:Any):
        ''' Pageクラスの配置を行うメソッド '''
        # ページクラス配置
        for PageClass in pages:
            page_name = PageClass.__name__
            page = PageClass(master=self, **self.style.transparent_frame)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")
    ```
1. 最初に表示したいページはAppクラスのrunメソッドで設定します。
    ```python
    # アプリケーション開始
    main_view.show_page("Page1") # 最初に表示したいページクラス名を渡す。
    main_view.mainloop()
    ```
## Pageクラスの作り方
下記のクラスを抽象クラスを継承して作る。

pages.py
```python
class BasePage(ctk.CTkFrame, ABC):
    def __init__(self, master:ctk.CTk|tk.Tk, **kwargs) -> None:
        super().__init__(master, **kwargs)

    @abstractmethod
    def build_ui(self):
        """UIを構築するための抽象メソッド"""
        ...
        
    def show_page(self, page_name:str) -> None:
        '''ページ遷移するメソッド'''
        self.master.show_page(page_name)
```

build_ui()メソッドを使ってuiを作る。
ページ更新用のメソッドもここに関数を使ってボタンなどに設定する。
データを取得したいコントローラはviewで生成時に渡したcontrollersからページで使用するコントローラをインスタンスメソッドに出す。

```python
class Page1(BasePage):
    def __init__(self, master:ctk.CTk, controllers: dict[str, Any], **kwargs) -> None:
        super().__init__(master, **kwargs)
        # コントローラ設定
        self.diary_controller = controllers['diary']
        # UI生成
        self.build_ui()
        
    def build_ui(self):
        '''UI生成するメソッド'''
        # ここでこのページで表示したいUIを作る
        ...
```

ビューを更新するメソッドはこのPageクラスに定義します。必要なビジネスロジックがあればコントローラクラスのメソッドを使用し、データを取得したりします。

```python
class Page1(BasePage):
    # ...省略...
    def msg_output(self, page_num:int) -> None:
        '''メッセージを出力するメソッド'''
        data:str = self.diary_controller.get_list_data()
        messagebox.showinfo("Information", f"ページ{page_num}のメッセージです。\n\n"
                            + "Diaryデータ：\n"
                            + f"{data}")
```

## CommonStyleクラスの使い方
このクラスは共通のスタイルを保持し、それを各クラスで取り出して使用するために作ったクラスです。
```python
class CommonStyle:
    ''' 共通のスタイルを定義するクラス '''
    def __init__(self) -> None:
        # 文字フォント設定
        self.HEADER_TITLE = (FONT_TYPE, 20, "bold")
        self.FRAME_TITLE = (FONT_TYPE, 17, "bold")
        self.DEFAULT = (FONT_TYPE, 15)
        
        # Windowの背景色
        self.transparent_frame = {
            "fg_color": BASE_COLOR_DARK,
        }
        
        # インラインボタン
        self.inline_btn = {
            "text_color": ("gray10", "#DCE4EE"),
            "fg_color": "transparent",
            "border_width":2,
        }
```

使用するときはCommonStyleのインスタンス変数をとりだして、下記のようにウィジェットの引数に渡すと、定義したスタイルを適応することができます。
```python
class Page1(BasePage):
    def build_ui(self) -> None:
        '''UI生成するメソッド'''
        # Gridレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        # ・・省略・・
        
        self.msg_btn = ctk.CTkButton(self, text="メッセージ表示", command=lambda: self.msg_output(1), **self.style.inline_btn)
                                                                                                        # ↑ココ
        self.msg_btn.grid(row=1, column=1, padx=(0,20), pady=40)
```

## コントローラクラスとモデルクラス
下記のように必要なメソッドを定義するだけです。

controllers.py
```python
class DiaryController:
    def __init__(self, diary_model:BaseModel) -> None:
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
```

models.py
```python
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
```