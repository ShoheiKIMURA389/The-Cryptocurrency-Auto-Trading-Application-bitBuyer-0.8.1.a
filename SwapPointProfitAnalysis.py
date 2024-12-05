"""
【スワップポイント計算プログラムの使い方】

このプログラムは、運用中および未運用のスワップポイント収益を計算し、そのトレンドをグラフとして可視化するツールです。
プログラムを実行することで、運用状況を理解しやすくなります。

プログラムファイル名: "SwapPointProfitAnalysis.py"

---
1. Python がインストールされているかの確認方法
    1.1 Mac の場合:
        - ターミナルを開き、以下のコマンドを入力してください。
          "python3 --version"
        - バージョンが表示されれば Python がインストールされています。
          例: "Python 3.9.x"
        - 表示されない場合はインストールが必要です。

    1.2 Windows の場合:
        - コマンドプロンプトを開き、以下のコマンドを入力してください。
          "python --version"
        - または以下を試してください。
          "py --version"
        - バージョンが表示されれば Python がインストールされています。
          例: "Python 3.9.x"
        - 表示されない場合はインストールが必要です。

---
2. Python のインストール方法
    Mac 及び Windows で、以下の手順を実行してください。

    2.1 Python をコマンドでインストール:
        1. ターミナルまたはコマンドプロンプトを開きます。
        2. 次のコマンドを入力して Python をインストールします。
           Mac の場合:
           "brew install python"
           Windows の場合:
           "choco install python"
        3. インストール後、上記の "python3 --version" または "python --version" でバージョンを確認してください。

    2.2 Python のインストールが完了したら、"pip" または "pip3" コマンドが有効になっていることを確認します。

---
3. 必要なライブラリのインストール状況確認とインストール方法
    このプログラムでは以下のライブラリを使用します。
    - "matplotlib"

    3.1 ライブラリのインストール状況確認:
        - ターミナルまたはコマンドプロンプトで以下を入力してください。
          "pip show matplotlib"
        - または:
          "pip3 show matplotlib"
        - 結果が表示されればインストールされています。

    3.2 ライブラリのインストール方法:
        - インストールされていない場合は以下を入力してください。
          "pip install matplotlib"
        - または:
          "pip3 install matplotlib"

---
4. VS Code を使ったプログラム実行方法
    4.1 VS Code をインストール:
        - 公式サイトからインストールしてください。
          URL: https://code.visualstudio.com
    
    4.2 Python 拡張機能をインストール:
        - VS Codeを開き、左側の「拡張機能」アイコンをクリックします。
        - 検索バーに "Python" と入力し、Microsoft が提供する Python 拡張機能をインストールします。

    4.3 このプログラムを実行:
        - プログラムをファイルに保存します。例: "SwapPointProfitAnalysis.py"
        - VS Code でこのファイルを開き、右側上部メニューの再生ボタンをクリックします。
        - VS Code 下部にコンソールが表示され、結果が表示されます。その直後、グラフが描画されます（ほぼ同時）。

---
5. トラブルシューティング
    - ライブラリが見つからないエラーが発生する場合:
        - 上記「ライブラリのインストール方法」を再度確認してください。
    - グラフが表示されない場合:
        - 実行環境（ターミナルやコマンドプロンプト）が正しいか確認してください。
        - Python のバージョンが 3.6 以上であることを確認してください。

---
これで準備完了です。プログラムを実行してスワップ収益計算を体験してください！
"""

# 【初期設定】

# 【初期投資額（円）】
# このプログラムで運用を開始するための最初の投資金額を指定します。
# この金額は最初に保有するロット数の購入に充当され、以後の計算に使用されます。
InitialInvestment = 600000

# 【各通貨の一日当たりのスワップポイント（円）】
# MXN/JPY（メキシコ・ペソ）と ZAR/JPY（南アフリカ・ランド）の通貨ペアで、
# 1ロット当たりの1日毎に得られるスワップポイントを設定します。
MxnSwapPerDay = 20
ZarSwapPerDay = 18

# 【1ロット購入に必要な金額】
# 各通貨の1ロット（DMM FXの場合：1万通貨）を購入するために必要な日本円の金額を指定します。
# この値は実際の為替レートを基に設定され、再投資や追加投資のロット数計算に使用されます。
Mxn1LotCost = 2958  # MXN/JPY
Zar1LotCost = 3318  # ZAR/JPY

# 【初期ロット数】
# 最初に購入するロット数を通貨ペア毎に設定します。
# このロット数に基づいてスワップポイント収益が計算されます。
MxnLots = 60  # MXN/JPY のロット数
ZarLots = 50  # ZAR/JPY のロット数

