# !/usr/bin/python
# coding: UTF-8

your_name = "userA"
search_your_name = " "+your_name+" "

opponent_name = "userB"
search_opponent_name = " "+opponent_name+" "

text = open('sample.txt')
lines = text.readlines()
# readlines() - ファイルを全て読み込み、1行毎に処理を行う
text.close()

for line in lines:
    # スライス: 文字列インデックス[開始インデックス:終了インデックス:ステップ数]

    if line[0:5:1] == "2016.":
        date = line[0:10:1] #日付の情報
        # print date
    
    if line[2:3:] == ":" and line[5:6:] == " ":
        time = line[0:5:1] #時間の情報
        # print time

    if line.find(search_your_name) >= 0:
        username = your_name
        content = line[len(time)+len(search_your_name):] #コンテンツ情報
        # print content
        print (date+", "+time+", "+username+", "+content)

    elif line.find(search_opponent_name) >= 0:
        username = opponent_name
        content = line[len(time)+len(search_opponent_name):] #コンテンツ情報
        # print content
        print (date+", "+time+", "+username+", "+content)
