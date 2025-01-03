"""
【スワップポイント＆デイトレード収益計算プログラムの使い方】

このプログラムは、運用中及び未運用のスワップポイントとデイトレード収益を計算し、そのトレンドをグラフとして可視化するツールです。
プログラムを実行することで、運用状況を理解しやすくなります。

プログラムファイル名: "SwapPointProfitAnalysis.py"

【機能】
●入力された設定値に基づいたスワップポイント収益を日次（年間取引可能日数261日分）で計算する機能（初期投資額の半分を運用）。
●入力された設定値に基づいたデイトレード収益を日次（年間取引可能日数261日分）で計算する機能。
●入力された設定値に基づき、実際の取引成績に基づくデイトレード利益率を算出する機能。
●入力された設定値に基づいた一定期間毎（毎月・偶数月・両方）の追加投資処理機能（半分を運用）。
●入力された設定値に基づいた、障害年金受給上限年収突破による追加投資停止機能。
●入力された設定値に基づいた、通貨毎のロットの配分比率の算出機能と、その比率に基づいて増資の配分や未運用残高の配分を計算する機能。
●目標証拠金維持率を超過した場合に、余剰資金を運用残高に移動する機能。
●日次リスク要因「1. デイトレードの取引回数の内、何回かで損失発生」「2. 時間帯によるボラティリティリスクを適用」「3. 年に二回大損失が発生」を計算する機能。
●成績に基づいたデイトレード利益率を計算に使用する場合に、日次リスク要因「1. デイトレードの取引回数の内、何回かで損失発生」を調節する機能。
●当年の損益通算後の収益に対する所得税課税処理機能（シミュレーションを行う設定年数毎に課税処理。税率は損益通算後の収益に準じたもの）。

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
# 【投資開始日】
# 実際に取り引きを始めた年月日を入力します。
# この日付に基づいて、次の設定項目である「初期投資額」から現在までの、口座残高の増分を考慮した日次デイトレード利益率を算出します。
InvestmentStartDay = "2024/12/05"

# 【初期投資額（円）】
# このプログラムで運用を開始するための最初の投資金額を指定します。初期投資額の 50% を運用資金として使用し、スワップポイント収益の計算に利用します。
# 残りの 50% は未運用分（元本）として管理されます。この分割は、証拠金維持率を充分に確保し、強制ロスカットのリスクを軽減するために行われます。
# またこの金額に基づいて、次の設定項目である「現在の口座残高」との差額を算出し、日次デイトレード利益率の算出を行います。
InitialInvestmentYen = 800000 + (50000 + (1598980 + 421487))

# 【現在の口座残高（円）】
# 初期投資額を含めた現在の口座残高を入力します。
# 初期投資額と同額でも構いませんが、その場合は日次デイトレード利益率の計算のために設定項目「デイトレードによる予想追加収入」に適切な値を入力してください。
# 注意：この設定値が初期投資額よりも高いと、この設定値を基にデイトレード利益率の計算を自動で行います。デイトレードを行う場合、
# 利益率の高い方を選択しますので、設定項目「デイトレードによる予想追加収入」に低い値を設定する場合は初期投資額と同額の値を設定することを推奨します。
# 初期投資額と現在の口座残高に大きな乖離があると、大きな利益率を算出してしまいます。
CurrentBalance = 3760443 + 2000

# 【レバレッジ】
# 適用するレバレッジの倍率を整数で設定します（25倍なら25）。
Leverage = 25

# 【1ロット購入に必要な金額】
# 各通貨の1ロット（DMM FX の場合：1万通貨）を購入するために必要な日本円の金額を指定します。
# この値は実際の為替レートを基に設定され、再投資や追加投資のロット数計算に使用されます。
Mxn1LotCost = 3081  # MXN/JPY
Zar1LotCost = 3439  # ZAR/JPY
# 1ロット購入金額がレバレッジ適用後の価格である場合は以下を True、そうでなければ False にします。
# レバレッジが適用されていない場合、1通貨の対円価格を最小取引単位倍した価格が1ロットの購入に必要な価格とほとんど等しくなります。
# 1ロットの購入に必要な金額が上記計算結果よりも大きく小さい場合、レバレッジが適用されています。
LotCostLeveraged = True

# 【各通貨の一日当たりのスワップポイント（円）】
# MXN/JPY（メキシコ・ペソ）と ZAR/JPY（南アフリカ・ランド）の通貨ペアで、1ロット当たりの1日毎に得られるスワップポイントを設定します。
# 補足：スワップポイント収益の計算を行わない場合は 0 を設定してください。
MxnSwapPerDay = 21
ZarSwapPerDay = 17

# 【初期ロット数】
# 最初に購入するロット数を通貨ペア毎に設定します。このロット数に基づいてスワップポイント収益が計算されます。
# シミュレーション結果を表示するグラフに含める「元本に占めるスワップ収益用運用額の割合」は「初期投資額」「現在の口座残高」の低い方を基準に計算します。
# 注意：レバレッジを参考に小さな値から計算を始めてください。この値を基に初期の必要証拠金が計算されます。
# 注意：この値を設定しないとシミュレーションを行うことができません。
# 　　　デイトレード収益の計算はこの値を直接参照しませんが、必要証拠金とスワップポイント収益の計算に必要です。
MxnLots = 600  # MXN/JPY のロット数
ZarLots = 0  # ZAR/JPY のロット数

# 【証拠金維持率の目標値（%）】
# このプログラムで運用を効率化するための目標となる証拠金維持率を設定します。証拠金維持率がこの値を超えた場合、未運用残高の一部を運用資金として振り分けます。
# この設定により、運用効率を最大化し、未運用資金の過剰な蓄積を防ぎます。目標値は適切な安全域を考慮して調整することが推奨されます。
MarginMaintenanceTarget = 300  # 証拠金維持率目標値（パーセントを整数で入力。300% なら 300）

# 【デイトレード設定】
# 総口座残高の何％をデイトレードに使用するかを設定します（パーセントを整数で入力。100% なら 100）。
# デイトレードをしない場合は 0 と設定します。ただし、この値はシミュレーションには直接的には影響しません。
# 使用先：「初期デイトレード使用金額（シミュレーションの初期段階で参照します）」「グラフに表示するデイトレード収益の参考値」
# シミュレーション中に「初期デイトレード使用金額」を未運用残高が超えた場合、この残高に基づいてデイトレード収益の計算を行います。
# 備考：総口座残高に占める未運用残高の割合は「初期ロット数」に基づいて計算されます。
DayTradingInvestmentRatio = 50

# 【デイトレードによる予想追加収入（円/日）】
# 毎日デイトレードを行うことで得られると想定される追加収入を設定します。この値はスワップポイント収益に加算され、総収益の予測計算に使用されます。
# デイトレードの実績や市場状況に応じてこの値を調節することが推奨されます。
# 既に取り引きを行っていて、これまでの設定項目の説明によってこの項目の入力の必要を促されない場合は、0 と設定してください。
ExpectedDailyTradeProfitInputYen = 8000 / 31  # 1日当たりのデイトレードによる予想追加収益（円/日）

# 【追加投資設定】
# 【毎月投入する追加投資額（円）】
# 毎月26日に投入する追加投資額を指定します。
# この設定は、日本の最も一般的な給料日を想定しており、給与が支払われるタイミングで、一部の資金を追加投資に充当する前提で計算を行います。
# 実際の日本の最も一般的な給料日は25日ですが、26日を投入日とすることで、資金投入の判断を行う時間を確保することを目的としています。
# MXN/JPY 及び ZAR/JPY のロット比率に基づいてこの金額の半分を運用に回し、新たなロットを購入します。
MonthlyInvestment = 0  # 下の偶数月の設定と同時設定が可能です。

# 【偶数月に投入する追加投資額（円）】
# 偶数月16日に投入する追加投資額を指定します。
# この設定は、日本の年金受給者を想定しており、偶数月（2月、4月、6月……）に年金が支給されるタイミングで、一部の資金を追加投資に充当する前提で計算を行います。
# 実際の日本の公的年金は「偶数月の15日」に支給されますが、16日を投入日とすることで、資金投入の判断を行う時間を確保することを目的としています。
# MXN/JPY 及び ZAR/JPY のロット比率に基づいてこの金額の半分を運用に回し、新たなロットを購入します。
BiMonthlyInvestment = 0  # 上の毎月の設定と同時設定が可能です。

# 【年間収益がこの金額に達すると追加投資を中止】
# 障害年金受給者を想定し、年収が 370 万円を超えると障害年金の支給が半減、472 万円を超えると停止されるため、
# この金額を上限として追加投資を中止するよう設定しています。ただし、上限に達するまでに計画されている当年分の追加投資は実行されます。
# 注意：この設定項目に該当しない方は極端に大きな値を設定してください。
InvestmentIncomeLimit = 3700000

# 【シミュレーション期間】
# シミュレーションを行う年数を設定してください。
SimulationYears = 1  # 例：1年の場合は 1、3年の場合は 3
# シミュレーションを行う年数に加えて、例えば税金差し引き後のシミュレーションを確認したい場合などに、任意の追加計算日数を設定できます。
SimulationDays = 181  # 例：半年の場合は 181 日、三ヶ月の場合は 90 日、九ヶ月の場合は 273 日

# 【グラフ表示設定】
# グラフの縦軸（金額）の単位を "K"（1,000 単位）または "M"（1,000,000 単位）のいずれかから選びます。
IfSelectedK = False  # "K" の場合は True、"M" の場合は False に設定

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
    global DayTradingInvestmentRatio, DayTradingInvestment, TradeProfitRate, ExpectedDailyTradeProfit, MxnSwapPerYear, ZarSwapPerYear

    if InitialInvestmentYen > 0:  # 初期投資額が 1 以上であることを確認
        # デイトレード使用金額率を小数に変換
        DayTradingInvestmentRatio = DayTradingInvestmentRatio / 100 if DayTradingInvestmentRatio > 0 else 0

        # 初期設定「デイトレードによる予想追加収入」に基づいたデイトレード利益率を計算
        if DayTradingInvestmentRatio > 0:  # デイトレード使用金額率が 1 以上であることを確認
            DayTradingInvestment = InitialInvestmentYen * DayTradingInvestmentRatio  # デイトレードに使用する金額を計算
            TradeProfitRate = ExpectedDailyTradeProfitInputYen / DayTradingInvestment \
                if ExpectedDailyTradeProfitInputYen > 0 else 0  # デイトレード利益率を計算
        else:  # デイトレード使用金額率が 0 の場合
            DayTradingInvestment = 0  # デイトレードに使用する金額を 0 に設定
            TradeProfitRate = 0  # デイトレード利益率を 0 に設定

        # 必要なライブラリをインポート
        from datetime import datetime, timedelta  # datetime モジュールをインポートして日付操作を可能にする

        # 投資開始日と現在の日付を解析
        StartDate = datetime.strptime(InvestmentStartDay, "%Y/%m/%d")  # 投資開始日を解析し、datetime オブジェクトに変換する
        CurrentDate = datetime.now()  # 現在の日付を取得
        TotalDays = (CurrentDate - StartDate).days  # 投資開始日から現在の日付までの経過日数を計算

        # 土日を除外した営業日数を計算
        BusinessDays = 0  # 営業日数のカウンタを初期化
        for DayOffset in range(TotalDays + 1):  # 経過日数分をループ
            Date = StartDate + timedelta(days=DayOffset)  # 投資開始日からの各日付を計算
            if Date.weekday() < 5:  # 月曜（0）～金曜（4）が営業日
                BusinessDays += 1  # 営業日数をインクリメント

        # 複利を考慮したデイトレード利益率を計算
        if BusinessDays > 0:  # 営業日数が有効であることを確認
            DailyProfitRate = (CurrentBalance / InitialInvestmentYen) ** (1 / BusinessDays) - 1  # デイトレード利益率を複利ベースで計算
        else:
            DailyProfitRate = 0  # 営業日数が 0 の場合の安全策

        # 初期設定「デイトレードによる予想追加収入」に基づいたデイトレード利益率、複利を考慮したデイトレード利益率の高い方を選択
        TradeProfitRate = max(TradeProfitRate, DailyProfitRate)  # 「デイトレードによる予想追加収入」に適切な値が設定されていることが前提

        # 計算された日次デイトレード収益（円/日）
        ExpectedDailyTradeProfit = max(InitialInvestmentYen, CurrentBalance) * DayTradingInvestmentRatio * TradeProfitRate
    else:  # 初期投資額が 0 の場合
        import sys  # システム操作に必要なモジュールをインポート
        print("初期投資金額が 0 に設定されています。プログラムの実行を中止しました。")
        sys.exit(1)  # プログラムの実行を中止し、終了コード 1 を返す

    # 各通貨ペアにおける、1ロット当たりの年間スワップ収益を計算
    MxnSwapPerYear = MxnSwapPerDay * 261  # MXN/JPY の年間スワップ収益
    ZarSwapPerYear = ZarSwapPerDay * 261  # ZAR/JPY の年間スワップ収益

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

    Parameters:
        LastSimulation (bool): シミュレーションの最終段階であることを示す真偽値。最終段階なら True、デフォルトは False。

    Returns:
        None
    """
    # 補助関数：日次スワップ収益を計算
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

    """ CalculateDailyIncome() の記述 """
    global DailyIncome, DailyInvestmentProfit  # グローバル変数を宣言

    # 日次スワップ収益を計算する（補助関数を利用）
    DailyIncome = CalculateDailySwap(CurrentMxnLots, CurrentZarLots, MxnSwapPerDay, ZarSwapPerDay)

    # デイトレード分の収益を計算して加算
    UnusedBalance = RemainingReinvestment + TotalCumulativeSwapAndTradingProfit + UsedProfitForInvestment + \
        AdditionalUnusedInvestment + UsedUnusedInvestment - TotalInvestment  # 未運用残高を算出
    # 初期デイトレード使用金額または未運用残高の大きい方にデイトレード利益率を掛けて日次デイトレード収益を計算
    DailyInvestmentProfit = max(DayTradingInvestment, UnusedBalance) * TradeProfitRate if LotCostLeveraged else \
        max(DayTradingInvestment, UnusedBalance) * Leverage * TradeProfitRate
    DailyIncome += DailyInvestmentProfit  # 日次収益にデイトレード収益を加算

