#!/usr/bin/python
# coding: UTF-8

import csv
import matplotlib.pyplot as plt
import pandas as pd

def main():    
    df = pd.read_csv('output/polarity.csv', parse_dates=['datetime'], date_parser=lambda date: pd.to_datetime(date, format='%Y/%m/%d %H:%M:%S'))

    plt.clf()

    x = df['datetime']
    y = df['polarity']

    plt.plot(x, y)

    plt.show()

if __name__ == '__main__':
    main()