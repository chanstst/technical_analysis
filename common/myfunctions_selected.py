import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from datetime import date, timedelta
from math import ceil

from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

def get_dfs():
    """
    load the data saved in 6 csv files (adj, high, low, volume, open, close)
    return 6 dfs
    """
    root = "../"

    file_adj = root + "data/adj.csv"
    df_adj = pd.read_csv(file_adj, index_col=0, header=0)
    df_adj = remove_null_rows(df_adj)
    df_adj = remove_repeated_row(df_adj)

    file_high = root + "data/high.csv"
    df_high = pd.read_csv(file_high, index_col=0, header=0)
    df_high = remove_null_rows(df_high)
    df_high = remove_repeated_row(df_high)

    file_low = root + "data/low.csv"
    df_low = pd.read_csv(file_low, index_col=0, header=0)
    df_low = remove_null_rows(df_low)
    df_low = remove_repeated_row(df_low)

    file_volume = root + "data/volume.csv"
    df_volume = pd.read_csv(file_volume, index_col=0, header=0)
    df_volume = remove_null_rows(df_volume)
    df_volume = remove_repeated_row(df_volume)

    file_open = root + "data/open.csv"
    df_open = pd.read_csv(file_open, index_col=0, header=0)
    df_open = remove_null_rows(df_open)
    df_open = remove_repeated_row(df_open)

    file_close = root + "data/close.csv"
    df_close = pd.read_csv(file_close, index_col=0, header=0)
    df_close = remove_null_rows(df_close)
    df_close = remove_repeated_row(df_close)

    return df_adj, df_high, df_low, df_volume, df_open, df_close

def single_stock_data(code, df_adj, df_high, df_low, df_volume, df_open, df_close):
    df = pd.DataFrame(df_adj.loc[:,code])
    df.rename(columns={code:"adj"}, inplace=True)
    df["open"] = df_open.loc[:,code]
    df["close"] = df_close.loc[:,code]
    df["high"] = df_high.loc[:,code]
    df["low"] = df_low.loc[:,code]
    df["volume"] = df_volume.loc[:,code]

    return df


def charts_list(codes):

    # load the data files
    df_adj, df_high, df_low, df_volume, df_open, df_close = get_dfs()

    # get the stock names
    df_names = pd.DataFrame(data=codes, index=codes)
    df_names = merge_stock_names(df_names)

    n = len(codes)

    # colors
    color_face = "#000047"

    color_5 = "pink"
    color_10 = "red"
    color_20 = "yellow"
    color_50 = "#b4b8e7"
    color_100 = "#9e7920"
    color_200 = "white"

    color_up = "#1ed4ff"
    color_down = "#6af80f"
    color_grid = "#aabbcc"

    fig = plt.figure(figsize=(16,6*ceil(n/2)))

    for j in np.arange(len(codes)):
        #print("j="+ str(j))
        code = codes[j]
        df = single_stock_data(code, df_adj, df_high, df_low, df_volume, df_open, df_close)
        df = add_range_MA(df)

        # day range to show
        n_days=50
        df = df[-n_days:]

        ax1 = fig.add_subplot(ceil(n/2),2,(j+1))

        name = df_names.loc[codes[j], "name"]
        ax1.set_title(code + " " + name, fontproperties=font)

        ax1.set_facecolor(color_face)

        # axis tickers
        months = [pd.to_datetime(df.index.values[i]).strftime("%b") for i in np.arange(0,len(df.index.values))]
        days = [pd.to_datetime(df.index.values[i]).strftime("%d") for i in np.arange(0,len(df.index.values))]
        labels = [months[i] + "-" + days[i] for i in np.arange(0,len(months))]
        x_pos = np.arange(len(labels))

        # To align labels with selection - list with skipping/steps
        max_label_no = 7;
        label_step = int(len(labels)/7)
        labels2 = labels[0:len(labels):label_step]

        plt.xticks(x_pos, labels2)
        #plt.xticks(x_pos, labels2, rotation="45")
        loc = plticker.FixedLocator(np.arange(0,len(labels),label_step))
        ax1.xaxis.set_major_locator(loc)


        ax1.yaxis.set_visible(False)
        ax1.bar(x_pos, (df["volume"]/1000000), color=color_grid, alpha=0.3)
        y1_max = (df["volume"]/1000000).max()*3
        y1_min = 0
        ax1.set_ylim(y1_min,y1_max)

        ax2 = ax1.twinx()
        ax2.plot(x_pos, df['5MA'], color_5, label='5MA: '+str(df['5MA'][-1]))
        ax2.plot(x_pos, df['10MA'], color_10, label='10MA: '+str(df['10MA'][-1]))
        ax2.plot(x_pos, df['20MA'], color_20, label='20MA: '+str(df['20MA'][-1]))
        ax2.plot(x_pos, df['50MA'], color_50, label='50MA: '+str(df['50MA'][-1]))
        ax2.plot(x_pos, df['100MA'], color_100, label='100MA: '+str(df['100MA'][-1]))

        leg = ax2.legend(framealpha=0, loc='upper left', frameon=False, mode="expand", ncol=3)
        for text in leg.get_texts():
            plt.setp(text, color = 'w')

        edgecolors = [color_down if df["delta"][i] < 0 else color_up for i in np.arange(0,len(df["close"]))]
        colors = [color_face if (df["open"][i] - df["close"][i] < 0) else edgecolors[i] for i in np.arange(0,len(df["close"]))]

        # bars in the middle
        ax2.bar(x_pos, df['open_close_diff'], bottom=df['open_close_min'] , width=0.7, color=colors, edgecolor=edgecolors)

        # sticks up and down
        ax2.bar(x_pos, df['range_up'], bottom=df['open_close_max'] , width=0.1, color=colors, edgecolor=edgecolors)
        ax2.bar(x_pos, df['range_down'], bottom=df['low'] , width=0.1, color=colors, edgecolor=edgecolors)

        y2_max = df["high"].max()*1.05
        y2_min = df["low"].min()*0.95
        ax2.set_ylim(y2_min,y2_max)

        ax2.grid(color=color_grid, linestyle="-", linewidth=0.3)

    #print the charts after the for loop
    plt.show()

    return None

