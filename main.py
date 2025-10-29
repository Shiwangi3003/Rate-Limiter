from fastapi import FastAPI, Request
from time import time
from fastapi.responses import JSONResponse
from configuration import collection
from database.schema import log_data

app = FastAPI()

time_limit = 5
requests_no = 3


@app.middleware("http")
async def rate_limiter(req: Request, call_next):
    # current time and ip address
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
        collection.update_one({"ip":ip},{"$set": log_entry})

        if len(log_entry["times"]) <= requests_no:
            res = await call_next(req)
            return res
        
    res = {
        "Status Code" : 429,
        "Error" : "Too many requests"
    }
    return JSONResponse(status_code= 429,content = res)



@app.get('/')
def home():
    return JSONResponse({
        "message" : "Welcome"
    })

