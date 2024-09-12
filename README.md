# Template_customtkinter_mvc
customtkinterのmvcパターン開発のテンプレートです。

## 環境
- 言語:python
- 外部モジュール：customtkinter
- DB:sqlite3

## アーキテクチャ
 mvcパターンを採用しており、それぞれ下記のモジュールにそれぞれのクラスを定義します。
 - ビュー：views.py & pages.py(Presentation Layer)
 - コントローラ：controllers.py(Business Logic Layer)
 - モデル：models.py(DataAccess Layer)

![alt text](設計/images/アーキテクチャ図_architecture.png)

## クラス
クラス構成は下記のようになっております。

| クラス名 | 種類 | 説明 | 備考 |
| -- | -- | -- | -- |
| MainWindowクラス | ビュー | メインウィンドウ表示 & Pageクラスを管理 | ページの表示・遷移など |
| Pageクラス | ビュー | 画面UIの生成 & UI更新担当 | 抽象クラス有 |
| Contorllerクラス | コントローラ | ビジネスロジックを担当 |  |
| Modelクラス | モデル | DB連携を担当 | 抽象クラス有 |

![alt text](設計/images/クラス構成図_class.png)

## モジュール構成
基本的に作成した各クラスをmain.py(エントリポイント)で生成し、それぞれ書くクラス独立した状態を保ちつつ連携を行います。

![alt text](設計/images/モジュール構成図_module.png)

## 使い方
※下記はmain.pyです。
1. モデルとコントローラはアプリDBの使用するテーブルごとに作成する。

1. 作成したコントローラはmain()関数でインスタンス化し、MainWindowクラスで使用するクラスをインスタンス生成時に渡す
    ```python
    def main():
    # モデルを生成
    diary_model = DiaryModel()
    
    # コントローラクラス群の辞書型定義
    main_controllers={
        "diary": DiaryController(diary_model),
    }
    # スタイルクラス群の辞書型定義
    main_styles={
        "main": MainStyle(),
    }
    
    # ビュークラスにページクラス群とコントローラークラス群を渡す
    main_window = MainWindow(main_controllers, main_styles)
    ```
1. MainWindowクラスで使用するページは下記のループでインスタンス生成
    ```python
    # ページクラス配置
    for PageClass in [Page1, Page2]:
        page_name = PageClass.__name__
        page = PageClass(master=main_window, **main_styles['main'].transparent_frame)
        main_window.pages[page_name] = page
        page.grid(row=0, column=0, sticky="nsew")
    ```
1. 最初に表示したいページを下記のように設定する。
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

ビューを更新するメソッドはこのPageクラスに定義する。