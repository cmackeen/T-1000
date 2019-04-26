import datetime
import talib
import colorama
import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from termcolor import colored

colorama.init()

def get_datasets(symbol, mode, limit):
    headers = {'User-Agent': 'Mozilla/5.0', 'authorization': 'Apikey 3d7d3e9e6006669ac00584978342451c95c3c78421268ff7aeef69995f9a09ce'}

    # OHLC
    url = 'https://min-api.cryptocompare.com/data/histo{}?fsym={}&tsym=BTC&e=Binance&limit={}'.format(mode, symbol, limit)
    print(colored('> downloading ' + symbol + ' OHLCV', 'green'))
    response = requests.get(url, headers=headers)
    json_response = response.json()
    result = json_response['Data']
    df = pd.DataFrame(result)
    df['Date'] = pd.to_datetime(df['time'], utc=True, unit='s')
    df.drop('time', axis=1, inplace=True)

    # indicators
    # https://github.com/mrjbq7/ta-lib/blob/master/docs/func.md
    open_price, high, low, close = np.array(df['open']), np.array(df['high']), np.array(df['low']), np.array(df['close'])
    volume = np.array(df['volumefrom'])
    # cycle indicators
    df.loc[:, 'HT_DCPERIOD'] = talib.HT_DCPERIOD(close)
    df.loc[:, 'HT_DCPHASE'] = talib.HT_DCPHASE(close)
    df.loc[:, 'HT_PHASOR_inphase'], df.loc[:, 'HT_PHASOR_quadrature'] = talib.HT_PHASOR(close)
    df.loc[:, 'HT_SINE_sine'], df.loc[:, 'HT_SINE_leadsine'] = talib.HT_SINE(close)
    df.loc[:, 'HT_TRENDMODE'] = talib.HT_TRENDMODE(close)
    # momemtum indicators
    df.loc[:, 'ADX'] = talib.ADX(high, low, close, timeperiod=14)
    df.loc[:, 'ADXR'] = talib.ADXR(high, low, close, timeperiod=14)
    df.loc[:, 'APO'] = talib.APO(close, fastperiod=12, slowperiod=26, matype=0)
    df.loc[:, 'AROON_down'], df.loc[:, 'AROON_up'] = talib.AROON(high, low, timeperiod=14)
    df.loc[:, 'AROONOSC'] = talib.AROONOSC(high, low, timeperiod=14)
    df.loc[:, 'BOP'] = talib.BOP(open_price, high, low, close)
    df.loc[:, 'CCI'] = talib.CCI(high, low, close, timeperiod=14)
    df.loc[:, 'CMO'] = talib.CMO(close, timeperiod=14)
    df.loc[:, 'DX'] = talib.DX(high, low, close, timeperiod=14)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df.loc[:, 'MFI'] = talib.MFI(high, low, close, volume, timeperiod=14)
    df.loc[:, 'MINUS_DI'] = talib.MINUS_DI(high, low, close, timeperiod=14)
    df.loc[:, 'MINUS_DM'] = talib.MINUS_DM(high, low, timeperiod=14)
    df.loc[:, 'MOM'] = talib.MOM(close, timeperiod=10)
    df.loc[:, 'PPO'] = talib.PPO(close, fastperiod=12, slowperiod=26, matype=0)
    df.loc[:, 'ROC'] = talib.ROC(close, timeperiod=10)
    df.loc[:, 'RSI'] = talib.RSI(close, timeperiod=14)
    df.loc[:, 'STOCH_k'], df.loc[:, 'STOCH_d'] = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df.loc[:, 'STOCHF_k'], df.loc[:, 'STOCHF_d'] = talib.STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
    df.loc[:, 'STOCHRSI_K'], df.loc[:, 'STOCHRSI_D'] = talib.STOCHRSI(close, timeperiod=30, fastk_period=14, fastd_period=10, fastd_matype=1)
    df.loc[:, 'TRIX'] = talib.TRIX(close, timeperiod=30)
    df.loc[:, 'ULTOSC'] = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    df.loc[:, 'WILLR'] = talib.WILLR(high, low, close, timeperiod=14)
    # overlap studies
    df.loc[:, 'BBANDS_upper'], df.loc[:, 'BBANDS_middle'], df.loc[:, 'BBANDS_lower'] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    df.loc[:, 'DEMA'] = talib.DEMA(close, timeperiod=30)
    df.loc[:, 'EMA'] = talib.EMA(close, timeperiod=30)
    df.loc[:, 'HT_TRENDLINE'] = talib.HT_TRENDLINE(close)
    df.loc[:, 'KAMA'] = talib.KAMA(close, timeperiod=30)
    df.loc[:, 'MA'] = talib.MA(close, timeperiod=30, matype=0)
    df.loc[:, 'MIDPOINT'] = talib.MIDPOINT(close, timeperiod=14)
    df.loc[:, 'WMA'] = talib.WMA(close, timeperiod=30)
    df.loc[:, 'SMA'] = talib.SMA(close)
    # pattern recoginition
    df.loc[:, 'CDL2CROWS'] = talib.CDL2CROWS(open_price, high, low, close)
    df.loc[:, 'CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(open_price, high, low, close)
    df.loc[:, 'CDL3INSIDE'] = talib.CDL3INSIDE(open_price, high, low, close)
    df.loc[:, 'CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(open_price, high, low, close)
    # price transform
    df.loc[:, 'WCLPRICE'] = talib.WCLPRICE(high, low, close)
    # statistic funcitons
    df.loc[:, 'BETA'] = talib.BETA(high, low, timeperiod=5)
    df.loc[:, 'CORREL'] = talib.CORREL(high, low, timeperiod=30)
    df.loc[:, 'STDDEV'] = talib.STDDEV(close, timeperiod=5, nbdev=1)
    df.loc[:, 'TSF'] = talib.TSF(close, timeperiod=14)
    df.loc[:, 'VAR'] = talib.VAR(close, timeperiod=5, nbdev=1)
    # volatility indicators
    df.loc[:, 'ATR'] = talib.ATR(high, low, close, timeperiod=14)
    df.loc[:, 'NATR'] = talib.NATR(high, low, close, timeperiod=14)
    df.loc[:, 'TRANGE'] = talib.TRANGE(high, low, close)
    # volume indicators
    df.loc[:, 'AD'] = talib.AD(high, low, close, volume)
    df.loc[:, 'ADOSC'] = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
    df.loc[:, 'OBV'] = talib.OBV(close, volume)
    # wallet indicator to trading bot
    df.loc[:, 'wallet_btc'] = 1.0
    df.loc[:, 'wallet_symbol'] = 0.0

    # df.fillna(df.mean(), inplace=True)
    df.dropna(inplace=True)
    df.set_index('Date', inplace=True)
    train_size = round(len(df) * 0.5) # 50% to train -> test with different value
    df_train = df[:train_size]
    df_rollout = df[train_size:]
    df_train.to_csv('datasets/bot_train_{}.csv'.format(symbol))
    df_rollout.to_csv('datasets/bot_rollout_{}.csv'.format(symbol))

    return df

#------------------------------------------------------------->

def init_data(symbol, mode):
    df = pd.read_csv('datasets/bot_{}_{}.csv'.format(mode, symbol))
    df.drop('Date', axis=1, inplace=True)
    df_array = df.values.tolist()
    keys = df.keys()
    return keys, df_array


def build_layout(title, x_axis_title, y_axis_title):
    """Create the plotly's layout with custom configuration

    Arguments:
        title {str} -- Layout's central title
        x_axis_title {str} -- Axis x title
        y_axis_title {str} -- Axis y title

    Returns:
        Object -- Plotly object from plotly.graph_objs
    """

    layout = go.Layout(plot_bgcolor='#2d2929',
                       paper_bgcolor='#2d2929',
                       title=title,
                       font=dict(color='rgb(255, 255, 255)', size=17),
                       legend=dict(orientation="h"),
                       yaxis=dict(title=y_axis_title),
                       xaxis=dict(title=x_axis_title))
    return layout

def var_cov_matrix(df, weigths):
    """Compute covariance matrix with respect of given weigths

    Arguments:
        df {pandas.DataFrame} -- The timeseries object
        weigths {list} -- List of weights to be used

    Returns:
        numpy.array -- The covariance matrix
    """

    sigma = np.cov(np.array(df).T, ddof=0)
    var = (np.array(weigths) * sigma * np.array(weigths).T).sum()
    return var

def calc_exp_returns(avg_return, weigths):
    """Compute the expected returns

    Arguments:
        avg_return {pandas.DataFrame} -- The average of returns
        weigths {list} -- A list of weigths

    Returns:
        array -- N dimensions array
    """

    exp_returns = avg_return.dot(weigths.T)
    return exp_returns




def print_dollar():
    print(chr(27) + "[2J")
    print(colored("""
||====================================================================||
||//$\\\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\//$\\\||
||(100)==================| FEDERAL RESERVE NOTE |================(100)||
||\\\$//        ~         '------========--------'                \\\$//||
||<< /        /$\              // ____ \\\                         \ >>||
||>>|  12    //L\\\            // ///..) \\\         L38036133B   12 |<<||
||<<|        \\\ //           || <||  >\  ||                        |>>||
||>>|         \$/            ||  $$ --/  ||        One Hundred     |<<||
||====================================================================||>||
||//$\\\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\//$\\\||<||
||(100)==================| FEDERAL RESERVE NOTE |================(100)||>||
||\\\$//        ~         '------========--------'                \\\$//||\||
||<< /        /$\              // ____ \\\                         \ >>||)||
||>>|  12    //L\\\            // ///..) \\\         L38036133B   12 |<<||/||
||<<|        \\\ //           || <||  >\  ||                        |>>||=||
||>>|         \$/            ||  $$ --/  ||        One Hundred     |<<||
||<<|      L38036133B        *\\\  |\_/  //* series                 |>>||
||>>|  12                     *\\\/___\_//*   1989                  |<<||
||<<\      Treasurer     ______/Franklin\________     Secretary 12 />>||
||//$\                 ~|UNITED STATES OF AMERICA|~               /$\\\||
||(100)===================  ONE HUNDRED DOLLARS =================(100)||
||\\\$//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\\$//||
||====================================================================||
    """, 'green', attrs=['bold']))