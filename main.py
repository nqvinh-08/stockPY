import logging
from fastapi import FastAPI
from api.stock_router import stock_router
from fastapi.staticfiles import StaticFiles



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) #cau truc log
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock API", version="1.0.0") #tao server

app.include_router(stock_router) #dung router

app.mount("/static", StaticFiles(directory="static"), name="static") #dung cac file trong /static

logger.info("FastAPI application started")
