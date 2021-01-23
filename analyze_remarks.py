#!/usr/bin/python
# coding: UTF-8

import re
import csv
import pandas as pd
import polarity

def get_dictionary():
    pd.set_option('display.unicode.east_asian_width', True)

    # 感情値辞書の読み込み
    pndic = pd.read_csv(r"resources/pn_ja.dic",
                        encoding="shift-jis",
                        names=['word_type_score'])

    # 語と感情値を抽出
    pndic["split"] = pndic["word_type_score"].str.split(":")
    pndic["word"] = pndic["split"].str.get(0)
    pndic["score"] = pndic["split"].str.get(3)

    # dict型に変換
    keys = pndic['word'].tolist()
    values = pndic['score'].tolist()
    return dict(zip(keys, values))

def get_avg_polarity(dic, text):
    results = polarity.analyze_polarity(dic ,text)
    return polarity.get_avg(results)

def main():
    DATE_PATTERN = r'\d{4}\/\d{2}\/\d{2}\([日月火水木金土]\)\n'
    TIME_PATTERN = r'^((0?|1)[0-9]|2[0-3]):[0-5][0-9]	'

    print('>> あなたのLINE上の表示名を入力してください。')
    your_name = input()
    opponent_name = ''
    date = ''
    time = ''
    tmp_min = 0
    user = ''
    content = ''

    firstLoop = True

    dic = get_dictionary()

    with open('input/history.txt') as h:
        with open('output/polarity.csv', 'w') as p:
            writer = csv.writer(p)
            writer.writerow(['datetime', 'user', 'polarity'])

            for line in h:
                # 一行目で会話相手の名前を取得する
                if firstLoop:
                    opponent_name = re.search(r'(?<=\[LINE\] ).*(?=とのトーク履歴)', line).group()
                    print('"' + your_name + '" と "' + opponent_name + '" 間のトーク履歴を処理します。')
                    firstLoop = False

                # 空行の場合はcontinue
                elif len(line.strip()) == 0:
                    continue

                # トークの年月日を取得する
                elif re.fullmatch(DATE_PATTERN, line):
                    date = re.search(r'\d{4}\/\d{2}\/\d{2}', line).group()
                    print('取得中: ' + date)

                # 発言時刻、発言者、発言を取得する
                elif re.match(TIME_PATTERN, line):

                    tmp_time = re.match(r'^((0?|1)[0-9]|2[0-3]):[0-5][0-9]', line).group()

                    # 時系列順にグラフ化するため、仮に秒数を設定する
                    # 1分間に60回以上発言された場合は無効(continue)
                    if tmp_min >= 60:
                        continue
                    if time == tmp_time + ':' + str(tmp_min).zfill(2):
                        tmp_min =+ 1
                        time = tmp_time + ':' + str(tmp_min).zfill(2)
                    else:
                        time = tmp_time + ':00'
                        tmp_min = 0

                    user = your_name if re.match(your_name, re.sub(TIME_PATTERN, '', line)) else opponent_name
                    content = re.sub(TIME_PATTERN + user, '', line)
                    # スタンプと画像は対象外
                    if re.fullmatch(r"^\[(スタンプ|画像)\]", content.strip()):
                        
                        continue

                # 改行された場合の発言取得
                else:
                    content = line
                
                # 書き出す
                if date and time and user and content:
                    writer.writerow([date + ' ' + time, user, get_avg_polarity(dic, content.strip('	').strip('\n'))])

if __name__ == '__main__':
    main()