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
取引手数料 = 0  # 1回の取引手数料（円）
シミュレーション年数 = 30  # シミュレーション年数

# 定数
国内税率 = 15.315  # 国内所得税率（％）
住民税率 = 5.0  # 住民税率（％）
米国源泉徴収税率 = 10.0  # 米国源泉徴収税率（％）

# 月次利回りと株価成長率への変換
月次利回り = (1 + ETF年間利回り / 100) ** (1 / 12) - 1
月次株価成長率 = (1 + 年間株価成長率 / 100) ** (1 / 12) - 1

# 税率の計算関数
def 税率を計算する():
    if NISA使用:
        return 0.0
    税率 = 国内税率
    if not 住民税免除:
        税率 += 住民税率
    if 米国株:
        税率 -= 米国源泉徴収税率  # 外国税額控除を適用
    return 税率

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
        税引後配当金 = 年間配当金 * (1 - 税率)
        税引後配当金 = int(税引後配当金)  # 小数点以下切り捨て

        # 再投資可能額
        再投資額 = 税引後配当金 * (配当金再投資割合 / 100)
        再投資額 = int(再投資額)  # 小数点以下切り捨て
        買付株数 = (月次増資額 * 12 + 再投資額 - 取引手数料) // 現在のETF単価

        # 保有株数と投資額の更新
        保有株数 += 買付株数
        総投資額 += 月次増資額 * 12
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
