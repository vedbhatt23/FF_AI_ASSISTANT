"""
Security middleware: API key validation, rate limiting, request logging.
"""
import logging, time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import get_settings

logger = logging.getLogger(__name__)

# In-memory rate limiting store
_rate_store: dict[str, list[float]] = defaultdict(list)


class SecurityMiddleware(BaseHTTPMiddleware):
    """API key validation and rate limiting middleware."""

    EXEMPT_PATHS = {"/api/health", "/docs", "/openapi.json", "/redoc"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Skip auth for exempt paths and OPTIONS
        if path in self.EXEMPT_PATHS or request.method == "OPTIONS":
            return await call_next(request)

        settings = get_settings()

        # API Key validation
        api_key = request.headers.get("X-API-Key", "")
        if not api_key or api_key != settings.API_KEY:
            logger.warning(f"Unauthorized request to {path} from {request.client.host}")
            raise HTTPException(status_code=401, detail="Invalid or missing API key")

        # Rate limiting
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = 60  # 1 minute window
        _rate_store[client_ip] = [t for t in _rate_store[client_ip] if now - t < window]
        if len(_rate_store[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        _rate_store[client_ip].append(now)

        # Log request
        logger.info(f"{request.method} {path} from {client_ip}")
        response = await call_next(request)
        return response
