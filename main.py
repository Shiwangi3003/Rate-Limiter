from fastapi import FastAPI, Request
from time import time
from fastapi.responses import JSONResponse, RedirectResponse
from configuration import collection
from math import ceil
import os

app = FastAPI()

time_limit = float(os.getenv("TIME_LIMIT", "5"))
requests_no = int(os.getenv("REQUESTS_NO", "3"))
redirect_url = os.getenv("REDIRECT_URL")


@app.middleware("http")
async def rate_limiter(req: Request, call_next):
    ip = req.client.host
    ct = time()  

    log_entry = collection.find_one({"ip": ip})
    if log_entry is None:
        collection.insert_one({
            "ip" : ip,
            "times" : [ct]
        })
        if redirect_url:
            return RedirectResponse(url=redirect_url, status_code=302)
        return await call_next(req)
    else:
        updated_log = []
        for t in log_entry["times"]:
            if (ct - t) < time_limit:
                updated_log.append(t)
                        
        log_entry["times"] = updated_log
        log_entry["times"].append(ct)
        collection.find_one_and_update(
            {"ip": ip}, 
            {"$set": {"times": log_entry["times"]}}
        )

        if len(log_entry["times"]) <= requests_no:
            if redirect_url:
                return RedirectResponse(url=redirect_url, status_code=302)
            return await call_next(req)
        
    res = {
        "Status Code" : 429,
        "Error" : "Too many requests"
    }

    retry_after = max(1, ceil(min(log_entry["times"]) + time_limit - ct))
    return JSONResponse(
        status_code=429,
        content=res,
        headers={"Retry-After": str(retry_after)}
    )


@app.get('/')
def home():
    return JSONResponse({
        "message" : "Welcome"
    })
