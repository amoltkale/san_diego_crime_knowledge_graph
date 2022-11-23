import string

import pandas as pd

import emoji

def translate_emojis(df, col):
    # source: https://stackoverflow.com/a/69423881
    df[col] =  df[col].apply(lambda x: ''.join((' '+c+' ') if c in emoji.UNICODE_EMOJI['en'] else c for c in x))
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
    df[new_col] = df[col].apply(lambda x: len(x.split(' ')))
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