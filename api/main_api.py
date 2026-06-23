import logging
from fastapi import FastAPI
from router.stock_router import stock_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) #cau truc log
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock API", version="1.0.0") #tao server

app.include_router(stock_router, prefix="/api") #dung router

logger.info("FastAPI application started")
