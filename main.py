import time
import uuid
from fastapi import FastAPI, Request, Response, HTTPException

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-hv15xk.example.com"
YOUR_EMAIL = "your-email@example.com"  # Replace with your actual logged-in email

@app.middleware("http")
async def cors_and_headers_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("origin")

    # Handle Preflight OPTIONS requests
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        # Only inject ACAO if the incoming origin matches the allowed one exactly
        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("access-control-request-headers", "*")
            response.headers["Access-Control-Max-Age"] = "86400"
        # If origin doesn't match or is missing, no ACAO header is returned (strict rejection)
        
        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response

    # Process standard requests (GET, etc.)
    response = await call_next(request)

    # Attach CORS header to actual responses if origin matches
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    process_time = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
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