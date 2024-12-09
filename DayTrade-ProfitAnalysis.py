"""
【スワップポイント＆デイトレード収益計算プログラムの使い方】

このプログラムは、運用中及び未運用のスワップポイントとデイトレード収益を計算し、そのトレンドをグラフとして可視化するツールです。
プログラムを実行することで、運用状況を理解しやすくなります。

プログラムファイル名: "SwapPointProfitAnalysis.py"

【機能】
●入力された設定値に基づいたスワップポイント収益を日次で計算する機能（初期投資額の半分を運用）。
●入力された設定値に基づいたデイトレード収益を日次で計算する機能。
●入力された設定値に基づいた一定期間毎の追加投資処理機能（半分を運用）。
●入力された設定値に基づいた、通貨毎のロットの配分比率の算出機能と、その比率に基づいて増資の配分や未運用残高の配分を計算する機能。
●目標証拠金維持率を超過した場合に、余剰資金を運用残高に移動する機能。
●日次リスク要因「1. デイトレードの取引回数の内、何回かで損失発生」「2. 時間帯によるボラティリティリスクを適用」「3. 年に二回大損失が発生」を計算する機能。
●所得税課税処理機能（シミュレーションを行う設定年数毎に課税処理。税率は損益通算収益に準じたもの）。

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
これで準備完了です。プログラムを実行して収益計算を体験してください！

---
【ライセンス】
# このスクリプトは matplotlib ライブラリを利用しています。
# matplotlib は BSD スタイルの Matplotlib License でライセンスされています。
# 詳細: https://matplotlib.org/stable/users/license.html

---
【注意】
シミュレーションには、一般常識に基づく現実的に起きうる損失リスクを、少し拡大した割合で設定してあります。このリスクはランダムな発生率によって適用されます。
従って、設定値が同じでもシミュレーション結果は毎回微妙に異なるものになる可能性があります。

---
【初期設定】
以下の説明に従って初期設定値を入力してください。
"""
# 【初期投資額（円）】
# このプログラムで運用を開始するための最初の投資金額を指定します。
# 初期投資額の 50% を運用資金として使用し、スワップポイント収益の計算に利用します。
# 残りの 50% は未運用分（元本）として管理され、課税対象外として扱われます。
# この分割は、証拠金維持率を充分に確保し、強制ロスカットのリスクを軽減するために行われます。
InitialInvestmentYen = 768000

# 【各通貨の一日当たりのスワップポイント（円）】
# MXN/JPY（メキシコ・ペソ）と ZAR/JPY（南アフリカ・ランド）の通貨ペアで、1ロット当たりの1日毎に得られるスワップポイントを設定します。
MxnSwapPerDay = 21
ZarSwapPerDay = 17

# 【1ロット購入に必要な金額】
# 各通貨の1ロット（DMM FX の場合：1万通貨）を購入するために必要な日本円の金額を指定します。
# この値は実際の為替レートを基に設定され、再投資や追加投資のロット数計算に使用されます。
Mxn1LotCost = 2972  # MXN/JPY
Zar1LotCost = 3328  # ZAR/JPY
# 1ロット購入金額がレバレッジ適用後の価格である場合は以下を True、そうでなければ False にします。
# レバレッジが適用されていない場合、1通貨の対円価格を最小取引単位倍した価格が1ロットの購入に必要な価格とほとんど等しくなります。
# 1ロットの購入に必要な金額が上記計算結果よりも大きく小さい場合、レバレッジが適用されています。
LotCostLeveraged = True

# 【レバレッジ】
# 適用するレバレッジの倍率を整数で設定します（25倍なら25）。
Leverage = 25

# 【初期ロット数】
# 最初に購入するロット数を通貨ペア毎に設定します。このロット数に基づいてスワップポイント収益が計算されます。
# 注意：レバレッジを参考に小さな値から計算を始めてください。この値を基に初期の必要証拠金が計算されます。
MxnLots = 100  # MXN/JPY のロット数
ZarLots = 0  # ZAR/JPY のロット数

# 【証拠金維持率の目標値（%）】
# このプログラムで運用を効率化するための目標となる証拠金維持率を設定します。証拠金維持率がこの値を超えた場合、未運用残高の一部を運用資金として振り分けます。
# この設定により、運用効率を最大化し、未運用資金の過剰な蓄積を防ぎます。目標値は適切な安全域を考慮して調整することが推奨されます。
MarginMaintenanceTarget = 300  # 証拠金維持率目標値（パーセントを整数で入力。300% なら 300）

# 【デイトレード設定】
# 総口座残高の何％をデイトレードに使用するかを設定します（パーセントを整数で入力。100% なら 100）。
# デイトレードをしない場合は 0 と設定します。
DayTradingInvestmentRatio = 100

# 【デイトレードによる予想追加収入（円/日）】
# 毎日デイトレードを行うことで得られると想定される追加収入を設定します。この値はスワップポイント収益に加算され、総収益の予測計算に使用されます。
# デイトレードの実績や市場状況に応じてこの値を調整することが推奨されます。
ExpectedDailyTradeProfitInputYen = 30000  # 1日当たりのデイトレードによる予想追加収益（円/日）

# 【追加投資設定】
# 【毎月投入する追加投資額（円）】
# 毎月26日に投入する追加投資額を指定します。
# この設定は、日本の最も一般的な給料日を想定しており、給与が支払われるタイミングで、一部の資金を追加投資に充当する前提で計算を行います。
# 実際の日本の最も一般的な給料日は25日ですが、26日を投入日とすることで、資金投入の判断を行う時間を確保することを目的としています。
# MXN/JPY 及び ZAR/JPY のロット比率に基づいてこの金額の半分を運用に回し、新たなロットを購入します。
MonthlyInvestment = 0  # 次の偶数月の設定と同時設定が可能です。

# 【偶数月に投入する追加投資額（円）】
# 偶数月16日に投入する追加投資額を指定します。
# この設定は、日本の年金受給者を想定しており、偶数月（2月、4月、6月……）に年金が支給されるタイミングで、一部の資金を追加投資に充当する前提で計算を行います。
# 実際の日本の公的年金は「偶数月の15日」に支給されますが、16日を投入日とすることで、資金投入の判断を行う時間を確保することを目的としています。
# MXN/JPY 及び ZAR/JPY のロット比率に基づいてこの金額の半分を運用に回し、新たなロットを購入します。
BiMonthlyInvestment = 50000  # 前の毎月の設定と同時設定が可能です。

# 【年間収益がこの金額に達すると追加投資を中止】
# 障害年金受給者を想定し、年収が 370 万円を超えると障害年金の支給が半減、472 万円を超えると停止されるため、
# この金額を上限として追加投資を中止するよう設定しています。ただし、上限に達するまでに計画されている当年分の追加投資は実行されます。
# 注意：この設定項目に該当しない方は極端に大きな値を設定してください。
InvestmentIncomeLimit = 3700000

# 【シミュレーション年数】
Simulation = 1

# 初期設定を基に各種設定値をグローバル変数として設定し、後続のプログラムが参照可能にする関数
def InitializeGlobals():
    """
    コンソールベースの当プログラムにおいて、ユーザーが初期設定した情報を持つグローバル変数に基づいて、後続のプログラムが利用可能なグローバル変数を設定する関数。

    初期投資額が 0 の場合、コンソールにメッセージを出力してプログラムの実行を中止します。

    Parameters:
        なし。

    Returns:
        なし。
    """
    # グローバル変数を宣言
    global InvestmentForTrading, DayTradingInvestmentRatio, DayTradingInvestment, TradeProfitRate, ExpectedDailyTradeProfit, \
        MxnSwapPerYear, ZarSwapPerYear

    if InitialInvestmentYen > 0:  # 初期投資額が 1 以上であることを確認
        InvestmentForTrading = InitialInvestmentYen * 0.5  # 初期投資額の約半分をスワップポイント運用に使用し、残りを残高として設定
        # デイトレード使用金額率を少数に変換
        DayTradingInvestmentRatio = DayTradingInvestmentRatio / 100 if DayTradingInvestmentRatio > 0 else 0

        if DayTradingInvestmentRatio > 0:  # デイトレード使用金額率が 0 でないことを確認
            DayTradingInvestment = InitialInvestmentYen * DayTradingInvestmentRatio  # デイトレードに使用する金額を計算
            TradeProfitRate = ExpectedDailyTradeProfitInputYen / DayTradingInvestment \
                if ExpectedDailyTradeProfitInputYen > 0 else 0  # デイトレード利益率を計算
        else:  # デイトレード使用金額率が 0 の場合
            TradeProfitRate = 0  # デイトレード利益率を 0 に設定

        # 計算された日次デイトレード収益（円/日）
        ExpectedDailyTradeProfit = InitialInvestmentYen * DayTradingInvestmentRatio * TradeProfitRate
    else:  # 初期投資額が 0 の場合
        import sys  # システム操作に必要なモジュールをインポート
        print("初期投資金額が 0 に設定されています。プログラムの実行を中止しました。")
        sys.exit(1)  # プログラムの実行を中止し、終了コード 1 を返す

    # 各通貨ペアにおける、1ロット当たりの年間スワップ収益を計算
    MxnSwapPerYear = MxnSwapPerDay * 365  # MXN/JPY の年間スワップ収益
    ZarSwapPerYear = ZarSwapPerDay * 365  # ZAR/JPY の年間スワップ収益

# 日次スワップ収益を計算する関数
def CalculateDailySwap(CurrentMxnLots, CurrentZarLots, MxnSwapPerDay, ZarSwapPerDay):
    """
    現在のロット数とスワップポイントを基に日次スワップ収益を計算する関数。

    Args:
        CurrentMxnLots (int): MXN/JPY の現在のロット数。
        CurrentZarLots (int): ZAR/JPY の現在のロット数。
        MxnSwapPerDay (float): MXN/JPY の日次スワップポイント。
        ZarSwapPerDay (float): ZAR/JPY の日次スワップポイント。

    Returns:
        float: 日次のスワップ収益（JPY）。
    """
    MxnDailySwap = CurrentMxnLots * MxnSwapPerDay  # MXN/JPY の日次スワップ収益を計算
    ZarDailySwap = CurrentZarLots * ZarSwapPerDay  # ZAR/JPY の日次スワップ収益を計算
    return MxnDailySwap + ZarDailySwap  # 両通貨のスワップ収益を合計して返す

# 日次収益を計算する関数
def CalculateDailyIncome(LastSimulation = False):
    """
    日次収益を計算する関数。

    この関数は以下の二つの収益要素を計算し、合算します：
    1. スワップ収益：通貨ロット数及びスワップポイントに基づいて計算。
    2. デイトレード収益：初期デイトレード使用金額または運用資金の大きい方にデイトレード利益率を掛けた値を計算し、スワップ収益に加算。

    注意:
    - 必要な値は全てグローバル変数から取得します。
    - 日次収益 ("DailyIncome") と日次デイトレード収益 ("DailyInvestmentProfit") を計算します。

    Returns:
        None
    """
    global DailyIncome, DailyInvestmentProfit  # グローバル変数を宣言

    # 日次スワップ収益を計算する（補助関数を利用）
    DailyIncome = CalculateDailySwap(CurrentMxnLots, CurrentZarLots, MxnSwapPerDay, ZarSwapPerDay)

    # デイトレード分の収益を計算して追加
    # 初期デイトレード使用金額または必要証拠金の大きい方にデイトレード利益率を掛けて日次デイトレード収益を計算
    DailyInvestmentProfit = max(DayTradingInvestment, TotalInvestment) * TradeProfitRate \
        if LotCostLeveraged else max(DayTradingInvestment, TotalInvestment) * Leverage * TradeProfitRate
    DailyIncome += DailyInvestmentProfit  # デイトレード収益を日次収益に加算

import random  # ランダムな数値や確率的な要素を生成するための標準ライブラリ
# 日次リスク要素を適用する関数
def ApplyDailyRiskFactors(LastSimulation = False):
    """
    デイトレードのシミュレーションにおける日次リスク要素を適用する関数。

    この関数は以下の三つのリスク要素を考慮して収益や投資額を調整します：
    1. デイトレード中の一定確率での損失発生。
    2. 時間帯に応じたボラティリティリスクの変動。
    3. 年に二回発生する大損失。

    注意:
    - "DailyInvestmentProfit"、"Leverage"、"Day"、"TotalInvestment"、"RemainingReinvestment" はグローバル変数として使用されます。
    - 大損失部分では、損失率は既にレバレッジを考慮した値として計算されている前提です。

    Returns:
        None
    """
    global DailyIncome, DailyInvestmentProfit, Day, TotalInvestment, RemainingReinvestment  # グローバル変数を宣言

    # デイトレード中の一定確率での損失発生
    LossProbability = 0.175  # 損失発生確率（17.5%）
    LossRate = 0.095  # 損失額を日次収益の 9.5% とする
    if random.random() < LossProbability:  # 損失が発生するかどうかをランダムに決定
        DailyIncome -= DailyInvestmentProfit * LossRate * Leverage  # レバレッジ適用

    # 時間帯によるボラティリティリスクの適用
    if Day % 24 in range(9, 18):  # 日本時間の昼間（午前9時から午後6時）
        LowVolatilityLossRate = 0.02  # ボラティリティが低い場合の日次収益に対する損失（2%）
        DailyIncome -= DailyInvestmentProfit * LowVolatilityLossRate * Leverage  # レバレッジ適用

    # 年に二回発生する大損失の適用
    if Day in [91, 273]:  # 年間の91日目（3ヶ月後）と273日目（9ヶ月後）
        MajorLossRate = 0.3  # 資金の 30% を喪失する大損失
        TotalInvestment -= TotalInvestment * MajorLossRate  # 運用資金からレバレッジ考慮済みの損失額を減算
        RemainingReinvestment -= RemainingReinvestment * MajorLossRate  # 再投資残高からレバレッジ考慮済みの損失額を減算
        TotalInvestment = max(TotalInvestment, 0)  # 運用資金が負の値にならないように調整
        RemainingReinvestment = max(RemainingReinvestment, 0)  # 再投資残高が負の値にならないように調整

