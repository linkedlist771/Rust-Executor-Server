
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException
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


app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTPException caught: {exc.detail}, Status Code: {exc.status_code}")
    if exc.status_code == 404:
        return Response(content=None, status_code=exc.status_code)
    return Response(content=str(exc.detail), status_code=exc.status_code)


@app.post("/run_rust_code", response_model=BaseResponse)
async def run_rust_code(request: BaseRequest):
    logger.info(f"Received rust code: {request.rust_code}")
    output, compile_error = create_and_run_rust_project(request.rust_code)
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

