"""
このスクリプトは、指定された文字数に応じてランダムな文字列を生成し、その中から最もランダム性の高い文字列を選定してコンソールに出力します。

主な機能:
- ランダム文字列を10個生成。
- 生成された文字列の中で、異なる文字の種類数が最も多い文字列を最もランダム性が高いと判断。
- 小文字、大文字、数字の割合を動的に調整可能。

使用方法:
1. スクリプトを実行します。
2. 必要な文字列の長さを整数値でコンソールに入力します。
3. 生成された文字列と最もランダム性が高い文字列、およびその統計情報が表示されます。

入力:
- 必要な文字列の長さ (int): ランダム文字列の総文字数。

出力:
- 生成された文字列リスト。
- 最もランダム性の高い文字列とその詳細な統計情報。

例:
    必要な文字列の文字数を入力してください: 32
    生成された文字列:
    rA9bC...

    最もランダム性の高い文字列:
    aBc123...
    文字数: 32
    小文字の数: 11
    大文字の数: 13
    数字の数: 8

注意:
- 入力が32の場合は固定された比率で文字列を生成します。
- それ以外の場合は動的に計算された比率で文字列を生成します。
- スクリプトは終了せず、何度でも入力を受け付けます。
"""

import random  # ランダム文字列生成用モジュール
import string  # 文字列操作用モジュール
from collections import Counter  # 文字カウント用モジュール

