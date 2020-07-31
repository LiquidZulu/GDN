from ENV import *
from typing import Optional
from fastapi import FastAPI
import requests

async def iimages(year: int, month: int, day:int):

    ymd     = [int(str(year)[2:]),month,day]
    ymd_str = ['00','00','00']

    for i in range(len(ymd)):

        if ymd[i] < 10:
            ymd_str[i] = f'''0{ymd[i]}'''
        else:
            ymd_str[i] = str(ymd[i])

    urls = [
        f'''http://strips.garfield.com/iimages1200/{year}/ga{ymd_str[0]}{ymd_str[1]}{ymd_str[2]}.gif''',
        f'''http://strips.garfield.com/iimages/{year}/ga{ymd_str[0]}{ymd_str[1]}{ymd_str[2]}.gif''',
        f'''http://strips.garfield.com/bwiimages1200/{year}/ga{ymd_str[0]}{ymd_str[1]}{ymd_str[2]}.gif'''
    ]
    resps = [False,False,False]
    
    for i in range(len(urls)):
        resp = requests.head(urls[i])
        resps[i] = resp.ok
    
    return resps


async def cloudfront(year: int, month: int, day:int):
    
    ymd     = [year,month,day]
    ymd_str = ['00','00','00']

    for i in range(len(ymd)):

        if ymd[i] < 10:
            ymd_str[i] = f'''0{ymd[i]}'''
        else:
            ymd_str[i] = str(ymd[i])
    
    return requests.head(f'''https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/{year}/{ymd_str[0]}-{ymd_str[1]}-{ymd_str[2]}.gif''').ok