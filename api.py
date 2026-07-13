import subprocess
import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/terrains")
async def get_terrains():
    result = subprocess.check_output(["node", "scraper.js"])
    data = json.loads(result)
    return data