# 【追加投資設定】
# 偶数月の16日に行う追加投資に関する設定です。
# この設定は、日本の年金受給者を想定しており、偶数月（2月、4月、6月...）に
# 年金が支給されるタイミングで、一部の資金を追加投資に充当する前提で計算を行います。
# 実際の日本の公的年金は「偶数月の15日」に支給されますが、16日を投入日とすることで、
# 資金投入の判断を行う時間を確保することを目的としています。

# 【偶数月に投入する追加投資額（円）】
# 偶数月16日に投入する追加投資額を指定します。
# この金額の 25% ずつを MXN/JPY 及び ZAR/JPY に分配して新たなロットを購入します。
BiMonthlyInvestment = 50000

# 【年間スワップ収益がこの金額に達すると追加投資を中止】
# 障害年金受給者を想定し、年収が 370 万円を超えると障害年金の支給が半減、472 万円を超えると停止されるため、
# この金額を上限として追加投資を中止するよう設定しています。
# ただし、上限に達するまでに計画されている当年分の追加投資は実行されます。
InvestmentIncomeLimit = 3700000

# 【各通貨の年間スワップ収益】
# 各通貨ペアにおいて、1ロット当たりの年間スワップ収益を計算した値です。
# これは運用益の参考値として使用されますが、プログラム内のロット購入計算には直接影響しません。
MxnSwapPerYear = MxnSwapPerDay * 365  # MXN/JPY の年間スワップ収益
ZarSwapPerYear = ZarSwapPerDay * 365  # ZAR/JPY の年間スワップ収益

