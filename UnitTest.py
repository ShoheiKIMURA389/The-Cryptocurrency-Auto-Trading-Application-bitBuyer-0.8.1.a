def BuildHierarchy(Data, IndentLevel = 0):
    """
    入力データのデータ構造を Python オブジェクトとして視覚化する関数。

    Args:
        Data (any): 視覚化する入力データ。辞書、リスト、タプル、セット、その他任意のデータ型をサポート。
        IndentLevel (int, optional): 現在のインデントレベル。デフォルトは0。

    Returns:
        str: 視覚化されたデータ構造の文字列。

    Examples:
        >>> BuildHierarchy({"key": [1, 2, 3]})
        {
            "key": [
                1,
                2,
                3
            ]
        }
    """
    Indent = " " * (IndentLevel * 4)  # 現在のインデントレベルに応じたスペースを計算
    Result = ""  # 結果の文字列を初期化

    if isinstance(Data, dict):  # データが辞書型の場合
        Result += "{\n"  # 開始括弧
        for Key, Value in Data.items():  # 辞書の各キーと値をループ処理
            Result += "{0}    \"{1}\": {2},\n".format(  # キーと値を文字列形式で追加
                Indent,
                str(Key),
                BuildHierarchy(Value, IndentLevel + 1).rstrip(",\n")  # 再帰呼び出しで値を整形
            )
        Result = Result.rstrip(",\n") + "\n" + Indent + "}"  # 最後のカンマを削除して閉じ括弧を追加
    elif isinstance(Data, list):  # データがリスト型の場合
        Result += "[\n"  # 開始括弧
        for Item in Data:  # リストの各項目をループ処理
            Result += "{0}    {1},\n".format(
                Indent,
                BuildHierarchy(Item, IndentLevel + 1).rstrip(",\n")  # 再帰呼び出しで項目を整形
            )
        Result = Result.rstrip(",\n") + "\n" + Indent + "]"  # 最後のカンマを削除して閉じ括弧を追加
    elif isinstance(Data, tuple):  # データがタプル型の場合
        Result += "(\n"  # 開始括弧
        for Item in Data:  # タプルの各項目をループ処理
            Result += "{0}    {1},\n".format(
                Indent,
                BuildHierarchy(Item, IndentLevel + 1).rstrip(",\n")  # 再帰呼び出しで項目を整形
            )
        Result = Result.rstrip(",\n") + "\n" + Indent + ")"  # 最後のカンマを削除して閉じ括弧を追加
    elif isinstance(Data, set):  # データがセット型の場合
        Result += "{\n"  # 開始括弧
        for Item in Data:  # セットの各項目をループ処理
            Result += "{0}    {1},\n".format(
                Indent,
                BuildHierarchy(Item, IndentLevel + 1).rstrip(",\n")  # 再帰呼び出しで項目を整形
            )
        Result = Result.rstrip(",\n") + "\n" + Indent + "}"  # 最後のカンマを削除して閉じ括弧を追加
    else:  # データがそれ以外の型の場合
        if isinstance(Data, str):  # データが文字列型の場合
            Result += "\"{0}\"".format(Data)  # 文字列として整形
        else:  # データがその他の場合
            Result += str(Data)  # 文字列形式に変換

    return Result  # 最終結果を返す

import locale  # ロケール設定を使用するためのインポート
import re  # 正規表現を使用するためのインポート

# 日本語のロケール設定を行う
try:
    locale.setlocale(locale.LC_COLLATE, "ja_JP.UTF-8")  # 日本語のソート順を使用するため
except locale.Error:
    print("日本語ロケールが設定されていません。")  # ロケールエラー時の警告メッセージ

# 濁音・半濁音を静音化するためのマッピング辞書
SilentMap = {
    "が": "か", "ぎ": "き", "ぐ": "く", "げ": "け", "ご": "こ",  # 濁音
    "ざ": "さ", "じ": "し", "ず": "す", "ぜ": "せ", "ぞ": "そ",  # 濁音
    "だ": "た", "ぢ": "ち", "づ": "つ", "で": "て", "ど": "と",  # 濁音
    "ば": "は", "び": "ひ", "ぶ": "ふ", "べ": "へ", "ぼ": "ほ",  # 濁音
    "ぱ": "は", "ぴ": "ひ", "ぷ": "ふ", "ぺ": "へ", "ぽ": "ほ",  # 半濁音
}

# 五十音順で並べるための関数
def SortStrings(InputList):
    """
    入力された文字列リストを五十音順でソートする関数。

    Args:
        InputList (list): ソートする文字列のリスト。

    Returns:
        list: 五十音順にソートされた文字列リスト。

    Examples:
        >>> SortStrings(['が', 'あ', 'か'])
        ['あ', 'か', 'が']
    """
    return sorted(InputList, key=locale.strxfrm)  # 日本語のロケールに従ったソートを実行

# 静音化を行う関数
def Silence(InputString):
    """
    入力された文字列に含まれる濁音・半濁音を静音化する関数。

    Args:
        InputString (str): 静音化する文字列。

    Returns:
        str: 静音化された文字列。

    Examples:
        >>> Silence('がぎぐげご')
        'かきくけこ'
    """
    for Dakuten, Seion in SilentMap.items():  # 濁音・半濁音を変換
        InputString = InputString.replace("{0}".format(Dakuten), "{0}".format(Seion))  # 置換処理
    return InputString

# メイン処理
def ProcessInput(InputData):
    """
    入力データ（単一リストまたは二重リスト）を受け取り、それぞれを静音化し五十音順でソートする関数。

    Args:
        InputData (list): 静音化とソートを行う文字列のリスト、またはリストのリスト。

    Returns:
        list: 静音化された後に五十音順でソートされた文字列リスト、またはリストのリスト。

    Examples:
        >>> ProcessInput(['が', 'あ', 'か'])
        ['あ', 'か', 'か']
        >>> ProcessInput([['が', 'ぎ'], ['げ', 'ご']])
        [['か', 'き'], ['け', 'こ']]
    """
    if isinstance(InputData[0], list):  # 二重リストの場合
        return [ProcessInput(Sublist) for Sublist in InputData]  # 各サブリストを再帰的に処理
    else:  # 単一リストの場合
        SilentList = ["{0}".format(Silence(Item)) for Item in InputData]  # 文字列を静音化
        return SortStrings(SilentList)  # 静音化後に五十音順でソート

"""
# 入力データ（単一リストまたは二重リスト）
InputData = []

# プログラム実行
OutputData = ProcessInput(InputData)  # 入力データの静音化とソートを実行
print("{0}".format(OutputData))  # 結果表示
"""
