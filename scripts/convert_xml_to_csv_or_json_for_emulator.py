import os
import numpy as np
import pandas as pd
from decimal import Decimal



def set_unit(x):
    d = Decimal(x)
    value = 0
    if d.as_tuple().exponent < 0:
        value = -d.as_tuple().exponent
    match value:
        case 0:
            return 'ns'
        case 3:
            return 'us'
        case 6:
            return 'ms'
        case 9:
            return 's'
        case _:
            return 'unknown'


def to_decimal(x):
    return Decimal(x)


def round_decimal(x):
    """
    round the value if it is in nanoseconds [ns]
    """
    count = float(x)
    if (count == 0.0 or count >= 1.0):
        return round(count)
  

def convert(path_from, path_to, hist_for_emulator=False):
    """
    Convert the measurement data in the XML format:
    <histogram>
        <bin low="1 ms">1</bin>
        <bin low="2 ms">4</bin>
        <bin low="3 ms">3</bin>
        <bin low="4 ms">0</bin>
    </histogram>
    to a histogram for the emulator in the CSV format [bounds, count, unit]
    or JSON format [count, lower_bound, upper_bound, unit]
    For the emulator, the units must be nanoseconds
    """
    _, extension_from = os.path.splitext(path_from)
    pkt_delays = pd.read_xml(path_from, names=['bounds', 'count'],
                         encoding='utf-8', parse_dates=[1])
    pkt_delays[['bounds', 'unit']] = pkt_delays['bounds'].str.split('\s+', expand=True)
    pkt_delays = pkt_delays.iloc[1:] # delete -inf
    pkt_delays = pkt_delays.convert_dtypes()
    pkt_delays['bounds'] = pkt_delays['bounds'].apply(lambda x: to_decimal(x))
    pkt_delays['count'] = pkt_delays['count'].apply(lambda x: to_decimal(x))
            
    if hist_for_emulator : #only [ns]
        pkt_delays.loc[pkt_delays['unit'] == 's', 'bounds'] *= 1_000_000_000
        pkt_delays.loc[pkt_delays['unit'] == 'ms', 'bounds'] *= 1_000_000
        pkt_delays.loc[pkt_delays['unit'] == 'us', 'bounds'] *= 1_000

        pkt_delays['bounds'] = pkt_delays['bounds'].apply(lambda x: round_decimal(x))
        pkt_delays.loc[pkt_delays['unit'] != 'unknown', 'unit'] = 'ns'

    _, extension_to = os.path.splitext(path_to)
    
    if extension_to.lower() == '.csv':
        pkt_delays.to_csv(path_to, index=False, encoding='utf-8', header=False)
    elif extension_to.lower() == '.json':
        pkt_delays['upper_bound'] = pkt_delays['bounds']
        order = ['count', 'bounds', 'upper_bound', 'unit']
        pkt_delays = pkt_delays.reindex(columns=order)
        pkt_delays.columns = ['count', 'lower_bound', 'upper_bound', 'unit']
        pkt_delays['upper_bound'] = pkt_delays['upper_bound'].shift(-1)
        pkt_delays = pkt_delays.drop(pkt_delays.index[-1])
        if hist_for_emulator :
            pkt_delays['upper_bound'] = pkt_delays['upper_bound'].apply(lambda x:  round_decimal(x))
        else :
            pkt_delays['upper_bound'] = pkt_delays['upper_bound'].apply(lambda x: str(x))
            pkt_delays['lower_bound'] = pkt_delays['lower_bound'].apply(lambda x: str(x))
                   
        pkt_delays.to_json(path_to, orient='records', double_precision=15)

