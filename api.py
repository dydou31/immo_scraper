from fastapi import FastAPI
import asyncio
from scraper import scrape

app = FastAPI()

@app.get("/terrains")
async def get_terrains():
    data = await scrape()
    return data
