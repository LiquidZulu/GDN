from ENV import *
from util import *
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import *
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "HTML landing page has yet to be created, please go to ./docs or ./redoc for Swagger UI or ReDoc documentation. I am planning to make self hosting docs at some point so that fastly, netlify and tiangolo dont need to connect for my fellow privacy nuts."}


@app.get("/json_scraperless/{year}-{month}-{day}")
async def date_json_scraperless_response(year: int, month: int, day:int):
    return {
        "iimages": await iimages(year, month, day),
        "cloudfront": await cloudfront(year, month, day)
    }

@app.get("/comic_scraperless/{year}-{month}-{day}")
async def comic_scraperless(year: int, month: int, day:int):

    iimages_res = await iimages(year, month, day)

    if(iimages_res[STATUS_OK][IIMAGES_LARGE]):
        return RedirectResponse(iimages_res[URLS][IIMAGES_LARGE])
    
    cloudfront_res = await cloudfront(year, month, day)

    if(cloudfront_res[STATUS_OK]):
        return RedirectResponse(cloudfront_res[URLS])
    
    raise HTTPException(status_code=404, detail=f'''Comic for {year}-{month}-{day} not found on scraperless CDNs''')