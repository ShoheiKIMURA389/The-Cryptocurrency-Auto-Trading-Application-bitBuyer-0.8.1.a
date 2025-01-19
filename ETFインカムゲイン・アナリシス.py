# VS Code を用いた利用方法
# --- Mac 及び Windows 共通 ---
# 1. 必要なライブラリの確認
# 以下のコマンドをターミナル（Mac）またはコマンドプロンプト（Windows）で実行し、ライブラリがインストールされているか確認してください。
# ```
# pip list | grep pandas または pip3 list | grep pandas
# pip list | grep PyQt5 または pip3 list | grep PyQt5
# ```
# 上記のコマンドで "pandas" と "PyQt5" が表示されない場合、以下のインストール手順を実行してください。

# 2. 必要なライブラリのインストール
# 以下のコマンドを使用してインストールを行います。
# ```
# pip install pandas PyQt5 または pip3 install pandas PyQt5
# ```

# 3. VS Code の設定
# - VS Code でこのスクリプトファイルを開きます。
# - Python 拡張機能がインストールされていることを確認してください。
# - このスクリプトを実行するには、VS Code ウィンドウ右上の再生ボタンをクリックします。

# 4. 実行結果
# シミュレーション結果がウィンドウに表示されます。
# ウィンドウは閉じるまで保持されますので、必要に応じて確認してください。

import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# グローバル変数の定義
ETF年間利回り = 7.22  # 年間利回り（％）
年間株価成長率 = 2.0  # 年間株価成長率（％）
ETF単価 = 9100  # 初期ETF価格（円）
ETF初期株数 = 1000  # 初期株数
月次増資額 = 34000  # 毎月の増資額（円）
配当金再投資割合 = 100  # 配当金再投資割合（％）
NISA使用 = True  # NISA利用の有無
住民税免除 = True  # 住民税免除の有無
米国株 = True  # 米国株かどうか
年間取引手数料 = 0  # 年間の取引手数料（円）
シミュレーション年数 = 10  # シミュレーション年数

# 定数
国内税率 = 15.315  # 国内所得税率（％）
住民税率 = 5.0  # 住民税率（％）
米国源泉徴収税率 = 10.0  # 米国源泉徴収税率（％）
NISA上限 = 18_000_000  # NISAの成長投資枠上限（円）

# 月次利回りと株価成長率への変換
月次利回り = (1 + ETF年間利回り / 100) ** (1 / 12) - 1
月次株価成長率 = (1 + 年間株価成長率 / 100) ** (1 / 12) - 1

# 税率の計算関数
def 税率を計算する():
    税率 = 国内税率
    if not 住民税免除:
        税率 += 住民税率
    if 米国株:
        税率 -= 米国源泉徴収税率  # 外国税額控除を適用
    return round(税率, 5)  # 小数点以下第六位を繰り上げ

# シミュレーション関数
def シミュレーションを実行する():
    税率 = 税率を計算する() / 100
    保有株数 = ETF初期株数
    現在のETF単価 = ETF単価
    総投資額 = 保有株数 * 現在のETF単価

    # 結果を格納するリスト
    結果 = []

    for 年次 in range(1, シミュレーション年数 + 1):
        年間配当金 = 保有株数 * 現在のETF単価 * 月次利回り * 12  # 税引前年間配当金
        年間配当金 = int(年間配当金)  # 小数点以下切り捨て

        # NISA非課税部分と課税対象部分を分けて計算
        非課税割合 = min(1, NISA上限 / 総投資額) if 総投資額 > 0 and NISA使用 else 0
        課税割合 = 1 - 非課税割合

        非課税配当 = 年間配当金 * 非課税割合
        課税配当 = 年間配当金 * 課税割合

        税引後配当金 = 非課税配当 + (課税配当 * (1 - 税率))
        税引後配当金 = int(税引後配当金)  # 小数点以下切り捨て

        # 再投資可能額
        再投資額 = 税引後配当金 * (配当金再投資割合 / 100)
        再投資額 = int(再投資額)  # 小数点以下切り捨て
        買付株数 = (月次増資額 * 12 + 再投資額 - 年間取引手数料) // 現在のETF単価

        # 保有株数と投資額の更新
        保有株数 += 買付株数
        総投資額 += 再投資額  # 再投資額を総投資額に加算
        総投資額 = int(総投資額)  # 小数点以下切り捨て

        # 株価成長
        現在のETF単価 *= (1 + 月次株価成長率) ** 12
        現在のETF単価 = int(現在のETF単価)  # 小数点以下切り捨て

        # 年次データを保存
        結果.append({
            "年次": 年次,
            "保有株数": f"{保有株数:,}",
            "年間配当金（円）": f"{税引後配当金:,}",
            "買付株数": f"{買付株数:,}",
            "総投資額（円）": f"{総投資額:,}",
            "ETF株価（円）": f"{現在のETF単価:,}",
        })

    # データフレームに変換して返す
    return pd.DataFrame(結果)

# データフレームをウィンドウで表示する関数
def 表を表示する(dataframe):
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("シミュレーション結果")
    layout = QVBoxLayout()

    table = QTableWidget()
    table.setRowCount(len(dataframe))
    table.setColumnCount(len(dataframe.columns))
    table.setHorizontalHeaderLabels(dataframe.columns)

    for row_idx, row in dataframe.iterrows():
        for col_idx, value in enumerate(row):
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    layout.addWidget(table)
    window.setLayout(layout)

    # ウィンドウサイズを設定
    screen = QApplication.primaryScreen().availableGeometry()
    width = int(screen.width() * 0.5)  # 横幅を50%に設定
    height = int(screen.height() * 0.8)  # 縦幅を80%に設定
    window.resize(width, height)
    window.move((screen.width() - width) // 2, (screen.height() - height) // 2)

    window.show()
    app.exec_()

# メイン処理
def メイン():
    シミュレーション結果 = シミュレーションを実行する()
    表を表示する(シミュレーション結果)

# プログラム実行
if __name__ == "__main__":
    メイン()
