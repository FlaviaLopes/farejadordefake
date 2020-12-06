# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
import numpy as np


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../interim).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    sheets = ['mar-abr', 'abr-mai', 'mai-jun', 'jun-jul', 'jul-ago', 'ago-set']
    cols = ['id','conversation_id','created_at','date','time','timezone','user_id','username','name','tweet','categoria','desinfo','mentions','urls','replies_count','retweets_count','likes_count','hashtags','link','retweet','quote_url','user_rt_id','user_rt','retweet_id','reply_to','popularidade']
    raw_data = f'{project_dir}/data/raw/tweets_aos_fatos_saude.xlsx'
    interim_data = f'{project_dir}/data/interim/'

    mar_abr = pd.read_excel(raw_data, sheet_name=sheets[0])
    abr_mai = pd.read_excel(raw_data, sheet_name=sheets[1])
    mai_jun = pd.read_excel(raw_data, sheet_name=sheets[2])
    jun_jul = pd.read_excel(raw_data, sheet_name=sheets[3])
    jul_ago = pd.read_excel(raw_data, sheet_name=sheets[4])
    ago_set = pd.read_excel(raw_data, sheet_name=sheets[5])


    mar_abr.drop(mar_abr.columns[0:2], axis=1, inplace=True)
    mar_abr.rename(columns={'desinf': 'desinfo'}, inplace=True)
    abr_mai.drop(abr_mai.columns[0:2], axis=1, inplace=True)
    mai_jun.drop(mai_jun.columns[0:2], axis=1, inplace=True)
    jun_jul.drop(jun_jul.columns[0:2], axis=1, inplace=True)
    jul_ago.drop(jul_ago.columns[0:2], axis=1, inplace=True)
    ago_set.drop(ago_set.columns[0:2], axis=1, inplace=True)

    frames = [mar_abr, abr_mai, mai_jun, jun_jul, jul_ago, ago_set]
    df = pd.concat(frames)

    df.drop(['user_rt_id', 'user_rt', 'retweet_id'], axis=1, inplace=True)
    df.desinfo = df.desinfo.replace('desinf', 'desinfo')

    df.desinfo = df.desinfo.replace('desinfo', 0)
    df.desinfo = df.desinfo.fillna(1)

    #apagar depoimentos
    df.drop(df[df.desinfo=='depoimento'].index, axis=0, inplace=True)
    df.desinfo = df.desinfo.astype(int)

    df.timezone = 'GMT-3'
    df.urls = df.urls.replace('[]', np.nan) 
    df.hashtags = df.hashtags.replace('[]', np.nan)
    df.mentions = df.mentions.replace('[]', np.nan)
    df.to_csv(f'{interim_data}tweets.csv', index=False)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    
    main()
