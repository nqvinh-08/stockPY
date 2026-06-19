import logging
import jwt
import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.stock_service import get_stocks_data , post_user_data, post_register_user
from datetime import datetime, timedelta
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()
stock_router = APIRouter()
templates = Jinja2Templates(directory="views")

#STOCKS /GET
@stock_router.get("/") # api get co dg dan /
async def index(request: Request): #ham index()
    try:
        #lay token
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login", status_code=303)
        try:

            #giai ma tocken va check
            payload= jwt.decode(
                token,
                os.getenv("JWT_SECRET"),
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return RedirectResponse("/login",status_code=303)
        except jwt.InvalidTokenError:
            return RedirectResponse("/login",status_code=303)
        
        fromDate = request.query_params.get("fromDate")
        toDate = request.query_params.get("toDate")
        print(fromDate)
        print(toDate)

        stock = get_stocks_data(fromDate,toDate)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "stock": stock,
                "username":payload["username"]
            },
        )
    except Exception as e:
        logger.error(f"loi lay stocks: {str(e)}", exc_info=True)
        raise

#LOGIN /GET
@stock_router.get("/login")
async def login_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )

# LOGIN /POST
@stock_router.post("/login")
async def login(request: Request):
    try:
        body = await request.form()
        username = body.get("username")
        password = body.get("password")
        isMatch = post_user_data(username,password)
        if isMatch:
            
            #tao token
            token = jwt.encode(
                {
                    "username": username,
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                os.getenv("JWT_SECRET"),
                algorithm="HS256"
            )
            response = RedirectResponse(
                url="/",
                status_code=303
            )

            response.set_cookie(
                key="access_token", #ten cookie
                value=token,
                httponly=True
            )
            return response   
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    except Exception as e:
        logger.error(f"loi lay stocks: {str(e)}", exc_info=True)
        raise


# REGISTER /GET
@stock_router.get("/register")
async def register_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )

# REGISTER /POST
@stock_router.post("/register")
async def register(request: Request):
    try:
        body = await request.form()
        username = body.get("username")
        password = body.get("password")

        success = post_register_user(username,password)
        if success:
            return RedirectResponse(url="/login",status_code=303)
        
        return RedirectResponse(url="/register",status_code=303)
    
    except Exception as e:
        logger.error(f"loi lay stocks: {str(e)}", exc_info=True)
        raise


