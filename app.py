import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.warning(f"Rate limit exceeded: {request.client.host}")
    return JSONResponse(
        content={"error": "Too Many Requests"}, status_code=429
    )

@app.get("/DDos_test")
@limiter.limit("10/second")
async def test_endpoint(request: Request) -> dict:
    logger.info(f"Request processed from {request.client.host}")
    return {"message": "Request successful"}
