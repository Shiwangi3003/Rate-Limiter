# 🚦 Rate Limiter API

A FastAPI middleware-based **Rate Limiter** that restricts the number of requests per IP address within a defined time window, backed by **MongoDB**.

---

## 🚀 Tech Stack

- **Framework:** FastAPI
- **Database:** MongoDB (via PyMongo)
- **Language:** Python 3.x
- **Middleware:** HTTP Rate Limiting

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/rate-limiter-api.git
   cd rate-limiter-api
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi pymongo uvicorn
   ```

3. **Configure MongoDB connection**
   Update your MongoDB URI and collection name in `configuration.py`.

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the interactive docs**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Rate Limiter Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `time_limit` | `5` seconds | Time window for request tracking |
| `requests_no` | `3` | Max allowed requests per IP within the time window |

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

## 🛡️ Middleware — Rate Limiter

Every incoming HTTP request passes through the `rate_limiter` middleware:

- Extracts the client's **IP address** and **current timestamp**.
- Looks up the IP in MongoDB.
- If the IP is **new**, it logs the request and allows it through.
- If the IP **exists**, it filters out timestamps older than `time_limit` seconds and checks the count.
- If requests within the window are within `requests_no`, the request is allowed.
- If the limit is **exceeded**, a `429 Too Many Requests` response is returned.

**Response `429`:**
```json
{
  "Status Code": 429,
  "Error": "Too many requests"
}
```

---

## ⚠️ Known Limitations

- Rate limit counters are stored in MongoDB; high traffic may introduce slight latency.
- No per-route rate limiting — the limit applies globally to all endpoints.
- No authentication or authorization is implemented.

---

## 📄 License

This project is open-source. Feel free to use and modify it.

---

## 👩‍💻 Author

Shiwangi
[GitHub Profile](https://github.com/Shiwangi3003)
