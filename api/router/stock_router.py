import logging
import jwt
import os
from fastapi import APIRouter, HTTPException,Header
from business_data.services.stock_service import get_stocks_data , post_user_data, post_register_user, login_google
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel
from business_data.schemas.user import User


logger = logging.getLogger(__name__)
load_dotenv()
stock_router = APIRouter()

# LOGIN /POST
@stock_router.post("/login")
async def login(body: User):
    try:
        #check user
        isMatch = post_user_data(body.username, body.password)
        if not isMatch:
            raise HTTPException(status_code=401)
        
        #tao token
        token = jwt.encode(
            {
                "username":body.username,
                "exp":datetime.utcnow() + timedelta(hours=1)
            },
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )
        return {"access_token":token}
    except Exception as e:
        logger.error(f"loi: {str(e)}", exc_info=True)
        raise

# REGISTER /POST
@stock_router.post("/register")
async def register(body: User):
    try:
        #them user
        success = post_register_user(body.username, body.password)
        if not success:
            raise HTTPException(status_code=400)
        
        return {"message":"success"}
    
    except Exception as e:
        logger.error(f"loi lay stocks: {str(e)}", exc_info=True)
        raise

#STOCK /GET
@stock_router.get("/stocks")
async def index(
    fromDate: str = None,
    toDate: str = None,
    authorization: str = Header(None)): #ko bat buoc phai co fromdate/todate
    #check token
    if not authorization:
        raise HTTPException(status_code=401)
    
    #tach token
    token = authorization.replace("Bearer ", "")

    #giai ma token
    payload = jwt.decode(
        token,
        os.getenv("JWT_SECRET"),
        algorithms=["HS256"]
    )

    stocks = get_stocks_data(fromDate, toDate)
    return {
        "username": payload["username"],
        "stocks": stocks
    }

class OauthLogin(BaseModel):
    username: str
    google_id: str
    
@stock_router.post("/oauth-login")
async def oauth_login(payload: OauthLogin):
    isMatch = login_google(payload.username, payload.google_id)
    if not isMatch :
        raise HTTPException(status_code=401)
    #tao token
    token = jwt.encode(
        {
            "username":payload.username,
            "exp":datetime.utcnow() + timedelta(hours=1)
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )
    return {"access_token":token}