# ランダムな文字列を生成する関数
def GenerateRandomStrings(InputLength):
    """
    指定された長さのランダム文字列を10個生成し、最もランダム性の高い文字列を判定して出力します。

    この関数は、以下の2つのケースに応じてランダム文字列を生成します。
    
    1. InputLengthが32の場合:
       - 小文字、大文字、数字をそれぞれ決まった比率で組み合わせたランダム文字列を10個生成します。
       - 各文字列は以下のように構成されます:
         - 小文字: 11文字
         - 大文字: 13文字
         - 数字: 8文字
       - 各文字列はランダムに並び替えられた後、リストに格納されます。

    2. InputLengthが32以外の場合:
       - 指定された長さに基づいて、小文字、大文字、数字の文字数を動的に計算します。
       - 各カテゴリの文字列を10個ずつ生成し、それらをランダムに組み合わせた10個の文字列を生成します。

    最終的に生成された文字列リストから、最もランダム性が高いと判定された文字列を出力します。
    ランダム性は、文字列内の異なる文字の種類数によって評価されます。

    Args:
        InputLength (int): 必要な文字列の総文字数。
                           - 32の場合、固定された比率で文字列を生成します。
                           - それ以外の場合、動的に計算された比率で文字列を生成します。

    Outputs:
        - 各生成された文字列
        - 最もランダム性が高い文字列とその統計情報:
          - 小文字の数
          - 大文字の数
          - 数字の数
          - 総文字数

    Returns:
        None: 生成された文字列とランダム性の高い文字列に関する統計を標準出力に出力します。

    Examples:
        >>> GenerateRandomStrings(32)
        生成された文字列:
        rA9bC...
        
        最もランダム性の高い文字列:
        aBc123...
        文字数: 32
        小文字の数: 11
        大文字の数: 13
        数字の数: 8

        >>> GenerateRandomStrings(50)
        生成された文字列:
        Zxy12...
        
        最もランダム性の高い文字列:
        Xyz987...
        文字数: 50
        小文字の数: 18
        大文字の数: 18
        数字の数: 14
    """
    if InputLength == 32:
        # 入力文字数が32の場合
        Strings = []  # ランダム文字列を格納するリスト
        for _ in range(10):  # 10個の文字列を生成
            SmallLetters = random.choices(string.ascii_lowercase, k=11)  # 小文字11文字を生成
            CapitalLetters = random.choices(string.ascii_uppercase, k=13)  # 大文字13文字を生成
            Digits = random.choices(string.digits, k=8)  # 数字8文字を生成
            Combined = SmallLetters + CapitalLetters + Digits  # 全ての文字を結合
            random.shuffle(Combined)  # ランダムに並び替え
            Strings.append("".join(Combined))  # ランダム文字列をリストに追加
    else:
        # 入力文字数が32でない場合
        RoundedValue = round(InputLength * 0.28)  # 0.28を掛けて四捨五入
        Remaining = InputLength - RoundedValue  # 残りの文字数を計算
        HalfRemaining = Remaining // 2  # 残りの文字数を半分に分割

        # 調整: 合計が入力文字数と一致するようにする
        Adjustment = InputLength - (HalfRemaining * 2 + RoundedValue)
        HalfRemaining += Adjustment // 2
        RoundedValue += Adjustment % 2

        SmallLetterStrings = [
            "".join(random.choices(string.ascii_lowercase, k=HalfRemaining))  # 小文字列を生成
            for _ in range(10)
        ]
        CapitalLetterStrings = [
            "".join(random.choices(string.ascii_uppercase, k=HalfRemaining))  # 大文字列を生成
            for _ in range(10)
        ]
        DigitStrings = [
            "".join(random.choices(string.digits, k=RoundedValue))  # 数字列を生成
            for _ in range(10)
        ]

        Strings = []  # ランダム文字列を格納するリスト
        for _ in range(10):  # 10個の文字列を生成
            Combined = (
                random.choice(SmallLetterStrings)  # 小文字列からランダムに選択
                + random.choice(CapitalLetterStrings)  # 大文字列からランダムに選択
                + random.choice(DigitStrings)  # 数字列からランダムに選択
            )
            Shuffled = list(Combined)  # 結合した文字列をリスト化
            random.shuffle(Shuffled)  # ランダムに並び替え
            Strings.append("".join(Shuffled))  # ランダム文字列をリストに追加

    # 補助関数: ランダム性を計算する
    def RandomnessScore(String):
        """
        文字列のランダム性を評価するためのスコアを計算します。

        この関数は、入力文字列に含まれる異なる文字の種類数をカウントし、それをスコアとして返します。異なる文字が多いほど、ランダム性が高いとみなされます。

        Args:
            String (str): 評価対象となる文字列。

        Returns:
            int: 入力文字列内の異なる文字の種類数。

        Examples:
            >>> RandomnessScore("aabbcc")
            3
            >>> RandomnessScore("abcdef")
            6
        """
        Counts = Counter(String)  # 各文字の出現頻度を計算
        return len(Counts.keys())  # 異なる文字の種類数をスコアとして返す

    MostRandomString = max(Strings, key=RandomnessScore)  # ランダム性の高い文字列を選択

    # 統計情報を計算
    LetterCounts = Counter(MostRandomString)  # 各文字の出現回数を計算
    NumLowercase = sum(LetterCounts[Char] for Char in string.ascii_lowercase)  # 小文字の数
    NumUppercase = sum(LetterCounts[Char] for Char in string.ascii_uppercase)  # 大文字の数
    NumDigits = sum(LetterCounts[Char] for Char in string.digits)  # 数字の数

    # 結果を出力
    print("生成された文字列:")
    for S in Strings:  # 生成された文字列を順に出力
        print(S)

    print("\n最もランダム性の高い文字列:")
    print(MostRandomString)  # 最もランダム性の高い文字列を出力
    print("文字数:", len(MostRandomString))  # ランダム性の高い文字列の文字数を出力
    print("小文字の数:", NumLowercase)  # 小文字の数を出力
    print("大文字の数:", NumUppercase)  # 大文字の数を出力
    print("数字の数:", NumDigits)  # 数字の数を出力

# 永続的に入力を受け付ける
while True:
    InputLength = int(input("必要な文字列の文字数を入力してください: "))  # プロンプトを正しく設定
    GenerateRandomStrings(InputLength)
