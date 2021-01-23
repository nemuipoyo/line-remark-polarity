import pandas as pd
import MeCab

def main(): 
    text = '今日はいい天気だね'
    dic = get_dictionary()
    results = analyze_polarity(dic, text)
    print(results)

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


def analyze_polarity(dic, text):

    mecab = MeCab.Tagger("-Ochasen")

    # 形態素解析に基づいて単語を抽出
    words = []
    for v in mecab.parse(text).splitlines():
        if len(v.split()) >= 3:
            if v.split()[3][:2] in ['名詞','形容詞','動詞','副詞']:
                words.append(v.split()[2])

    # 空の要素を削除
    words = [x for x in words if x != []]

    # 語単位の処理
    results = []
    for word in words:
        word_score = []
        score = dic.get(word)
        word_score = (word, score)
        results.append(word_score)       

    return results

def get_avg(results):
    sum = float(0)
    count = 0
    for result in results:
        if not result[1] == None:
            sum =+ float(result[1])
            count =+ 1
    if not count == 0:
        return sum / float(count)
    else:
        return float(0)    

if __name__ == '__main__':
    main()