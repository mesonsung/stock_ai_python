
# 自訂指標模組
import indicator

import os
import yahoostock
import matplotlib.pyplot as plot
import matplotlib.ticker as mticker
from matplotlib.widgets import MultiCursor


# 暫存目錄 ./temp
__path__ = os.path.dirname(__file__)
temp_path = f'{__path__}/temp'
os.makedirs(temp_path, 0o755, exist_ok=True)


if __name__ == '__main__':
    # ==================================================
    # 證券代碼
    symbol = '2317'
    datefmt = '%Y-%m-%d'
    df = yahoostock.get_stock_daily_candles(symbol, start='2020-12-01')
    # 刪除索引(預設是Date欄位)
    df.reset_index(drop=True, inplace=True)
    # ==================================================
    # 
    df['SMA5'] = indicator.SMA(df['Close'])
    df['EMA5'] = indicator.EMA(df['Close'])
    df['WMA5'] = indicator.WMA(df['Close'])
    df['CMA'] = indicator.CMA(df['Close'])
    df['CBI'] = indicator.CBI(df['Close'])
    df['BIAS'] = indicator.BIAS(df['Close'])
    df['MACD-DIF'], df['MACD-DEM'], df['MACD-OSC'] = indicator.MACD(df['Close'])
    df['MTM'], df['MTM-SMA'] = indicator.MTM(df['Close'])
    df['CMO'] = indicator.CMO(df['Close'])
    df['RSI-F'] = indicator.RSI(df['Close'], 6)
    df['RSI-S'] = indicator.RSI(df['Close'], 12)
    df['RSI-SM'] = indicator.SMA(df['RSI-F'], 6)
    df['KDJ-RSV'], df['KDJ-K'], df['KDJ-D'], df['KDJ-J'], df['KDJ-J2'] = indicator.KDJ(df['High'], df['Low'], df['Close'], 9)
    df['ATR'] = indicator.ATR(df['High'], df['Low'], df['Close'], 14)
    df['OBV'], df['OBV-SMA'] = indicator.OBV(df['Close'], df['Volume'])
    df['BBANDS-UP'], df['BBANDS-SMA'], df['BBANDS-DN'] = indicator.BBands(df['Close'], 5)
    df['CDP-AH'], df['CDP-NH'], df['CDP'], df['CDP-NL'], df['CDP-AL'] = indicator.CDP(df['High'], df['Low'], df['Close'])
    df['LOHAS-AH'], df['LOHAS-NH'], df['LOHAS-T'], df['LOHAS-NL'], df['LOHAS-AL'] = indicator.LOHAS(df['Close'])
    df['LOHAS-UP'], df['LOHAS-MD'], df['LOHAS-DN'] = indicator.LohasBands(df['High'], df['Low'], df['Close'])
    df['DC-UP'], df['DC-MD'], df['DC-DN'] = indicator.DonCH(df['High'], df['Low'], df['Close'])
    df.to_csv(f'{temp_path}/stock.csv')
    # ==================================================
    # 繪製圖表 
    # 設定索引為日期字串
    df.index = df['Date']
    # 色彩表
    colors = ['#fca103', '#5773ff', '#d700eb', '#0a9c05']
    colors_5 = ['#f22c2c', '#ff9900', '#888888', '#33b013', '#1357b0']
    # 圖表
    fig, ax = plot.subplots(4, 1, sharex=True, figsize=(10, 10))
    ax[0].set_title(symbol)
    # 
    df['Close'].plot(ax=ax[0], color='red', linewidth=1)
    # df['SMA5'].plot(ax=ax[0], color=colors[0], linewidth=0.5)
    # df['EMA5'].plot(ax=ax[0], color=colors[1], linewidth=0.5)
    # df['WMA5'].plot(ax=ax[0], color=colors[2], linewidth=0.5)
    # df['CMA'].plot(ax=ax[0], color=colors[3], linewidth=0.5)
    # df['CBI'].plot(ax=ax[0], color=colors[2], linewidth=0.5)
    # 
    # df['BBANDS-UP'].plot(ax=ax[0], color=colors_5[0], linewidth=0.5)
    # df['BBANDS-SMA'].plot(ax=ax[0], color=colors_5[1], linewidth=0.5, linestyle=':')
    # df['BBANDS-DN'].plot(ax=ax[0], color=colors_5[2], linewidth=0.5)
    # 
    # df['CDP-AH'].plot(ax=ax[0], color=colors_5[0], linewidth=0.5)
    # df['CDP-NH'].plot(ax=ax[0], color=colors_5[1], linewidth=0.5)
    # df['CDP'].plot(ax=ax[0], color=colors_5[2], linewidth=0.5, linestyle=':')
    # df['CDP-NL'].plot(ax=ax[0], color=colors_5[3], linewidth=0.5)
    # df['CDP-AL'].plot(ax=ax[0], color=colors_5[4], linewidth=0.5)
    # 
    df['LOHAS-AH'].plot(ax=ax[0], color=colors_5[0], linewidth=0.5)
    df['LOHAS-NH'].plot(ax=ax[0], color=colors_5[1], linewidth=0.5)
    df['LOHAS-T'].plot(ax=ax[0], color=colors_5[2], linewidth=0.5, linestyle=':')
    df['LOHAS-NL'].plot(ax=ax[0], color=colors_5[3], linewidth=0.5)
    df['LOHAS-AL'].plot(ax=ax[0], color=colors_5[4], linewidth=0.5)
    # 
    # df['LOHAS-UP'].plot(ax=ax[0], color=colors_5[1], linewidth=0.5)
    # df['LOHAS-MD'].plot(ax=ax[0], color=colors_5[2], linewidth=0.5, linestyle=':')
    # df['LOHAS-DN'].plot(ax=ax[0], color=colors_5[3], linewidth=0.5)
    # 
    # df['DC-UP'].plot(ax=ax[0], color=colors_5[1], linewidth=0.5)
    # df['DC-MD'].plot(ax=ax[0], color=colors_5[2], linewidth=0.5, linestyle=':')
    # df['DC-DN'].plot(ax=ax[0], color=colors_5[3], linewidth=0.5)
    # 
    df['MACD-DIF'].plot(ax=ax[1], color=colors[0], linewidth=1)
    df['MACD-DEM'].plot(ax=ax[1], color=colors[1], linewidth=1)
    ax[1].fill_between(df.index, 0, df['MACD-OSC'], color='#cccccc')
    ax[1].axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
    ax[1].axhline(y=2, color='red', linewidth=0.5, linestyle='--')
    ax[1].axhline(y=-2, color='green', linewidth=0.5, linestyle='--')
    # 
    # df['BIAS'].plot(ax=ax[2], color=colors[0], linewidth=0.5)
    # ax[2].fill_between(df.index, 0, df['BIAS'], color='#cccccc')
    # ax[2].axhline(y=0.03, color='red', linewidth=0.5, linestyle='--')
    # ax[2].axhline(y=-0.03, color='green', linewidth=0.5, linestyle='--')
    # 
    df['RSI-F'].plot(ax=ax[2], color=colors[0], linewidth=1)
    df['RSI-SM'].plot(ax=ax[2], color=colors[1], linewidth=1)
    # df['RSI-S'].plot(ax=ax[2], color=colors[1], linewidth=1)
    ax[2].axhline(y=80, color='red', linewidth=0.5, linestyle='--')
    ax[2].axhline(y=50, color='gray', linewidth=0.5, linestyle='--')
    ax[2].axhline(y=20, color='green', linewidth=0.5, linestyle='--')
    #
    # df['MTM'].plot(ax=ax[2], color=colors[0], linewidth=1)
    # df['MTM-SMA'].plot(ax=ax[2], color=colors[1], linewidth=1)
    # ax[2].axhline(y=10, color='red', linewidth=0.5, linestyle='--')
    # ax[2].axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
    # ax[2].axhline(y=-10, color='green', linewidth=0.5, linestyle='--')
    # 
    # df['CMO'].plot(ax=ax[2], color=colors[2], linewidth=1)
    # ax[2].axhline(y=20, color='red', linewidth=0.5, linestyle='--')
    # ax[2].axhline(y=-20, color='green', linewidth=0.5, linestyle='--')
    # 
    df['KDJ-K'].plot(ax=ax[3], color=colors[0], linewidth=1)
    df['KDJ-D'].plot(ax=ax[3], color=colors[1], linewidth=1)
    # df['KDJ-J'].plot(ax=ax[3], color=colors[2], linewidth=1, linestyle=':')
    # df['KDJ-J2'].plot(ax=ax[3], color=colors[3], linewidth=1, linestyle=':')
    ax[3].axhline(y=80, color='red', linewidth=0.5, linestyle='--')
    ax[3].axhline(y=20, color='green', linewidth=0.5, linestyle='--')
    #
    # df['OBV'].plot(ax=ax[2], color=colors[0], linewidth=1)
    # df['OBV-SMA'].plot(ax=ax[2], color=colors[1], linewidth=1)
    # 
    for i in range(len(ax)):
        ax[i].legend(
            loc='upper left',
            bbox_to_anchor=(0, 1),
            ncol=1,
            prop={'size': 6}
        )
        ax[i].get_xaxis().set_visible(not (i < len(ax) - 1))
        ax[i].yaxis.tick_right()
        ax[i].tick_params(labelsize=8)
        ax[i].set_xticks(df.index)
        # ax[i].set_xticklabels(df['Date'].apply(lambda d: d.strftime(datefmt)))
        ax[i].xaxis.set_major_locator(mticker.MultipleLocator(5))
    multi = MultiCursor(fig.canvas, ax, color='red', lw=1)
    plot.xticks(fontsize=8, rotation=90)
    plot.subplots_adjust(hspace=0)
    plot.show()