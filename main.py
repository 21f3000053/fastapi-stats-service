import time
import uuid
from fastapi import FastAPI, Request, Response, HTTPException

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-hv15xk.example.com"
YOUR_EMAIL = "21f3000053@ds.iitm.study.ac.in"  # Replace with your actual logged-in email

@app.middleware("http")
async def add_cors_and_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("origin")

    # Handle CORS preflight and actual requests explicitly
    if request.method == "OPTIONS":
        response = Response(status_code=200)
    else:
        response = await call_next(request)

    # Attach required custom response headers
    process_time = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    # Enforce strict per-origin CORS policy
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"] = "86400"

    return response

@app.get("/stats")
def get_stats(values: str):
    try:
        nums = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integers provided")

    if not nums:
        raise HTTPException(status_code=400, detail="No values provided")

    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = total_sum / count

    return {
        "email": YOUR_EMAIL,
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }