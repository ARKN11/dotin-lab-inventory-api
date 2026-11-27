import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger(__name__)


async def observability_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()
    response: Response | None = None

    logger.info(
        "[%s] Request started: %s %s",
        request_id,
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)
        return response

    except Exception:
        logger.exception(
            "[%s] Unexpected request error",
            request_id,
        )
        raise

    finally:
        process_time = time.perf_counter() - start_time

        if response is not None:
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

        logger.info(
            "[%s] Request finished: status=%s duration=%.4fs",
            request_id,
            response.status_code if response is not None else "ERROR",
            process_time,
        )
