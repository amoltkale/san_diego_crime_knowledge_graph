import string

import pandas as pd

import emoji
from datetime import datetime

def translate_emojis(df, col):
    # source: https://stackoverflow.com/a/69423881
    df[col] =  df[col].apply(lambda x: ''.join((' '+c+' ') if c in emoji.UNICODE_EMOJI['en'] else c for c in str(x)))
    df[col] =  df[col].apply(lambda x: emoji.demojize(x))
    return df

def remove_puncuations(df, col, *, keep=None):
    # remove special char combinations
    df[col] = df[col].replace(r'&amp;',' ', regex=True)
    df[col] = df[col].replace(r'\n',' ', regex=True)
    if keep is None:
        remove = string.punctuation
    else:
        remove = ''.join(list(set(string.punctuation).difference(set(keep))))
    df[col] = df[col].apply(lambda x: x.translate(str.maketrans('', '', remove)))
    return df
    
def add_word_count(df, col):
    new_col = f"{col}_count"
    df[new_col] = df[col].apply(lambda x: len(x.split()))
    return df

def concat_str_cols(df, col_a, col_b, merge_col, *, delimiter = ' '):
    df[merge_col] = df[col_a] + delimiter + df[col_b]
    df[merge_col] = df[merge_col].apply(lambda x: ' '.join(x.split()))
    return df

def clean_str_col(df, col):
    df = translate_emojis(df, col)
    # remove urls and embedded gifs/giphy
    # source https://stackoverflow.com/a/51994366
    df[col] = df[col].replace(r'gif', '', regex=True).replace(r'giphy\S+', '', regex=True)
    df[col] = df[col].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)

    
    df = remove_puncuations(df, col, keep=['.', ' '])
    df[col] = df[col].str.lower()
    return df


def bin_the_date(x):
    ''' This function returns binned time of the day given the hour of the day.'''
    if (x > 4) and (x <= 8):
        return 'Early Morning'
    elif (x > 8) and (x <= 12 ):
        return 'Morning'
    elif (x > 12) and (x <= 16):
        return'Noon'
    elif (x > 16) and (x <= 20) :
        return 'Evening'
    elif (x > 20) and (x <= 24):
        return'Night'
    elif (x <= 4):
        return'Late Night'



def get_binned_tod(date):
    ''' This function returns hour of the day given the timestamp.'''
    d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return bin_the_date(d.hour)


def get_binned_tod_col(df, col):
    ''' This function returns pd dataframe with the binned time of the data.'''
    new_col = f"{col}_bin"
    df[new_col] = df[col].apply(lambda x: get_binned_tod(x))
    return df