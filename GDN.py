from ENV import *
from util import *
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import *
import requests
from fastapi.middleware.wsgi import WSGIMiddleware
from vibora import Vibora, Response

wgsi_app = Vibora()


@wgsi_app.route("/test")
async def flask_main():
    return PAGES[LANDING_PAGE]


@wgsi_app.route("/json/<year>-<month>-<day>/scraperless")
async def flask_date_json_scraperless_response(year:int, month:int, day:int):
    return {
        "iimages": await iimages(year, month, day),
        "cloudfront": await cloudfront(year, month, day)
    }

app = FastAPI()

@app.get("/")
async def root():
    return PAGES[LANDING_PAGE]


@app.get("/v2/json/{year}-{month}-{day}/scraperless")
async def date_json_scraperless_response(year:int, month:int, day:int):
    return {
        "iimages": await iimages(year, month, day),
        "cloudfront": await cloudfront(year, month, day)
    }

@app.get("/v2/comic/{year}-{month}-{day}/scraperless")
async def comic_scraperless(year:int, month:int, day:int):

    iimages_res = await iimages(year, month, day)

    if(iimages_res[STATUS_OK][IIMAGES_LARGE]):
        return RedirectResponse(iimages_res[URLS][IIMAGES_LARGE])
    
    cloudfront_res = await cloudfront(year, month, day)

    if(cloudfront_res[STATUS_OK]):
        return RedirectResponse(cloudfront_res[URLS])
    
    raise HTTPException(status_code=404, detail=f'''Comic for {year}-{month}-{day} not found on scraperless CDNs''')


app.mount("/v1", WSGIMiddleware(wgsi_app))