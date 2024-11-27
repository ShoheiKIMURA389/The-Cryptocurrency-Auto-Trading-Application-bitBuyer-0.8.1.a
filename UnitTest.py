def BuildHierarchy(Data, IndentLevel = 0):
    """
    入力データのデータ構造を Python オブジェクトとして視覚化する関数。
    """
    Indent = " " * (IndentLevel * 4)
    Result = ""

    if isinstance(Data, dict):
        Result += "{\n"
        for Key, Value in Data.items():
            Result += "{0}    \"{1}\": {2},\n".format(Indent, str(Key), BuildHierarchy(Value, IndentLevel + 1).rstrip(",\n"))
        Result = Result.rstrip(",\n") + "\n" + Indent + "}"
    elif isinstance(Data, list):
        Result += "[\n"
        for Item in Data:
            Result += "{0}    {1},\n".format(Indent, BuildHierarchy(Item, IndentLevel + 1).rstrip(",\n"))
        Result = Result.rstrip(",\n") + "\n" + Indent + "]"
    elif isinstance(Data, tuple):
        Result += "(\n"
        for Item in Data:
            Result += "{0}    {1},\n".format(Indent, BuildHierarchy(Item, IndentLevel + 1).rstrip(",\n"))
        Result = Result.rstrip(",\n") + "\n" + Indent + ")"
    elif isinstance(Data, set):
        Result += "{\n"
        for Item in Data:
            Result += "{0}    {1},\n".format(Indent, BuildHierarchy(Item, IndentLevel + 1).rstrip(",\n"))
        Result = Result.rstrip(",\n") + "\n" + Indent + "}"
    else:
        if isinstance(Data, str):
            Result += "\"{0}\"".format(Data)
        else:
            Result += str(Data)

    return Result

import locale  # ロケール設定を使用するためのインポート
import re  # 正規表現を使用するためのインポート
# 日本語のロケール設定を行う
try:
    locale.setlocale(locale.LC_COLLATE, "ja_JP.UTF-8")  # 日本語のソート順を使用するため
except locale.Error:
    print("日本語ロケールが設定されていません。")

# 濁音・半濁音を静音化するためのマッピング辞書
SilentMap = {
    "が": "か", "ぎ": "き", "ぐ": "く", "げ": "け", "ご": "こ",  # 濁音
    "ざ": "さ", "じ": "し", "ず": "す", "ぜ": "せ", "ぞ": "そ",  # 濁音
    "だ": "た", "ぢ": "ち", "づ": "つ", "で": "て", "ど": "と",  # 濁音
    "ば": "は", "び": "ひ", "ぶ": "ふ", "べ": "へ", "ぼ": "ほ",  # 濁音
    "ぱ": "は", "ぴ": "ひ", "ぷ": "ふ", "ぺ": "へ", "ぽ": "ほ",  # 半濁音
}

# 五十音順で並べるための関数
def SortStrings(input_list):
    """
    入力された文字列リストを五十音順でソートする関数。

    Parameters:
        input_list (list): ソートする文字列のリスト。

    Returns:
        list: 五十音順にソートされた文字列リスト。
    """
    # ソートを行う際に日本語のロケール順を優先させる
    return sorted(input_list, key=locale.strxfrm)  # 日本語のロケールに従ったソートを実行

# 静音化を行う関数
def Silence(input_string):
    """
    入力された文字列に含まれる濁音・半濁音を静音化する関数。

    Parameters:
        input_string (str): 静音化する文字列。

    Returns:
        str: 静音化された文字列。
    """
    for dakuten, seion in SilentMap.items():  # 濁音・半濁音を変換
        input_string = input_string.replace(dakuten, seion)  # 置換処理
    return input_string

# メイン処理
def ProcessInput(input_data):
    """
    入力データ（単一リストまたは二重リスト）を受け取り、それぞれを静音化し五十音順でソートする関数。

    Parameters:
        input_data (list): 静音化とソートを行う文字列のリスト、またはリストのリスト。

    Returns:
        list: 静音化された後に五十音順でソートされた文字列リスト、またはリストのリスト。
    """
    # 入力データが二重リストの場合、再帰的に処理
    if isinstance(input_data[0], list):  # 二重リストの場合
        return [ProcessInput(sublist) for sublist in input_data]  # 各サブリストを再帰的に処理
    else:  # 単一リストの場合
        silent_list = [Silence(item) for item in input_data]  # 文字列を静音化
        return SortStrings(silent_list)  # 静音化後に五十音順でソート

# 入力データ（単一リストまたは二重リスト）
input_data = []

# プログラム実行
output_data = ProcessInput(input_data)  # 入力データの静音化とソートを実行
print(output_data)  # 結果表示
