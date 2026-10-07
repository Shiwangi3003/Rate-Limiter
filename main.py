from fastapi import FastAPI, Request
from time import time
from fastapi.responses import JSONResponse
from configuration import collection
from math import ceil
import os

app = FastAPI()

time_limit = os.getenv("TIME_LIMIT")
requests_no = os.getenv("REQUESTS_NO")


@app.middleware("http")
async def rate_limiter(req: Request, call_next):
    # current time and ip address of device requesting
    ip = req.client.host
    ct = time()  

    log_entry = collection.find_one({"ip": ip})
    if log_entry == None:
        collection.insert_one({
            "ip" : ip,
            "times" : [ct]
        })
        res = await call_next(req)
        return res
    else:
        updated_log = []
        for t in log_entry["times"]:
            if (ct - t) < time_limit:
                updated_log.append(t)
        log_entry["times"] = updated_log
        log_entry["times"].append(ct)
        collection.find_one_and_update_one({"ip":ip},{"$set": log_entry})

        if len(log_entry["times"]) <= requests_no:
            res = await call_next(req)
            return res
        
    res = {
        "Status Code" : 429,
        "Error" : "Too many requests"
    }

    retry_after = max(1, ceil(min(log_entry["times"]) + float(time_limit) - ct))
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
