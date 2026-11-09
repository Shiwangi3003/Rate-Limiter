# 🚦 Rate Limiter API

A FastAPI middleware-based **Rate Limiter** that restricts the number of requests per IP address within a defined time window, backed by **MongoDB**.

---
✨ **Features**
- **Sliding-window limiting** per client IP (timestamps are stored and pruned on every request)
- **Configurable** window size and request cap via environment variables
- **Retry-After header** on 429 responses so clients know when to try again
- **Optional redirect mode:** send every allowed request to a URL of your choice
- **Persistent counters** in MongoDB, so limits survive server restarts and are shared across app instances
- Drop-in middleware: no changes needed to your route handlers

## 🚀 Tech Stack

 Layer | Technology |
|-------|------------|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |
| Database | [MongoDB](https://www.mongodb.com/) via [PyMongo](https://pymongo.readthedocs.io/) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |
| Language | Python 3.9+ |

---

## ⚙️ Setup & Installation

### Prerequisites
 
- Python 3.9 or newer
- A MongoDB instance: [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier works) or a local `mongod`

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Rate-Limiter.git
   cd Rate-Limiter
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root (it is already git-ignored):
 
```env
# Required
MONGODB_URL=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
 
# Optional (defaults shown)
TIME_LIMIT=5
REQUESTS_NO=3

# REDIRECT_URL=https://example.com
```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the interactive docs**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Configuration

All settings come from environment variables.
 
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGODB_URL` | ✅ Yes | none | MongoDB connection string |
| `TIME_LIMIT` | No | `5` | Length of the sliding window, in **seconds** (floats allowed) |
| `REQUESTS_NO` | No | `3` | Max requests allowed per IP within the window |
| `REDIRECT_URL` | No | unset | If set, every *allowed* request is answered with a `302` redirect to this URL instead of reaching the route handler |
 
**Database layout:** database `rates_db`, collection `rates_db`. Each document looks like:
 
```json
{
  "ip": "203.0.113.42",
  "times": [1731050000.12, 1731050001.48, 1731050002.97]
}
```
 
`times` holds Unix timestamps of the client's recent requests.
 
---
 

## 🔌 API Endpoints

### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| ➤ `GET` | `/` | welcome message |

#### ➤ `GET /`
Returns a welcome message.

**Response `200`:**
```json
{
  "message": "Welcome"
}
```

---

### Rate-limited response
 
When a client exceeds the limit, any endpoint returns:
 
**Response `429 Too Many Requests`**
 
```json
{
  "Status Code": 429,
  "Error": "Too many requests"
}
```
 
Headers:
 
| Header | Description |
|--------|-------------|
| `Retry-After` | Minimum number of seconds (at least 1) until the client's oldest request leaves the window |
 
---
 

## ⚠️ Known Limitations

- **Rejected requests still count.** The current timestamp is recorded even when a request is blocked, so a client that keeps hammering the API stays blocked until it stops for a full `TIME_LIMIT` window.
- **Global limit only.** The same limit applies to every route; there is no per-endpoint or per-user configuration.
- **IP detection.** The limiter uses `request.client.host`. Behind a reverse proxy or load balancer this may be the proxy's IP unless you configure forwarded headers (e.g. `uvicorn --proxy-headers`).
- **Not atomic.** The read-modify-write against MongoDB is not atomic, so heavy concurrent traffic from one IP can briefly slip past the limit.
- **Stale data accumulates.** Documents for IPs that stop visiting are never removed. Consider a cleanup job or a TTL index.
- **Extra latency.** Every request makes at least one round trip to MongoDB.
- No authentication or authorization is implemented.
---

## 📄 License

This project is open-source. Feel free to use and modify it.

---

## 👩‍💻 Author

Shiwangi
[GitHub Profile](https://github.com/Shiwangi3003)