# 日次リスク要素を適用する関数
def ApplyDailyRiskFactors(LastSimulation = False):
    """
    デイトレードのシミュレーションにおける日次リスク要素を適用する関数。

    この関数は、ランダム性を含むリスク要素の計算を 10 回試行し、それぞれの試行結果から最悪値（最大損失）と平均値を収集します。その後、これらの結果を統合して
    リスク評価を行い、グローバル変数に反映します。

    主な処理:
    1. 10 回の試行毎にリスク計算を行い、日次収益及び累積収益をシミュレート。
    2. 各試行結果から最悪値（最大損失）と平均値を計算。
    3. 最悪値と平均値を加重平均で統合し、バランスの取れたリスク評価を提供。
    4. 計算結果をグローバル変数 DailyIncome と TotalCumulativeSwapAndTradingProfit に反映。

    リスク評価の特徴:
    - デイトレード中の一定確率での損失発生をシミュレートします（損失確率や損失率を動的に調整）。
    - 時間帯によるボラティリティリスクを考慮し、特定時間帯に損失を適用。
    - 年に二回発生する大損失イベントをシミュレートし、大きな市場変動を反映。

    この設計により、リスクが過小評価されることを防ぎ、現実的なリスク評価を行います。

    注意:
    - 大損失部分では、損失率は既にレバレッジを考慮した値として計算されている前提です。

    Parameters:
        LastSimulation (bool): シミュレーションの最終段階であることを示す真偽値。最終段階なら True、デフォルトは False。

    Returns:
        None
    """
    import random  # ランダムな数値や確率的な要素を生成するための標準ライブラリ

    # グローバル変数を宣言
    global DailyIncome, DailyInvestmentProfit, Day, TotalInvestment, RemainingReinvestment, TotalCumulativeSwapAndTradingProfit

    # 最悪の結果と平均値を保持するためのローカル変数
    WorstDailyIncome = DailyIncome  # 最悪の日次スワップ及びデイトレード収益を初期化
    WorstTotalCumulativeProfit = TotalCumulativeSwapAndTradingProfit  # 最悪の累積スワップ及びデイトレード収益を初期化
    DailyIncomeSum = 0  # 日次スワップ及びデイトレード収益の合計
    TotalCumulativeProfitSum = 0  # 累積スワップ及びデイトレード収益の合計

    for _ in range(10):
        # 保存しておく初期値を設定
        OriginalDailyIncome = DailyIncome  # 日次スワップ及びデイトレード収益の元の値を保存
        OriginalTotalCumulativeProfit = TotalCumulativeSwapAndTradingProfit  # 累積スワップ及びデイトレード収益の元の値を保存

        # デイトレード中の一定確率での損失発生
        LossProbability = 0.175  # 損失発生確率（17.5%）
        LossRate = 0.095  # 損失額を日次収益の 9.5% とする

        if ExpectedDailyTradeProfitInputYen == 0:  # 成績に基づいているため、リスク要素の損失確率と損失率を動的に計算
            AdjustedLossProbability = LossProbability * (1.0 - TradeProfitRate)  # 利益率が高いほど損失確率を低減
            AdjustedLossRate = LossRate * (1.0 - (TradeProfitRate / 2))  # 利益率が高いほど損失率を軽減
            AdjustedLeverage = Leverage * max(0.5, (1.0 - TradeProfitRate))  # レバレッジを利益率に基づき調節（利益率が高いほどレバレッジを低減）
            if random.random() < AdjustedLossProbability:  # 調節後の損失確率で判定
                DailyIncome -= DailyInvestmentProfit * (AdjustedLossRate * AdjustedLeverage)  # 調節後のレバレッジを適用
        else:  # 初期設定「デイトレードによる予想追加収入」に基づいたデイトレード利益率の場合
            if random.random() < LossProbability:  # 損失が発生するかどうかをランダムに決定
                DailyIncome -= DailyInvestmentProfit * (LossRate * Leverage)  # レバレッジを適用

        # 時間帯によるボラティリティリスクの適用
        if Day % 24 in range(9, 18):  # 日本時間の昼間（午前9時から午後6時）
            LowVolatilityLossRate = 0.02  # ボラティリティが低い場合の日次収益に対する損失（2%）
            DailyIncome -= DailyInvestmentProfit * (LowVolatilityLossRate * Leverage)  # レバレッジを適用

        # 年に二回発生する大損失の適用
        if Day in [91, 273] and not LastSimulation:  # 年間の91日目（3ヶ月後）と273日目（9ヶ月後）
            MajorLossRate = 0.3  # 資金の 30% を喪失する大損失
            TotalInvestment -= TotalInvestment * MajorLossRate  # 運用資金からレバレッジ考慮済みの損失額を減算
            RemainingReinvestment -= RemainingReinvestment * MajorLossRate  # 再投資残高からレバレッジ考慮済みの損失額を減算
            # 累積スワップ及びデイトレード収益からレバレッジ考慮済みの損失額を減算
            TotalCumulativeSwapAndTradingProfit -= TotalCumulativeSwapAndTradingProfit * MajorLossRate
            TotalInvestment = max(TotalInvestment, 0)  # 運用資金が負の値にならないように調節
            RemainingReinvestment = max(RemainingReinvestment, 0)  # 再投資残高が負の値にならないように調節
            # 累積スワップ及びデイトレード収益が負の値にならないように調節
            TotalCumulativeSwapAndTradingProfit = max(TotalCumulativeSwapAndTradingProfit, 0)

        # 最悪の収益を更新
        if DailyIncome < WorstDailyIncome:
            WorstDailyIncome = DailyIncome  # 最悪の日次スワップ及びデイトレード収益を更新
        if TotalCumulativeSwapAndTradingProfit < WorstTotalCumulativeProfit:
            WorstTotalCumulativeProfit = TotalCumulativeSwapAndTradingProfit  # 最悪の累積スワップ及びデイトレード収益を更新

        # 平均値の計算のために各収益を加算
        DailyIncomeSum += DailyIncome
        TotalCumulativeProfitSum += TotalCumulativeSwapAndTradingProfit

        # 次のイテレーションのため状態を元に戻す
        DailyIncome = OriginalDailyIncome  # 日次スワップ及びデイトレード収益を元に戻す
        TotalCumulativeSwapAndTradingProfit = OriginalTotalCumulativeProfit  # 累積スワップ及びデイトレード収益を元に戻す

    # 平均値を計算
    AverageDailyIncome = DailyIncomeSum / 10  # 日次スワップ及びデイトレード収益の平均値
    AverageTotalCumulativeProfit = TotalCumulativeProfitSum / 10  # 累積スワップ及びデイトレード収益の平均値

    # グローバル変数に反映（平均値と最悪値の加重平均を適用）
    Alpha = 0.7  # 平均値と最悪値の重み（0.5 = 平均値と最悪値が同等、0.9 = 平均値を重視）
    DailyIncome = Alpha * AverageDailyIncome + (1 - Alpha) * WorstDailyIncome  # 日次スワップ及びデイトレード収益を更新
    # 累積スワップ及びデイトレード収益を更新
    TotalCumulativeSwapAndTradingProfit = Alpha * AverageTotalCumulativeProfit + (1 - Alpha) * WorstTotalCumulativeProfit

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
            DailyIncome (float): 日次スワップ及びデイトレード収益。
            TotalInvestment (float): 運用残高（必要証拠金）。
            TotalCumulativeSwapAndTradingProfit (float): 「累積スワップ及びデイトレード収益」。
            UsedProfitForInvestment (float): 運用済み「累積スワップ及びデイトレード収益」。
            Leverage (int): レバレッジ。
            MarginMaintenanceTarget (int): 目標証拠金維持率（300% なら 300）。
            RemainingReinvestment (float): 再投資残高（運用残高の追加準備金、レバレッジ未適用）。
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
        def CalculateMarginMaintenanceRate(TotalInvestment, RemainingReinvestment, MarginMaintenanceTarget, DailyIncome,
            TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, AdditionalUnusedInvestment, UsedUnusedInvestment):
            """
            現在の証拠金維持率を計算する関数。

            この関数は、運用中の資金に対する口座全体の資金比率を計算し、整数のパーセント形式で証拠金維持率を返します。証拠金維持率は、運用中の資金がどの程度の
            安全性・余裕を持っているかを評価するための指標です。また、口座残高全体を内部で計算しますが、この関数ではその値を返しません。

            Args:
                TotalInvestment (float): 運用残高（必要証拠金）。
                RemainingReinvestment (float): 再投資残高（運用残高の追加準備金、レバレッジ未適用）。
                MarginMaintenanceTarget (int): 目標証拠金維持率（300% なら 300）。
                DailyIncome (float): 日次スワップ及びデイトレード収益。
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
            AvailableFunds = ProfitAvailable + AdditionalAvailable + DailyIncome  # 未運用残高を合算

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
        # 証拠金維持率を計算（補助関数を利用）
        MarginMaintenanceRate = CalculateMarginMaintenanceRate(TotalInvestment, RemainingReinvestment, MarginMaintenanceTarget,
            DailyIncome, TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, AdditionalUnusedInvestment, UsedUnusedInvestment)

        # 日次スワップ及びデイトレード収益を再投資残高（RemainingReinvestment）に加算：
        # - 再投資額は、最低でも日次収入 (DailyIncome) の 50% を保証します。
        # - 証拠金維持率 (MarginMaintenanceRate) が目標証拠金維持率 (MarginMaintenanceTarget) を超えている場合は、
        #   その超過率に応じた金額を再投資額として計算し、それを再投資残高に加算します。
        # - 計算式：
        #   1. DailyIncome * 0.5（最低保証額）
        #   2. DailyIncome * ((MarginMaintenanceRate - MarginMaintenanceTarget) / 100)（動的調節分）
        #   上記二つの値の内大きい方を選び、それを再投資残高 RemainingReinvestment に加算します。
        RemainingReinvestment += max(DailyIncome * 0.5, DailyIncome * ((MarginMaintenanceRate - MarginMaintenanceTarget) / 100))

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
            RemainingReinvestment += MonthlyInvestment * InvestmentRatioForSwap  # 追加投資中スワップポイント運用に回す割合を再投資残高に加算
            AdditionalUnusedInvestment += MonthlyInvestment * (1 - InvestmentRatioForSwap)  # 残った金額を未運用残高に加算
            ProcessInvestment()  # 補助関数を利用して、再投資残高に基づき、利用可能な証拠金を計算し、比率に従って MXN 及び ZAR に投資を行う

        # 偶数月16日に追加投資を行う
        if Day % 30 == 15 and (Day // 30 + 1) % 2 == 0:  # 偶数月16日かどうかを判定
            RemainingReinvestment += BiMonthlyInvestment * InvestmentRatioForSwap  # 追加投資中スワップポイント運用に回す割合を再投資残高に加算
            AdditionalUnusedInvestment += BiMonthlyInvestment * (1 - InvestmentRatioForSwap)  # 残った金額を未運用残高に加算
            ProcessInvestment()  # 補助関数を利用して、再投資残高に基づき、利用可能な証拠金を計算し、比率に従って MXN 及び ZAR に投資を行う

        return TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, CurrentMxnLots, CurrentZarLots  # 更新後の状態を返す

    # 補助関数：税金を計算
    def CalculateTaxableIncome(Income):
        """
        所得金額に基づき、日本の所得税を税率のみで計算する関数。所得控除は考慮しません。

        Args:
            Income (float): 課税対象となる総収益金額（JPY）

        Returns:
            float: 税金差し引き後の収益金額（JPY）
        """
        # 所得に対する累進課税方式に基づいて税額を計算
        # 累進課税方式では、各所得階層毎に異なる税率が適用される
        TaxBrackets = [
            (1_949_000, 0.05),   # 1,949,000 円以下の税率：5%
            (3_299_000, 0.10),   # 3,299,000 円以下の税率：10%
            (6_949_000, 0.20),   # 6,949,000 円以下の税率：20%
            (8_999_000, 0.23),   # 8,999,000 円以下の税率：23%
            (17_999_000, 0.33),  # 17,999,000 円以下の税率：33%
            (39_999_000, 0.40),  # 39,999,000 円以下の税率：40%
            (float('inf'), 0.45) # それ以上の税率：45%
        ]

        TaxAmount = 0  # 累進税額の初期化
        PreviousBracketLimit = 0  # 前の階層の上限を管理

        for BracketLimit, Rate in TaxBrackets:
            if Income > BracketLimit:
                # 現在の階層全体に適用される税金を計算
                TaxAmount += (BracketLimit - PreviousBracketLimit) * Rate
            else:
                # 現在の階層に収まる部分のみに適用される税金を計算
                TaxAmount += (Income - PreviousBracketLimit) * Rate
                break  # 全ての課税が完了したら終了

            # 次の階層のために上限を更新
            PreviousBracketLimit = BracketLimit

        return Income - TaxAmount  # 税金差し引き後の収益金額を返す

    """ CalculateSwapAndTradingProfitGrowth() の記述 """
    # 初期化：グローバル変数を宣言
    global InitialRequiredMargin, TotalInvestment, InvestmentRatioForSwap, RemainingReinvestment, TotalCumulativeSwapAndTradingProfit, \
        Day, DailyIncome, DailyInvestmentProfit, UsedProfitForInvestment, AdditionalUnusedInvestment, UsedUnusedInvestment, \
        CurrentMxnLots, CurrentZarLots

    # 初期必要証拠金計算のために、設定されたロット数と1ロットのコスト、レバレッジを使用
    InitialRequiredMargin = ((Mxn1LotCost * MxnLots) + (Zar1LotCost * ZarLots))  # 1ロットのコストにロット数をかけて運用中の金額を算出
    if not LotCostLeveraged:  # 1ロット当たりのコストにレバレッジが適用されていない場合
        InitialRequiredMargin = InitialRequiredMargin / Leverage  # 必要証拠金をレバレッジで割って求める

    # 初期化：各種変数
    TotalInvestment = InitialRequiredMargin  # 初期必要証拠金を運用残高として代入
    InvestmentRatioForSwap = InitialRequiredMargin / min(InitialInvestmentYen, CurrentBalance)  # 元本に占めるスワップ収益用運用額の割合
    RemainingReinvestment = 0  # 再投資残高を初期化
    AdditionalUnusedInvestment = 0  # 増資未運用残高を初期化
    TradeDays = 0  # 実際に取引が可能な日数をカウントする変数を初期化
    DailyIncome = 0  # 日次スワップ及びデイトレード収益を初期化
    DailyInvestmentProfit = 0  # デイトレード収益を初期化
    TotalCumulativeSwapAndTradingProfit = 0  # 累積スワップ及びデイトレード収益を初期化
    PreviousCumulativeSwapAndTradingProfit = 0  # 前年の累積スワップ及びデイトレード収益を記録する変数を初期化
    UsedProfitForInvestment = 0  # 運用済み「累積スワップ及びデイトレード収益」を初期化
    UsedUnusedInvestment = 0  # 運用済み「増資未運用残高」を初期化
    CurrentMxnLots = MxnLots  # MXN/JPY の初期ロット数
    CurrentZarLots = ZarLots  # ZAR/JPY の初期ロット数

    # グラフ描画用日次データの記録用リスト
    DailySwapAndTradingProfit = []  # "日次の" 運用残高を記録するリストを初期化
    CumulativeSwapAndTradingProfit = []  # "日次の" 累積スワップ及びデイトレード収益を記録するリストを初期化

    # 現在の MXN ロット数と ZAR ロット数に基づき、最小公約数（GCD）を計算して比率を求める
    GCD = math.gcd(int(CurrentMxnLots), int(CurrentZarLots))  # ロット数を整数に変換して GCD を計算
    if GCD > 0:
        MxnLotRatio = int(CurrentMxnLots) // GCD  # 最小公約数で割って比率を計算
        ZarLotRatio = int(CurrentZarLots) // GCD  # 最小公約数で割って比率を計算
    else:
        MxnLotRatio = ZarLotRatio = 0  # GCD が 0 の場合、比率は 0 に設定
    TotalRatio = MxnLotRatio + ZarLotRatio  # 両者の比率の合計を求める

    # メインロジック
    for Day in range(1, (SimulationYears * 365) + (SimulationDays + 1)):  # 設定年分の日次計算を行うループを開始
        # 1週間のサイクル（1 = 月曜日、7 = 日曜日）を判定
        WeekDay = (Day - 1) % 7 + 1  # 月曜を 1、日曜を 7 とする
        if WeekDay <= 5:  # 平日（1～5）の場合のみ取り引きを実行
            TradeDays += 1  # 取引可能日をカウント

            # 日次スワップ収益とデイトレード収益を計算
            # （初期デイトレード使用金額または必要証拠金の大きい方にデイトレード利益率を掛けて日次デイトレード収益を計算）
            CalculateDailyIncome()  # 必要な値は全てグローバル変数として定義

            # 日次リスク要素を適用
            ApplyDailyRiskFactors()  # 必要な値は全てグローバル変数として定義

            # 再投資処理（補助関数を利用）
            TotalInvestment, RemainingReinvestment, UsedProfitForInvestment, UsedUnusedInvestment, CurrentMxnLots, CurrentZarLots = \
            PerformReinvestment(DailyIncome, TotalInvestment, TotalCumulativeSwapAndTradingProfit, UsedProfitForInvestment, Leverage,
                MarginMaintenanceTarget, RemainingReinvestment, AdditionalUnusedInvestment, UsedUnusedInvestment,
                CurrentMxnLots, CurrentZarLots, Mxn1LotCost, Zar1LotCost, MxnLotRatio, ZarLotRatio, TotalRatio)

            # 累積スワップ及びデイトレード収益を更新
            TotalCumulativeSwapAndTradingProfit += DailyIncome  # デイトレード収益を含む日次収益を累積スワップ及びデイトレード収益に加算
        else:  # 週末ではスキップ、または異なる処理を記述可能
            pass  # 必要なら週末用ロジックを記述

        # 追加投資処理（補助関数を利用）
        TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, CurrentMxnLots, CurrentZarLots = \
        PerformMonthlyInvestment(Day, TotalInvestment, RemainingReinvestment, AdditionalUnusedInvestment, Mxn1LotCost, Zar1LotCost,
            MxnLotRatio, ZarLotRatio, TotalRatio, Leverage, CurrentMxnLots, CurrentZarLots)

        if Day % 365 == 0:  # 年次税金処理
            CurrentYear = Day // 365  # 現在の年数（1年目、2年目、3年目……）

            if Day == 365:  # 最初の年の税金計算
                TaxableIncome = TotalCumulativeSwapAndTradingProfit
            else:  # 二年目以降の税金計算（当年分の収益を算出）
                TaxableIncome = TotalCumulativeSwapAndTradingProfit - PreviousCumulativeSwapAndTradingProfit

            # 増資額を課税対象から減算（当年分を計算）
            TaxExemptInvestment = AdditionalUnusedInvestment / CurrentYear  # 累積増資額を当年分に分配
            TaxableIncome -= TaxExemptInvestment  # 課税対象収益から当年増資額を控除
            TaxableIncome = max(0, TaxableIncome)  # 課税対象が負になることを防ぐ

            # 税金適用後の累積スワップ及びデイトレード収益を計算（補助関数を利用）
            TotalCumulativeSwapAndTradingProfit = CalculateTaxableIncome(TaxableIncome)

            # 前年度の累積スワップ及びデイトレード収益を更新
            PreviousCumulativeSwapAndTradingProfit = TotalCumulativeSwapAndTradingProfit

        # 日次データを記録（一行目：運用残高、二行目：初期投資額または現在の口座残高＋増資未運用残高（運用済み含む）＋累積スワップ及びデイトレード収益）
        DailySwapAndTradingProfit.append(TotalInvestment)
        CumulativeSwapAndTradingProfit.append(
            max(InitialInvestmentYen, CurrentBalance) + AdditionalUnusedInvestment + TotalCumulativeSwapAndTradingProfit)

    return DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit  # 計算結果を返す

# グラフを描画する関数
def PlotSwapData(DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit):
    """
    スワップ収益とデイトレード収益の運用中と未運用のトレンドを別々のグラフに描画します（設定年分）。

    Args:
        DailySwapAndTradingProfit (list): 日次スワップ収益＋デイトレード収益のデータ（運用中、元本の半分を含む）。
        CumulativeSwapAndTradingProfit (list): 累積スワップ収益＋デイトレード収益のデータ（未運用、元本の半分を含む利益）。
    """
    # 補助関数："K" 単位の数値にフォーマット
    def FormatYAxisK(X, _):
        """
        Y 軸の値を "K"（キロ）単位でフォーマットする関数。

        Parameters:
            X (int): 表示する値。
            _ (Any): 不使用（軸の位置用パラメータ）。

        Returns:
            str: "K" 単位でフォーマットされた文字列。
        """
        return "{:,.0f}K".format(X // 1_000)  # 値を 1,000 で割り、"K" 単位にフォーマットして返す

    # 補助関数："M" 単位の数値にフォーマット
    def FormatYAxisM(X, _):
        """
        Y 軸の値を "M"（メガ）単位でフォーマットする関数。

        Parameters:
            X (int): 表示する値。
            _ (Any): 不使用（軸の位置用パラメータ）。

        Returns:
            str: "M" 単位でフォーマットされた文字列。
        """
        return "{:,.0f}M".format(X // 1_000_000)  # 値を 1,000,000 で割り、"M" 単位にフォーマットして返す

    """ PlotSwapData() の記述 """
    import matplotlib.pyplot as plt  # グラフ描画のためのモジュール
    import matplotlib.ticker as mticker  # グラフの目盛りや軸ラベルを調整するモジュール

    # 日次データを年次データに変換
    DaysPerYear = 365  # 1年の日数
    Years = [day / DaysPerYear for day in range(1, len(DailySwapAndTradingProfit) + 1)]  # 年単位の X 軸

    # グラフウィンドウを作成（1行2列のサブプロット）
    fig, axes = plt.subplots(1, 2, figsize = (16, 6))  # 1行2列の配置

    # 運用中残高のグラフ（左側）
    # 未運用残高をプロットし、凡例に「Total Investment Amount for Swap (With n% Principal)」を設定
    axes[0].plot(Years, DailySwapAndTradingProfit, marker = "o",
        label = "Total Investment Amount for Swap (With {0}% Principal)".format(round(InvestmentRatioForSwap * 100)), linestyle = "--",
        color = "blue")
    # グラフタイトルを設定
    axes[0].set_title("Total Investment Amount for Swap (With {0}% Principal)".format(round(InvestmentRatioForSwap * 100)),
        fontsize = 16)
    axes[0].set_xlabel("Year (already taxed)", fontsize = 14)  # X 軸ラベルを設定
    if IfSelectedK:
        axes[0].set_ylabel("In Use Swap & Day Trading Income (JPY, in K)", fontsize = 14)  # Y 軸ラベルを設定
        axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisK))  # Y 軸の数値を "K" 単位でカンマ区切り表示にする
    else:
        axes[0].set_ylabel("In Use Swap & Day Trading Income (JPY, in M)", fontsize = 14)  # Y 軸ラベルを設定
        axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisM))  # Y 軸の数値を "M" 単位でカンマ区切り表示にする
    axes[0].grid(True)  # グリッドを表示
    axes[0].legend(fontsize = 12)  # 凡例を設定

    # 累積スワップ及びデイトレード収益のグラフ（右側）
    axes[1].plot(
        # 累積スワップ及びデイトレード収益をプロットし、凡例に「Total Assets of Account (With Principal)」を設定
        Years, CumulativeSwapAndTradingProfit, marker = "s", label = "Total Assets of Account (With Principal)", linewidth = 2,
        color = "purple")
    axes[1].set_title("Total Assets of Account (With Principal)", fontsize = 16)  # グラフタイトルを設定
    axes[1].set_xlabel("Year (already taxed)", fontsize = 14)  # X 軸ラベルを設定
    if IfSelectedK:
        axes[1].set_ylabel("In Use Swap & Day Trading Income (JPY, in K)", fontsize = 14)  # Y 軸ラベルを設定
        axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisK))  # Y 軸の数値を "K" 単位でカンマ区切り表示にする
    else:
        axes[1].set_ylabel("In Use Swap & Day Trading Income (JPY, in M)", fontsize = 14)  # Y 軸ラベルを設定
        axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(FormatYAxisM))  # Y 軸の数値を "M" 単位でカンマ区切り表示にする
    axes[1].grid(True)  # グリッドを表示
    axes[1].legend(fontsize = 12)  # 凡例を設定

    # 各種参考値をグラフ内に表示
    try:
        # 左右グラフのスケールを統一
        axes[0].set_ylim(0, max(DailySwapAndTradingProfit) * 1.2)  # 左グラフの Y 軸範囲を設定（最大値の 120% を上限）
        axes[1].set_ylim(0, max(CumulativeSwapAndTradingProfit) * 1.2)  # 右グラフの Y 軸範囲を設定（最大値の 120% を上限）
        # 左右グラフのそれぞれで最大値を再計算（左グラフの最大値から 80%、右グラフの最大値から 80% を計算）
        MaxYleft = max(DailySwapAndTradingProfit) * 0.8 if max(DailySwapAndTradingProfit) > 0 else 1_000_000
        MaxYright = max(CumulativeSwapAndTradingProfit) * 0.8 if max(CumulativeSwapAndTradingProfit) > 0 else 1_000_000

        """ 左側のグラフ """
        # スワップ収益の参考値を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 1.18,  # テキストの Y 座標位置を最大値の 118% に配置（上部）
            # スワップ収益の年間参考値をフォーマットして表示
            "Swap Reference:\nA lot of MXN: {0:,} JPY/year\nA lot of ZAR: {1:,} JPY/year".format(MxnSwapPerYear, ZarSwapPerYear),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "blue",  # テキストの色を青に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # 投資額の参考値を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 1.03,  # テキストの Y 座標位置を最大値の 103% に配置（スワップ収益参考値の少し下）
            # 投資額と n% が運用されていることをフォーマットして表示
            "Current Balance:\n{0:,} JPY ({1}% used)".format(CurrentBalance, round(InitialRequiredMargin / CurrentBalance * 100)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "green",  # テキストの色を緑に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # デイトレード収益の参考値を表示
        axes[0].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYleft * 0.88,  # テキストの Y 座標位置を最大値の 88% に配置（投資額表示の少し下）
            # デイトレード収益と 50% が運用されていることをフォーマットして表示
            "Profit / Day Trading:\n{0:,} JPY/day ({1}% used)".format(
                int(ExpectedDailyTradeProfit), round(InvestmentRatioForSwap * 100)),
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

        """ 右側のグラフ """
        # 投資額の参考値を表示
        axes[1].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYright * 1.24,  # テキストの Y 座標位置を最大値の 124% に配置（上部）
            # 投資額をフォーマットして表示
            "Current Balance:\n{0:,} JPY".format(CurrentBalance),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "green",  # テキストの色を緑に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # デイトレード収益の参考値を表示
        axes[1].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYright * 1.09,  # テキストの Y 座標位置を最大値の 109% に配置（投資額表示の少し下）
            # デイトレード収益をフォーマットして表示
            "Profit / Day Trading:\n{0:,} JPY/day (now)".format(int(ExpectedDailyTradeProfit)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "purple",  # テキストの色を紫に設定
            bbox = dict(facecolor = "white", alpha = 0.8, edgecolor = "gray")  # テキストボックスの背景色を白、透明度を 0.8、枠線の色を灰色に設定
        )

        # 月収の参考値を表示
        axes[1].text(
            0.05,  # テキストの X 座標位置を指定（左寄り）
            MaxYright * 0.94,  # テキストの Y 座標位置を最大値の 94% に配置（デイトレード収益表示の少し下）
            # 月収の参考値をフォーマットして表示
            "Last Monthly Income:\n{0:,} JPY/month".format(int(MonthlyIncome)),
            fontsize = 12,  # フォントサイズを 12 ポイントに設定
            color = "red",  # テキストの色を赤に設定
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

# コンソールに最後の30日分の累積スワップ及びデイトレード収益（元本を含む）を表示
print("\n累積スワップ及びデイトレード収益（元本を含む：最後の30日分）:")
for i in range(max(0, len(CumulativeSwapAndTradingProfit) - 30), len(CumulativeSwapAndTradingProfit)):
    print("Day {0}: {1:,.0f}円".format(i + 1, CumulativeSwapAndTradingProfit[i]))

# 最終月の翌月の月収を概算参考値として表示するための計算
MonthlyIncome = 0  # 最終月の翌月の月収を累積する変数を初期化
for ForCalculateMonthDailyIncome in range(1, 31):
    CalculateDailyIncome()  # 日次スワップ収益とデイトレード収益を計算（必要な値は全てグローバル変数として定義）
    ApplyDailyRiskFactors(LastSimulation = True)  # 日次リスク要素を適用（必要な値は全てグローバル変数として定義）
    MonthlyIncome += DailyIncome  # 日次収益を月収に加算

# グラフ描画
PlotSwapData(DailySwapAndTradingProfit, CumulativeSwapAndTradingProfit)