def add_range_MA(df):
    # delta is the changes in close price today vs one day prior
    df['delta'] = df['close'] - df['close'].shift(1)

    df['open_close_diff'] = (df['close'] - df['open']).apply(np.absolute)

    df['open_close_min'] = df[['open', 'close']].apply(np.min, axis=1)
    df['open_close_max'] = df[['open', 'close']].apply(np.max, axis=1)

    df['range_up'] = df['high'] - df['open_close_max']
    df['range_down'] = df['open_close_min'] - df['low']

    df['5MA'] = df['close'].rolling(5).mean().round(2)
    df['10MA'] = df['close'].rolling(10).mean().round(2)
    df['20MA'] = df['close'].rolling(20).mean().round(2)
    df['50MA'] = df['close'].rolling(50).mean().round(2)
    df['100MA'] = df['close'].rolling(100).mean().round(2)
    df['200MA'] = df['close'].rolling(200).mean().round(2)

    return df


def remove_repeated_row(df):
    if (df.index.values[-2] == df.index.values[-1]):
        df1 = pd.DataFrame(data=df.iloc[0:-2], index=df.index.values[0:-2], columns=df.columns)
        df2 = pd.DataFrame(data=df.iloc[-1:], index=df.index.values[-1:], columns=df.columns)
        df = pd.concat([df1,df2], axis=0)
        print("last second row repetitive - removed")
        print(df.tail())
    return df


def remove_null_rows(df):
    """
    Drop the rows where entire row has null values
    index will be changed to date time
    assume one to two layers of column header
    """
    column0 = df.columns[0]
    if type(column0) == tuple:
        column0_0 = df.columns[0][0]
        column0_1 = df.columns[0][1]
        # get the indices to drop
        index_to_drop = df[column0_0][column0_1][df[column0_0][column0_1].isna()==True].index
    else:
        index_to_drop = df[column0][df[column0].isna()==True].index

    # drop the indices
    df.drop(index_to_drop, inplace=True)

    return df

def merge_stock_names(df):
    """
    Merge with stock names based on the file ../data/hk_names.csv
    df - where index is the stock code
    """
    names = pd.read_csv("../data/hk_names.csv", engine='python', index_col=0, header=None)
    names.rename(columns={1:"name"}, inplace=True)
    df_merged = pd.merge(names, df, left_index=True, right_index=True, how="right")
    return df_merged