# 運用成績を計算する関数
def CalculateSwapAndTradingProfitGrowth():
    """
    スワップポイントとデイトレード収益を複利計算し、設定年分の日次収益データを生成します。
    偶数月の16日に追加投資を行い、日次の収益から再投資を行います。

    Returns:
        tuple: 日次、累積収益データを格納したリスト。
    """
    import math  # 最少公約数 (GCD) の計算など数学的な処理に使用するライブラリ
    # 補助関数：再投資処理
    def PerformReinvestment(DailyIncome, TotalInvestment, TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, Leverage,
        MarginMaintenanceTarget, RemainingReinvestment, AdditionalUnusedInvestment, UsedUnusedInvestment,
        CurrentMxnLots, CurrentZarLots, Mxn1LotCost, Zar1LotCost, MxnLotRatio, ZarLotRatio, TotalRatio):
        """
        再投資処理を行い、指定された通貨（MXN/JPY、ZAR/JPY）のロット数を追加購入する関数。

        この関数は日次収益（DailyIncome）の一部を再投資に充て、証拠金維持率の調整及び通貨ロットの購入を行います。
        投資資金の運用状況を動的に管理し、再投資残高やロット保有数などの状態を更新します。

        処理の詳細:
        1. 再投資額の計算及び加算:
        - 日次収益（DailyIncome）の 50% を再投資額として計算し、再投資残高（RemainingReinvestment）に加算します。

        2. 証拠金維持率の計算:
        - 現在の証拠金維持率を補助関数 "CalculateMarginMaintenanceRate()" を使用して計算します。
        - 計算には、運用残高、再投資残高、累積スワップ及びデイトレード収益、増資未運用残高などの情報を使用します。

        3. 証拠金維持率の調整:
        - 証拠金維持率が目標値を超えている場合、補助関数 "TransferFundsToReinvestment()" を呼び出し、
          未運用の「累積スワップ及びデイトレード収益」や「増資未運用残高」から再投資残高への資金移動を行います。
        - 資金移動後、再投資残高や運用済み「累積スワップ及びデイトレード収益」の状態が更新されます。

        4. 購入可能額の計算:
        - 再投資残高にレバレッジを不適用・適用し、購入可能額（AvailableFunds）を算出します。
        - 通貨毎のロット購入比率（MxnLotRatio、ZarLotRatio）に基づき、購入可能額を二つの通貨に分配します。

        5. ロット購入処理:
        - 割り当てられた購入可能額に基づき、以下の処理を繰り返します:
            - 1ロット分のコスト以上の資金がある場合に、購入可能なロット数を計算。
            - 計算したロット数を既存のロット保有数に加算。
            - 使用した金額を購入可能額及び再投資残高から減算。
            - 必要証拠金（TotalInvestment）を加算し、運用状況を反映。

        6. 計算結果の返却:
        - 更新された状態の各種変数を返します。

        注意:
        - レバレッジ適用の有無（LotCostLeveraged）は、購入可能額や残高の計算に影響します。
        - 証拠金維持率が高すぎる場合、運用効率が低下する可能性があるため、再投資の際には証拠金維持率の目標値を基準とした調整が行われます。

        Args:
            DailyIncome (float): 日次スワップ及びデイトレード収益。収益の 50% を再投資用の資金として充当。
            TotalInvestment (float): 運用残高（必要証拠金）。
            TotalCumulativeSwapAndTradingProfit (float): 「累積スワップ及びデイトレード収益」。
            UsedProfitForInvestment (float): 運用済み「累積スワップ及びデイトレード収益」。
            Leverage (int): レバレッジ。
            MarginMaintenanceTarget (int): 目標証拠金維持率（300% なら 300）。
            RemainingReinvestment (float): 再投資残高（運用残高の追加準備金、レバレッジ未適用）。残っている再投資用残高に日次収益の 50% を加算。
            AdditionalUnusedInvestment (float): 「増資未運用残高（累積）」。
            UsedUnusedInvestment (float): 運用済み「増資未運用残高（累積）」。
            CurrentMxnLots (int): 現在保有している MXN/JPY のロット数。
            CurrentZarLots (int): 現在保有している ZAR/JPY のロット数。
            Mxn1LotCost (float): 1ロット当たりの MXN/JPY の購入費用。
            Zar1LotCost (float): 1ロット当たりの ZAR/JPY の購入費用。
            MxnLotRatio (float): MXN のロット数比率。
            ZarLotRatio (float): ZAR のロット数比率。
            TotalRatio (float): MXN 及び ZAR のロット数比率の合計。

        Returns:
            tuple:
                - TotalInvestment (float): 更新後の運用残高（必要証拠金）。
                - RemainingReinvestment (float): 更新後の再投資残高（運用残高の追加準備金）。
                - UsedProfitForInvestment (float): 更新後の運用済み「累積スワップ及びデイトレード収益」。
                - UsedUnusedInvestment (float): 更新後の運用済み「増資未運用残高（累積）」。
                - CurrentMxnLots (int): 更新された MXN/JPY のロット数。
                - CurrentZarLots (int): 更新された ZAR/JPY のロット数。
        """
        # 補助関数：証拠金維持率を計算
        def CalculateMarginMaintenanceRate(TotalInvestment, RemainingReinvestment, MarginMaintenanceTarget,
            TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, AdditionalUnusedInvestment, UsedUnusedInvestment):
            """
            現在の証拠金維持率を計算する関数。

            この関数は、運用中の資金に対する口座全体の資金比率を計算し、整数のパーセント形式で証拠金維持率を返します。証拠金維持率は、運用中の資金がどの程度の
            安全性・余裕を持っているかを評価するための指標です。また、口座残高全体を内部で計算しますが、この関数ではその値を返しません。

            Args:
                TotalInvestment (float): 運用残高（必要証拠金）。
                RemainingReinvestment (float): 再投資残高（運用残高の追加準備金、レバレッジ未適用）。
                MarginMaintenanceTarget (int): 目標証拠金維持率（300% なら 300）。
                TotalCumulativeSwapAndTradingProfit (float): 「累積スワップ及びデイトレード収益」。
                UsedProfitForInvestment (float): 運用済み「累積スワップ及びデイトレード収益」。
                AdditionalUnusedInvestment (float): 「増資未運用残高（累積）」。
                UsedUnusedInvestment (float): 運用済み「増資未運用残高（累積）」。

            Returns:
                int: 現在の証拠金維持率（整数のパーセント形式。例：300% なら 300）。
                    - 証拠金維持率が計算できない場合（総資産がゼロの場合）は目標値から1を引いた数を返します。

            Note:
                証拠金維持率が高すぎる場合、運用効率が低下する可能性があります。この関数の戻り値を利用して、未運用残高を適切に再投資残高に振り分ける処理を
                行うことが推奨されます。
            """
            # 利用可能な未運用残高を計算
            ProfitAvailable = TotalCumulativeSwapAndTradingProfit - UsedProfitForInvestment  # 累計から運用中金額を差し引く
            AdditionalAvailable = AdditionalUnusedInvestment - UsedUnusedInvestment  # 累計から運用中金額を差し引く
            AvailableFunds = ProfitAvailable + AdditionalAvailable  # 未運用残高を合算

            AccountTotalBalance = TotalInvestment + RemainingReinvestment + AvailableFunds  # 総口座残高を計算

            if AccountTotalBalance > 0:  # 証拠金維持率を計算（ゼロ除算防止）
                MarginMaintenanceRate = int((TotalInvestment / AccountTotalBalance) * 100)  # 必要証拠金 / 総口座残高 * 100（整数の％にする）
            else:  # 総資産がゼロの場合
                MarginMaintenanceRate = MarginMaintenanceTarget - 1  # 目標証拠金維持率から 1 を引いた数を代入

            return MarginMaintenanceRate  # 証拠金維持率を返す

        # 補助関数：未運用残高から再投資残高への資金移動
        def TransferFundsToReinvestment(TotalInvestment, MarginMaintenanceRate, MarginMaintenanceTarget,
            RemainingReinvestment, TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment,
            AdditionalUnusedInvestment, UsedUnusedInvestment):
            """
            未運用累積スワップ及びデイトレード収益、増資未運用残高から再投資残高に資金を移動する関数。

            現在の証拠金維持率が目標値を超えている場合、目標維持率へ向けて調整が必要な金額を計算し、未運用累積スワップ及びデイトレード収益や増資未運用残高を
            用いて再投資残高に移動します。移動後は、累積スワップ及びデイトレード収益部分と増資部分の値を適切に更新します。

            Args:
                TotalInvestment (float): 運用残高（必要証拠金）。
                MarginMaintenanceRate (float): 現在の証拠金維持率。
                MarginMaintenanceTarget (int): 目標証拠金維持率（300% なら 300）。
                RemainingReinvestment (float): 再投資残高（運用残高の追加準備金、レバレッジ未適用）。
                TotalCumulativeSwapAndTradingProfit (float): 「累積スワップ及びデイトレード収益」。
                UsedProfitForInvestment (float): 運用済み「累積スワップ及びデイトレード収益」。
                AdditionalUnusedInvestment (float): 「増資未運用残高（累積）」。
                UsedUnusedInvestment (float): 運用済み「増資未運用残高（累積）」。

            Returns:
                tuple: (RemainingReinvestment, UsedProfitForInvestment, UsedUnusedInvestment)
                    - 更新後の再投資残高。
                    - 更新後の運用済み「累積スワップ及びデイトレード収益」。
                    - 更新後の運用済み「増資未運用残高（累積）」。

            Note:
                この関数はリスク要素や損失が適用された後に実行されるため、未運用スワップ及びデイトレード収益や増資未運用残高の範囲内で資金移動を行うことが保証
                されています。
            """
            # 目標維持率へ向けて調整するために移動が必要な金額を計算
            ExcessMargin = TotalInvestment * (MarginMaintenanceRate / MarginMaintenanceTarget) - TotalInvestment
            """
            ExcessMargin:
            - 現在の必要証拠金（TotalInvestment）に基づき、目標維持率（MarginMaintenanceTarget）へ向けて調整が必要な金額を計算します。
            - 例: TotalInvestment = 100,000, MarginMaintenanceRate = 400, MarginMaintenanceTarget = 300 の場合、
              ExcessMargin = 100,000 * (400 / 300) - 100,000 = 33,333.33
            """

            # 利用可能な未運用残高を計算（累積スワップ及びデイトレード収益、増資未運用残高）
            ProfitAvailable = TotalCumulativeSwapAndTradingProfit - UsedProfitForInvestment
            AdditionalAvailable = AdditionalUnusedInvestment - UsedUnusedInvestment
            AvailableUnusedFunds = ProfitAvailable + AdditionalAvailable
            """
            AvailableUnusedFunds:
            - 現在利用可能な合計未運用残高を計算します。
            - ProfitAvailable: 未運用「累積スワップ及びデイトレード収益」。
            - AdditionalAvailable: 未運用「増資未運用残高」。
            - 例: ProfitAvailable = 20,000, AdditionalAvailable = 10,000 の場合、AvailableUnusedFunds = 30,000
            """

            TransferAmount = min(ExcessMargin, AvailableUnusedFunds)  # 実際に移動可能な金額を計算
            """
            TransferAmount:
            - 実際に再投資残高に移動する金額を決定します。
            - ExcessMargin と AvailableUnusedFunds の小さい方を選択します。
            - 例: ExcessMargin = 25,000, AvailableUnusedFunds = 30,000 の場合、TransferAmount = 25,000
            """

            RemainingReinvestment += TransferAmount  # 再投資残高に移動金額を加算
            """
            RemainingReinvestment:
            - 再投資残高に移動金額（TransferAmount）を加算します。
            - 例: RemainingReinvestment = 50,000, TransferAmount = 25,000 の場合、再投資残高は 75,000 になります。
            """

            # TransferAmount を累積スワップ及びデイトレード収益部分と増資部分に割り当て
            ProfitContribution = TransferAmount if TransferAmount <= ProfitAvailable else ProfitAvailable
            """
            ProfitContribution:
            - TransferAmount のうち、未運用「累積スワップ及びデイトレード収益」から使用可能な金額を表します。
            - ProfitAvailable を超えない範囲で全額充当します。
            - 例: TransferAmount = 25,000, ProfitAvailable = 20,000 の場合、ProfitContribution = 20,000
            """

            AdditionalContribution = TransferAmount - ProfitContribution
            """
            AdditionalContribution:
            - TransferAmount のうち、未運用「増資未運用残高」から補填する金額を表します。
            - ProfitAvailable が TransferAmount に満たない場合、その不足分を全額補います。
            - 例: TransferAmount = 25,000, ProfitContribution = 20,000 の場合、AdditionalContribution = 5,000
            """

            # 運用済み「累積スワップ及びデイトレード収益」と運用済み「増資未運用残高」を記録
            UsedProfitForInvestment += ProfitContribution
            """
            UsedProfitForInvestment:
            - 再投資に使用した「累積スワップ及びデイトレード収益」の金額を記録します。
            """

            UsedUnusedInvestment += AdditionalContribution
            """
            UsedUnusedInvestment:
            - 再投資に使用した「増資未運用残高」の金額を記録します。
            """

            return RemainingReinvestment, UsedProfitForInvestment, UsedUnusedInvestment  # 計算結果を返す

        """ PerformReinvestment() の記述 """
        Reinvestment = DailyIncome * 0.5  # 再投資額を日次収益の 50% として計算
        RemainingReinvestment += Reinvestment  # 再投資額を再投資残高に加算

        # 証拠金維持率を計算（補助関数を利用）
        MarginMaintenanceRate = CalculateMarginMaintenanceRate(TotalInvestment, RemainingReinvestment, MarginMaintenanceTarget,
            TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, AdditionalUnusedInvestment, UsedUnusedInvestment)

        # 証拠金維持率が目標値を超えている場合、未運用累積スワップ及びデイトレード収益、増資未運用残高から再投資残高に資金を移動（補助関数を利用）
        if MarginMaintenanceRate > MarginMaintenanceTarget:
            RemainingReinvestment, UsedProfitForInvestment, UsedUnusedInvestment = TransferFundsToReinvestment(TotalInvestment,
                MarginMaintenanceRate, MarginMaintenanceTarget, RemainingReinvestment,
                TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, AdditionalUnusedInvestment, UsedUnusedInvestment)

        # ロット購入処理
        if TotalRatio > 0:  # ロットの比率の合計が 1 以上であることを確認
            MxnReinvestment = RemainingReinvestment * (MxnLotRatio / TotalRatio)  # 再投資残高を比率で分配
            ZarReinvestment = RemainingReinvestment * (ZarLotRatio / TotalRatio)  # 再投資残高を比率で分配
        else:
            MxnReinvestment = ZarReinvestment = 0  # 比率がない場合は 0

        # 再投資残高にレバレッジを不適用・適用して取引可能金額を算出
        AvailableFunds = RemainingReinvestment if LotCostLeveraged else RemainingReinvestment * Leverage

        while AvailableFunds >= Mxn1LotCost or AvailableFunds >= Zar1LotCost:  # 取引可能金額が取引不能金額になるまでのロット購入ループ
            if AvailableFunds >= Mxn1LotCost and MxnReinvestment > 0:  # MXN ロットの購入処理
                LotsToBuy = int(AvailableFunds // Mxn1LotCost)  # 購入可能なロット数を計算
                CurrentMxnLots += LotsToBuy  # MXN ロット数を増加
                UsedFunds = LotsToBuy * Mxn1LotCost  # 使用した資金を計算
                AvailableFunds -= UsedFunds  # 使用分を取引可能金額から減算
                MxnReinvestment -= UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 再投資残高から使用した金額を減算
                RemainingReinvestment -= UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 実際に使用した再投資残高を減算
                TotalInvestment += UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 必要証拠金を加算

            if AvailableFunds >= Zar1LotCost and ZarReinvestment > 0:  # ZAR ロットの購入処理
                LotsToBuy = int(AvailableFunds // Zar1LotCost)  # 購入可能なロット数を計算
                CurrentZarLots += LotsToBuy  # ZAR ロット数を増加
                UsedFunds = LotsToBuy * Zar1LotCost  # 使用した資金を計算
                AvailableFunds -= UsedFunds  # 使用分を取引可能金額から減算
                ZarReinvestment -= UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 再投資残高から使用した金額を減算
                RemainingReinvestment -= UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 実際に使用した再投資残高を減算
                TotalInvestment += UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 必要証拠金を加算

        # 計算結果を返す
        return TotalInvestment, RemainingReinvestment, UsedProfitForInvestment, UsedUnusedInvestment, CurrentMxnLots, CurrentZarLots

    # 補助関数：毎月26日または偶数月16日またはその両方の追加投資処理
    def PerformMonthlyInvestment(Day, TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, Mxn1LotCost, Zar1LotCost,
        MxnLotRatio, ZarLotRatio, TotalRatio, Leverage, CurrentMxnLots, CurrentZarLots):
        """
        毎月26日または偶数月16日またはその両方で追加投資を行い、その投資額を基に再投資を実施する関数。

        この関数は以下の処理を順序立てて行います：

        1. 追加投資の実施
        - 毎月26日または偶数月16日またはその両方（シミュレーション内で指定された条件の日付）で追加投資を行います。
        - 投資額を以下の二つに分配します：
            - 再投資残高（RemainingReinvestment）：投資額の半分を運用準備金として加算。
            - 増資未運用残高（AdditionalUnusedInvestment）：投資額の半分を未運用の増資金額として記録。

        2. 購入可能額の計算
        - 再投資残高にレバレッジを適用して、必要証拠金ベースでの購入可能額を算出します。
        - ロットコストへのレバレッジ適用の有無（LotCostLeveraged）に基づき、以下を使用します：
            - 再投資残高そのもの。
            - またはレバレッジ適用後の金額。

        3. 通貨毎の割り当て処理
        - MXN/JPY と ZAR/JPY のロット購入比率（MxnLotRatio、ZarLotRatio）に基づき、購入可能額を二つの通貨に分配。
        - 比率が未定義の場合、分配金額は0とする。

        4. ロット購入処理
        - 割り当てられた購入可能額に基づき以下を実行：
            - 購入可能額が1ロット分のコスト以上の場合、購入可能なロット数を計算。
            - 計算したロット数を既存のロット保有数に加算。
            - 使用した金額を購入可能額及び再投資残高から減算。
            - 必要証拠金（TotalInvestment）を更新し、使用された金額をレバレッジの有無に応じて調整して加算。

        5. 再投資残高の更新
        - 購入処理後、再投資残高（RemainingReinvestment）を適切に更新します。
        - レバレッジの適用有無（LotCostLeveraged）を考慮して計算。

        注意:
        - この関数は、シミュレーション内で資金管理及び運用戦略のロジックを担い、指定されたルールに従って動的に資金とロット数を更新します。
        - レバレッジの設定や追加投資額の値は、運用結果に大きな影響を与えるため正確な設定が必要です。

        Args:
            Day (int): 経過日数。偶数月16日かどうかを判定するために使用。
            TotalInvestment (float): 運用残高（必要証拠金）。
            RemainingReinvestment (float): 再投資残高（運用残高の追加準備金、レバレッジ未適用）。
            AdditionalUnusedInvestment (float): 「増資未運用残高（累積）」。
            Mxn1LotCost (float): 1ロット当たりの MXN/JPY の購入費用。
            Zar1LotCost (float): 1ロット当たりの ZAR/JPY の購入費用。
            MxnLotRatio (float): MXN への投資比率。
            ZarLotRatio (float): ZAR への投資比率。
            TotalRatio (float): MXN 及び ZAR のロット数比率の合計。
            Leverage (float): レバレッジ倍率。
            CurrentMxnLots (int): 現在保有している MXN/JPY のロット数。
            CurrentZarLots (int): 現在保有している ZAR/JPY のロット数。

        Returns:
            tuple:
                - TotalInvestment (float): 更新後の運用残高（必要証拠金）。
                - RemainingReinvestment (float): 更新後の再投資残高（運用残高の追加準備金）。
                - AdditionalUnusedInvestment (float): 更新後の「増資未運用残高（累積）」。
                - CurrentMxnLots (int): 更新後の MXN/JPY ロット数。
                - CurrentZarLots (int): 更新後の ZAR/JPY ロット数。
        """
        # 補助関数：外部関数のコアロジック
        def ProcessInvestment():
            """
            再投資残高に基づき、利用可能な証拠金を計算し、比率に従って MXN 及び ZAR に投資を行う関数。

            この関数は以下の処理を行います：
            1. レバレッジの有無に応じた利用可能資金の計算。
            2. 比率に基づく投資金額の割り当て。
            3. MXN 及び ZAR へのロット単位での投資。
            4. 購入後の再投資残高の計算。

            必要な変数は "nonlocal" キーワードを用いて外部スコープから参照及び変更します。

            Returns:
                None
            """
            nonlocal RemainingReinvestment, TotalInvestment, CurrentMxnLots, CurrentZarLots  # 外部スコープの変数を参照

            # 再投資残高にレバレッジを不適用・適用して取引可能金額を算出
            AvailableFunds = RemainingReinvestment if LotCostLeveraged else RemainingReinvestment * Leverage

            if TotalRatio > 0:  # 比率に基づいて購入可能額を分配（比率が定義されている場合のみ処理）
                MxnAvailableFunds = AvailableFunds * (MxnLotRatio / TotalRatio)  # MXN への割り当て金額
                ZarAvailableFunds = AvailableFunds * (ZarLotRatio / TotalRatio)  # ZAR への割り当て金額
            else:
                MxnAvailableFunds = ZarAvailableFunds = 0  # 比率が 0 の場合、割り当て金額も 0

            # MXN への投資処理
            if MxnAvailableFunds >= Mxn1LotCost:  # MXN 割り当て金額が1ロット購入費用以上の場合
                LotsToBuy = int(MxnAvailableFunds // Mxn1LotCost)  # 購入可能な MXN のロット数を整数で計算
                CurrentMxnLots += LotsToBuy  # 保有中の MXN ロット数に購入分を追加
                UsedFunds = LotsToBuy * Mxn1LotCost  # 実際に使用する金額を計算
                AvailableFunds -= UsedFunds  # 使用済み金額を利用可能な証拠金から差し引き
                TotalInvestment += UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 必要証拠金に加算

            # ZAR への投資処理
            if ZarAvailableFunds >= Zar1LotCost:  # ZAR 割り当て金額が1ロット購入費用以上の場合
                LotsToBuy = int(ZarAvailableFunds // Zar1LotCost)  # 購入可能な ZAR のロット数を整数で計算
                CurrentZarLots += LotsToBuy  # 保有中の ZAR ロット数に購入分を追加
                UsedFunds = LotsToBuy * Zar1LotCost  # 実際に使用する金額を計算
                AvailableFunds -= UsedFunds  # 使用済み金額を利用可能な証拠金から差し引き
                TotalInvestment += UsedFunds if LotCostLeveraged else UsedFunds / Leverage  # 必要証拠金に加算

            # 購入後の再投資残高を計算
            RemainingReinvestment = AvailableFunds if LotCostLeveraged else AvailableFunds / Leverage

        """ PerformMonthlyInvestment() の記述 """
        # 毎月26日に追加投資を行う
        if Day % 30 == 26:  # 毎月26日かどうかを判定
            RemainingReinvestment += MonthlyInvestment * 0.5  # 追加投資額の半分を再投資残高に加算
            AdditionalUnusedInvestment += MonthlyInvestment * 0.5  # 追加投資額の半分を未運用残高に加算
            ProcessInvestment()  # 補助関数を利用して、再投資残高に基づき、利用可能な証拠金を計算し、比率に従って MXN 及び ZAR に投資を行う

        # 偶数月16日に追加投資を行う
        if Day % 30 == 15 and (Day // 30 + 1) % 2 == 0:  # 偶数月16日かどうかを判定
            RemainingReinvestment += BiMonthlyInvestment * 0.5  # 追加投資額の半分を再投資残高に加算
            AdditionalUnusedInvestment += BiMonthlyInvestment * 0.5  # 追加投資額の半分を未運用残高に加算
            ProcessInvestment()  # 補助関数を利用して、再投資残高に基づき、利用可能な証拠金を計算し、比率に従って MXN 及び ZAR に投資を行う

        return TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, CurrentMxnLots, CurrentZarLots  # 更新後の状態を返す

    # 補助関数：税金を計算
    def CalculateTaxableIncome(Income):
        """
        所得金額に基づき、日本の所得税を税率のみで計算する関数。所得控除は考慮しません。

        Args:
            Income (float): 課税対象となる総収益金額（JPY）

        Returns:
            float: 税金引き後の収益金額（JPY）
        """
        if Income <= 1_949_000:  # 1,949,000 円以下の所得に適用される税率
            TaxRate = 0.05  # 税率：5%
        elif Income <= 3_299_000:  # 3,299,000 円以下の所得に適用される税率
            TaxRate = 0.10  # 税率：10%
        elif Income <= 6_949_000:  # 6,949,000 円以下の所得に適用される税率
            TaxRate = 0.20  # 税率：20%
        elif Income <= 8_999_000:  # 8,999,000 円以下の所得に適用される税率
            TaxRate = 0.23  # 税率：23%
        elif Income <= 17_999_000:  # 17,999,000 円以下の所得に適用される税率
            TaxRate = 0.33  # 税率：33%
        elif Income <= 39_999_000:  # 39,999,000 円以下の所得に適用される税率
            TaxRate = 0.40  # 税率：40%
        else:  # それ以上の所得に適用される税率
            TaxRate = 0.45  # 税率：45%

        TaxAmount = Income * TaxRate  # 税額を計算
        return Income - TaxAmount  # 税金引き後の収益金額を返す

    """ CalculateSwapAndTradingProfitGrowth() の記述 """
    # 初期必要証拠金計算のために、設定されたロット数と1ロットのコスト、レバレッジを使用
    InitialRequiredMargin = ((Mxn1LotCost * MxnLots) + (Zar1LotCost * ZarLots))  # 1ロットのコストにロット数をかけて運用中の金額を算出
    if not LotCostLeveraged:  # 1ロット当たりのコストにレバレッジが適用されていない場合
        InitialRequiredMargin = InitialRequiredMargin / Leverage  # 必要証拠金をレバレッジで割って求める

    # 初期化：グローバル変数を宣言
    global TotalInvestment, RemainingReinvestment, TotalCumulativeSwapAndTradingProfit, Day, DailyIncome, DailyInvestmentProfit, \
        CurrentMxnLots, CurrentZarLots

    # 初期化：各種変数
    TotalInvestment = InitialRequiredMargin  # 初期必要証拠金を運用残高として代入
    UnusedInvestment = InvestmentForTrading  # 初期未運用残高を設定
    RemainingReinvestment = 0  # 再投資残高を初期化
    AdditionalUnusedInvestment = 0  # 増資未運用残高を初期化
    TotalCumulativeSwapAndTradingProfit = 0  # 累積スワップ及びデイトレード収益を初期化
    PreviousCumulativeSwapAndTradingProfit = 0  # 前年の累積スワップ及びデイトレード収益を記録する変数を初期化
    UsedProfitForInvestment = 0  # 運用済み「累積スワップ及びデイトレード収益」を初期化
    UsedUnusedInvestment = 0  # 運用済み「増資未運用残高」を初期化
    CurrentMxnLots = MxnLots  # MXN/JPY の初期ロット数
    CurrentZarLots = ZarLots  # ZAR/JPY の初期ロット数

    # グラフ描画用日次データの記録用リスト
    DailySwapAndTradingProfit = []  # "日次の" 運用残高を記録するリストを初期化
    CumulativeSwapAndTradingProfit = []  # "日次の" 累積スワップ及びデイトレード収益を記録するリストを初期化
    # 初期値を設定
    DailySwapAndTradingProfit.append(TotalInvestment)  # 初期必要証拠金を累積投資リストの最初に追加
    CumulativeSwapAndTradingProfit.append(UnusedInvestment)  # 初期未運用残高を累積スワップ及びデイトレード収益リストの最初に追加

    # 現在の MXN ロット数と ZAR ロット数に基づき、最小公約数（GCD）を計算して比率を求める
    GCD = math.gcd(int(CurrentMxnLots), int(CurrentZarLots))  # ロット数を整数に変換して GCD を計算
    if GCD > 0:
        MxnLotRatio = int(CurrentMxnLots) // GCD  # 最小公約数で割って比率を計算
        ZarLotRatio = int(CurrentZarLots) // GCD  # 最小公約数で割って比率を計算
    else:
        MxnLotRatio = ZarLotRatio = 0  # GCD が 0 の場合、比率は 0 に設定
    TotalRatio = MxnLotRatio + ZarLotRatio  # 両者の比率の合計を求める

    # メインロジック
    for Day in range(1, Simulation * 365 + 1):  # 設定年分の日次計算を行うループを開始
        # 日次スワップ収益とデイトレード収益を計算（初期デイトレード使用金額または必要証拠金の大きい方にデイトレード利益率を掛けて日次デイトレード収益を計算）
        CalculateDailyIncome()  # 必要な値は全てグローバル変数として定義

        # 日次リスク要素を適用
        ApplyDailyRiskFactors()  # 必要な値は全てグローバル変数として定義

        # 再投資処理（補助関数を利用）
        TotalInvestment, RemainingReinvestment, UsedProfitForInvestment, UsedUnusedInvestment, CurrentMxnLots, CurrentZarLots = \
        PerformReinvestment(DailyIncome, TotalInvestment, TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, Leverage,
            MarginMaintenanceTarget, RemainingReinvestment, AdditionalUnusedInvestment, UsedUnusedInvestment,
            CurrentMxnLots, CurrentZarLots, Mxn1LotCost, Zar1LotCost, MxnLotRatio, ZarLotRatio, TotalRatio)

        # 追加投資処理（補助関数を利用）
        TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, CurrentMxnLots, CurrentZarLots = \
        PerformMonthlyInvestment(Day, TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, Mxn1LotCost, Zar1LotCost,
            MxnLotRatio, ZarLotRatio, TotalRatio, Leverage, CurrentMxnLots, CurrentZarLots)

        # 累積スワップ及びデイトレード収益を更新
        TotalCumulativeSwapAndTradingProfit += DailyIncome  # デイトレード収益を含む日次収益を各種未運用残高に加算

        if Day % 365 == 0:  # 年次税金処理
            CurrentYear = Day // 365  # 現在の年数（1年目、2年目、3年目……）

            if Day == 365:  # 最初の年の税金計算
                TaxableIncome = TotalCumulativeSwapAndTradingProfit - CumulativeSwapAndTradingProfit[0]  # 未運用分元本を無視
            else:  # 二年目以降の税金計算
                TaxableIncome = TotalCumulativeSwapAndTradingProfit - PreviousCumulativeSwapAndTradingProfit  # 当年分の収益

            # 増資額を課税対象から減算（当年分を計算）
            TaxExemptInvestment = AdditionalUnusedInvestment / CurrentYear  # 累積増資額を当年分に分配
            TaxableIncome -= TaxExemptInvestment  # 課税対象収益から当年増資額を控除
            TaxableIncome = max(0, TaxableIncome)  # 課税対象が負になることを防ぐ

            # 税金適用後の累積スワップ及びデイトレード収益を計算（補助関数を利用）
            TotalCumulativeSwapAndTradingProfit = CalculateTaxableIncome(TaxableIncome)

            # 前年度の累積スワップ及びデイトレード収益を更新
            PreviousCumulativeSwapAndTradingProfit = TotalCumulativeSwapAndTradingProfit

        # 日次データを記録
        DailySwapAndTradingProfit.append(TotalInvestment)  # 運用残高を記録
        CumulativeSwapAndTradingProfit.append(TotalCumulativeSwapAndTradingProfit)  # 累積スワップ及びデイトレード収益を記録

    return DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit  # 計算結果を返す

# グラフを描画する関数
def PlotSwapData(DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit):
    """
    スワップ収益とデイトレード収益の運用中と未運用のトレンドを別々のグラフに描画します（設定年分）。

    Args:
        DailySwapAndTradingProfit (list): 日次スワップ収益＋デイトレード収益のデータ（運用中、元本の半分を含む）。
        CumulativeSwapAndTradingProfit (list): 累積スワップ収益＋デイトレード収益のデータ（未運用、元本の半分を含む利益）。
    """
    import matplotlib.pyplot as plt  # グラフの描画やデータの視覚化を行うためのライブラリ
    import matplotlib.ticker as mticker  # グラフの軸ラベルや目盛りのカスタマイズに使用するモジュール

    # 日次データを年次データに変換
    DaysPerYear = 365  # 1年の日数
    Years = [day / DaysPerYear for day in range(1, len(DailySwapAndTradingProfit) + 1)]  # 年単位の X 軸

    # 未運用スワップ及びデイトレード収益を計算
    NotUsed = [
        cumulative - InvestmentForTrading  # 初期投資額の 50% を差し引く
        for cumulative in CumulativeSwapAndTradingProfit]

    # フォーマッター関数: 金額を "K" 単位に変換しカンマ区切りを追加
    def FormatYAxisK(Value, _):
        return f"{int(Value // 1_000):,}K"  # 1,000 で割りカンマ区切りで "K" を付与

    # グラフウィンドウを作成（1行2列のサブプロット）
    fig, axes = plt.subplots(1, 2, figsize = (16, 6))  # 1行2列の配置

    # 運用中残高のグラフ（左側）
    # 未運用残高をプロットし、凡例に「Total Investment Amount (With 50% Principal)」を設定
    axes[0].plot(Years, DailySwapAndTradingProfit, marker = "o", label = "Total Investment Amount (With 50% Principal)", linestyle = "--")
    axes[0].set_title("Total Investment Amount (With 50% Principal)", fontsize = 16)
    axes[0].set_xlabel("Year (already taxed)", fontsize = 14)
    axes[0].set_ylabel("In Use Swap & Day Trading Income (JPY, in K)", fontsize = 14)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisK))  # 縦軸を "K" 単位でカンマ区切り
    axes[0].grid(True)  # グリッド表示
    axes[0].legend(fontsize = 12)

    # 未運用残高のグラフ（右側）
    axes[1].plot(
        # 未運用残高をプロットし、凡例に「Unused Total Assets (Without 50% Principal)」を設定
        Years, NotUsed, marker = "s", label = "Unused Total Assets (Without 50% Principal)", linewidth = 2, color = "orange")
    axes[1].set_title("Unused Total Assets (Without 50% Principal)", fontsize = 16)  # グラフタイトルを設定
    axes[1].set_xlabel("Year (already taxed)", fontsize = 14)  # X 軸ラベルを設定
    axes[1].set_ylabel("Not Used Swap & Day Trading Income (JPY, in K)", fontsize = 14)  # Y 軸ラベルを設定
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisK))  # Y 軸の数値を "K" 単位でカンマ区切り表示にする
    axes[1].grid(True)  # グリッドを表示
    axes[1].legend(fontsize = 12)  # 凡例を設定

    # 各種参考値をグラフ内に表示
    try:
        # 左右グラフのスケールを統一
        axes[0].set_ylim(0, max(DailySwapAndTradingProfit) * 1.2)  # 左グラフの Y 軸範囲を設定（最大値の 120% を上限）
        axes[1].set_ylim(0, max(NotUsed) * 1.2)  # 右グラフの Y 軸範囲を設定（最大値の 120% を上限）
        # 左右グラフのそれぞれで最大値を再計算
        MaxYleft = max(DailySwapAndTradingProfit) * 0.8 if max(DailySwapAndTradingProfit) > 0 else 1_000_000  # 左グラフの最大値から 80% を計算
        MaxYright = max(NotUsed) * 0.8 if max(NotUsed) > 0 else 1_000_000  # 右グラフの最大値から 80% を計算

        """ 左側のグラフ """
        # スワップ収益の参考値を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 1.18,  # テキストの Y 座標位置を最大値の 118% に配置（上部）
            # スワップ収益の年間参考値をフォーマットして表示
            "Swap Reference:\n1MXN: {0:,} JPY/year\n1ZAR: {1:,} JPY/year".format(MxnSwapPerYear, ZarSwapPerYear),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "blue",  # テキストの色を青に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # 初期投資額の参考値を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 1.03,  # テキストの Y 座標位置を最大値の 103% に配置（スワップ収益参考値の少し下）
            # 初期投資額と 50% が運用されていることをフォーマットして表示
            "Initial Investment:\n{0:,} JPY (50% used)".format(InitialInvestmentYen),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "green",  # テキストの色を緑に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # デイトレード収益の参考値を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 0.88,  # テキストの Y 座標位置を最大値の 88% に配置（初期投資額表示の少し下）
            # デイトレード収益と 50% が運用されていることをフォーマットして表示
            "Profit / Day Trading:\n{0:,} JPY/day (50% used)".format(int(ExpectedDailyTradeProfit)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "purple",  # テキストの色を紫に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # 目標証拠金維持率を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 0.73,  # テキストの Y 座標位置を最大値の 73% に配置（デイトレード収益表示の少し下）
            # 目標証拠金維持率が設定されていることをフォーマットして表示
            "Margin Maintenance Target:\n{0:,}%".format(int(MarginMaintenanceTarget)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "red",  # テキストの色を赤に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # リスク織り込み済み表示を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 0.58,  # テキストの Y 座標位置を最大値の 58% に配置（目標証拠金維持率表示の少し下）
            # リスク計算が設定されていることをフォーマットして表示
            "Risk included:\nSlightly higher",
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "red",  # テキストの色を赤に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # 最終月の翌月の月収を概算参考値として表示するための計算
        MonthlyIncome = 0  # 最終月の翌月の月収を累積する変数を初期化
        for ForCalculateMonthDailyIncome in range(1, 31):
            CalculateDailyIncome()  # 日次スワップ収益とデイトレード収益を計算（必要な値は全てグローバル変数として定義）
            ApplyDailyRiskFactors()  # 日次リスク要素を適用（必要な値は全てグローバル変数として定義）
            MonthlyIncome += DailyIncome  # 日次収益を月収に加算

        # 最終月の翌月の月収を概算参考値として表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 0.43,  # テキストの Y 座標位置を最大値の 43% に配置（リスク織り込み済み表示の少し下）
            # 最終月の翌月の月収をフォーマットして表示
            "Last Monthly Income:\n{0:,} JPY/day".format(int(MonthlyIncome)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "red",  # テキストの色を赤に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        """ 右側のグラフ """
        # スワップ収益の参考値を表示
        axes[1].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYright * 1.18,  # テキストの Y 座標位置を最大値の 118% に配置（上部）
            # スワップ収益の年間参考値をフォーマットして表示
            "Swap Reference:\n1MXN: {0:,} JPY/year\n1ZAR: {1:,} JPY/year".format(MxnSwapPerYear, ZarSwapPerYear),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "blue",  # テキストの色を青に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # 初期投資額の参考値を表示
        axes[1].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYright * 1.03,  # テキストの Y 座標位置を最大値の 103% に配置（スワップ収益参考値の少し下）
            # 初期投資額と 50% が未運用とされていることをフォーマットして表示
            "Initial Investment:\n{0:,} JPY (50% added)".format(InitialInvestmentYen),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "green",  # テキストの色を緑に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # デイトレード収益の参考値を表示
        axes[1].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYright * 0.88,  # テキストの Y 座標位置を最大値の 88% に配置（初期投資額表示の少し下）
            # デイトレード収益と 50% が未運用とされていることをフォーマットして表示
            "Profit / Day Trading:\n{0:,} JPY/day (50% added)".format(int(ExpectedDailyTradeProfit)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "purple",  # テキストの色を紫に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )
    except Exception:  # テキスト描画でエラーが発生した場合
        pass  # エラーを無視して処理を継続

    # レイアウトを調整して表示
    plt.tight_layout()
    plt.show()

# 初期設定をイニシャライズ
InitializeGlobals()

# スワップ及びデイトレード収益データを計算
DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit = CalculateSwapAndTradingProfitGrowth()

# コンソールに最後の30日分の運用中残高（元本を含む）を表示
print("\n運用中残高（元本を含む：最後の30日分）:")
for i in range(max(0, len(DailySwapAndTradingProfit) - 30), len(DailySwapAndTradingProfit)):
    print("Day {0}: {1:,.0f}円".format(i + 1, DailySwapAndTradingProfit[i]))

# コンソールに最後の30日分の未運用残高（元本を含む）を表示
print("\n未運用残高（元本を含む：最後の30日分）:")
for i in range(max(0, len(CumulativeSwapAndTradingProfit) - 30), len(CumulativeSwapAndTradingProfit)):
    print("Day {0}: {1:,.0f}円".format(i + 1, CumulativeSwapAndTradingProfit[i]))

# グラフ描画
PlotSwapData(DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit)
