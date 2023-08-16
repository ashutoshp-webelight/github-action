import json
from typing import Union

from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next) -> Union[JSONResponse, Response]:
        response = await call_next(request)
        content_type = response.raw_headers[1][1]

        if not content_type == "text/html; charset=utf-8".encode("utf-8"):
            bytes_ = [body async for body in response.__dict__["body_iterator"]][0]
        else:
            return response

        body = json.loads(bytes_.decode("utf-8"))

        if isinstance(body, dict):
            if not body.get("openapi"):
                if response.status_code == 200:
                    send = {"status": "success", "status_code": response.status_code, "data": body}
                    result = JSONResponse(status_code=response.status_code, content=send)
                else:
                    result = JSONResponse(status_code=response.status_code, content=body)

            else:
                result = Response(
                    content=bytes_,
                    status_code=response.status_code,
                    headers={"Content-Type": "application/json"},
                    media_type=response.media_type,
                    background=response.background,
                )

        else:
            send = {"status": "success", "status_code": response.status_code, "data": body}
            result = JSONResponse(status_code=response.status_code, content=send)

        return result