# 運用成績を計算する関数
def CalculateSwapGrowth():
    """
    スワップポイントを複利計算し、3年間分の日次スワップ収益データを生成します。
    偶数月の16日に追加投資を行い、日次のスワップ収益から再投資を行います。

    Returns:
        tuple: 日次、累積スワップの収益データを格納したリスト。
    """
    # 日次収益データの初期化
    DailySwap = []  # 日次収益データ
    CumulativeSwap = []  # 累積スワップポイントのデータ

    # 初期資産設定
    TotalInvestment = InitialInvestment  # 初期投資額
    TotalCumulativeSwap = 0  # 累積スワップポイントの累積
    CurrentMxnLots = MxnLots  # MXN/JPYのロット数
    CurrentZarLots = ZarLots  # ZAR/JPYのロット数
    IsYearLimitReached = False  # 年間収益が上限に達したかを管理
    RemainingReinvestment = 0  # 再投資額の残高

    # 日次スワップ収益計算（3年間分）
    for Day in range(1, 3 * 365 + 1):
        # 各通貨の1日当たりのスワップ収益
        MxnDailySwap = CurrentMxnLots * MxnSwapPerDay  # MXN/JPYの日次スワップ収益
        ZarDailySwap = CurrentZarLots * ZarSwapPerDay  # ZAR/JPYの日次スワップ収益

        # 総スワップ収益（日次）
        DailyIncome = MxnDailySwap + ZarDailySwap  # 日次の総スワップ収益

        # 複利計算のための再投資額（スワップポイントの50%）
        Reinvestment = DailyIncome * 0.5  # 再投資額
        RemainingReinvestment += Reinvestment  # 再投資額を残高に追加

        # 再投資でロットを購入（MXNとZARに分配）
        while RemainingReinvestment >= Mxn1LotCost or RemainingReinvestment >= Zar1LotCost:
            if RemainingReinvestment >= Mxn1LotCost:
                CurrentMxnLots += 1
                RemainingReinvestment -= Mxn1LotCost
            elif RemainingReinvestment >= Zar1LotCost:
                CurrentZarLots += 1
                RemainingReinvestment -= Zar1LotCost

        # 偶数月の16日に追加投資を実施
        if (Day % 30 == 15 and (Day // 30 + 1) % 2 == 0):  # 偶数月の16日を判定
            if not IsYearLimitReached or (Day - 1) % 365 < 334:  # 年内の追加投資を継続
                TotalInvestment += BiMonthlyInvestment  # 追加入金

                # 追加入金額を4分割
                MxnInvestment = BiMonthlyInvestment * 0.25
                ZarInvestment = BiMonthlyInvestment * 0.25

                # 入金額をMXNとZARに分配してロット数を増加
                if MxnInvestment >= Mxn1LotCost:
                    CurrentMxnLots += MxnInvestment // Mxn1LotCost
                    RemainingReinvestment += MxnInvestment % Mxn1LotCost
                if ZarInvestment >= Zar1LotCost:
                    CurrentZarLots += ZarInvestment // Zar1LotCost
                    RemainingReinvestment += ZarInvestment % Zar1LotCost

        # 累積スワップポイントの更新
        TotalCumulativeSwap += DailyIncome  # 全収益を累積

        # 年間収益が上限に達した場合のフラグを更新
        if TotalCumulativeSwap >= InvestmentIncomeLimit and not IsYearLimitReached:
            IsYearLimitReached = True  # 年間収益の上限に到達

        # 日次収益の保存
        DailySwap.append(TotalInvestment)  # 日次の累積投資額を保存
        CumulativeSwap.append(TotalCumulativeSwap)  # 累積スワップポイントを保存

    return DailySwap, CumulativeSwap

# グラフを描画する関数
def PlotSwapData(DailySwap, CumulativeSwap):
    """
    スワップ収益の運用中と未運用のトレンドを別々のグラフに描画します（3年分）。

    Args:
        DailySwap (list): 日次スワップ収益データ（運用中、元本を含む）。
        CumulativeSwap (list): 累積スワップ収益データ（未運用、元本を差し引いた純利益）。
    """
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker  # 軸のフォーマット調整用

    # 日次データを年次データに変換
    DaysPerYear = 365  # 1年の日数
    Years = [day / DaysPerYear for day in range(1, len(DailySwap) + 1)]  # 年単位のX軸

    # 未運用スワップ収益を計算（累積スワップ収益から元本を差し引く）
    NotUsedSwap = [cumulative - InitialInvestment for cumulative in CumulativeSwap]

    # フォーマッター関数: 金額を"K"単位に変換しカンマ区切りを追加
    def FormatYAxisK(value, _):
        return f"{int(value // 1_000):,}K"  # 1,000で割りカンマ区切りで"K"を付与

    # グラフウィンドウを作成（1行2列のサブプロット）
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1行2列の配置

    # 運用中スワップ収益のグラフ（左側）
    axes[0].plot(Years, DailySwap, marker="o", label="In Use Swap Income (With Principal)", linestyle="--")
    axes[0].set_title("In Use Swap Income (With Principal)", fontsize=16)
    axes[0].set_xlabel("Year", fontsize=14)
    axes[0].set_ylabel("Swap Income (JPY, in K)", fontsize=14)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisK))  # 縦軸をK単位でカンマ区切り
    axes[0].grid(True)  # グリッド表示
    axes[0].legend(fontsize=12)

    # 年間スワップ収益の参考値をグラフ内に表示
    try:
        max_y = max(DailySwap) * 0.8 if max(DailySwap) > 0 else 1_000_000  # Y位置（デフォルト100万円）
        axes[0].text(
            0.1,  # X位置（左寄り）
            max_y,
            "Reference:\n1MXN: {0:,} JPY/year\n1ZAR: {1:,} JPY/year".format(MxnSwapPerYear, ZarSwapPerYear),
            fontsize=12,
            color="blue",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray")  # テキストボックスのスタイル
        )
    except Exception:
        pass  # テキスト描画のエラーを無視

    # 未運用スワップ収益のグラフ（右側）
    axes[1].plot(Years, NotUsedSwap, marker="s", label="Not Used Swap Income (Without Principal)", linewidth=2, color="orange")
    axes[1].set_title("Not Used Swap Income (Without Principal)", fontsize=16)
    axes[1].set_xlabel("Year", fontsize=14)
    axes[1].set_ylabel("Swap Income (JPY, in K)", fontsize=14)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisK))  # 縦軸をK単位でカンマ区切り
    axes[1].grid(True)  # グリッド表示
    axes[1].legend(fontsize=12)

    # レイアウトを調整して表示
    plt.tight_layout()
    plt.show()

# スワップ収益データを計算
DailySwap, CumulativeSwap = CalculateSwapGrowth()

# コンソールに最後の30日分の運用中スワップ収益（元本含む）を表示
print("\n運用中スワップ収益（元本含む：最後の30日分）:")
for i in range(max(0, len(DailySwap) - 30), len(DailySwap)):
    print("Day {0}: {1:,.0f}円".format(i + 1, DailySwap[i]))

# コンソールに最後の30日分の未運用スワップ収益（口座合計）を表示
print("\n未運用スワップ収益（口座合計：最後の30日分）:")
for i in range(max(0, len(CumulativeSwap) - 30), len(CumulativeSwap)):
    uninvested_swap = CumulativeSwap[i] - InitialInvestment  # 元本を差し引く
    print("Day {0}: {1:,.0f}円".format(i + 1, uninvested_swap))

# グラフ描画
PlotSwapData(DailySwap, CumulativeSwap)
