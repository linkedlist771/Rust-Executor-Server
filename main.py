import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Security
from fastapi.responses import Response
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_403_FORBIDDEN
import argparse
import fire
import uvicorn
import copy
from loguru import logger
from utils import create_and_run_rust_project
from schemas import BaseRequest, BaseResponse

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="0.0.0.0", help="host")
parser.add_argument("--port", default=8000, help="port")
args = parser.parse_args()

API_KEY_NAME = "X-API-KEY"
API_KEY = "dinglizuibangl, hahahahah"  # Replace with your actual API key
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key: str = Security(api_key_header),
):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )


app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTPException caught: {exc.detail}, Status Code: {exc.status_code}")
    if exc.status_code == 404:
        return Response(content=None, status_code=exc.status_code)
    return Response(content=str(exc.detail), status_code=exc.status_code)


@app.post("/run_rust_code", response_model=BaseResponse)
async def run_rust_code(
    request: BaseRequest,
    api_key: APIKey = Security(get_api_key),
):
    logger.info(f"Received rust code: \n{request.rust_code}")
    output, compile_error = create_and_run_rust_project(request.rust_code)
    logger.info(f"Output: \n{output}")

    if compile_error:
        return BaseResponse(message="Rust code failed to compile, check data for details.", data=output, code=400)
    else:
        return BaseResponse(message="Rust code executed successfully, check data for details.", data=output, code=200)


def start_server(port=args.port, host=args.host):
    logger.info(f"Starting server at {host}:{port}")
    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config=config)
    try:
        server.run()
    finally:
        logger.info("Server shutdown.")


if __name__ == "__main__":
    fire.Fire(start_server)

