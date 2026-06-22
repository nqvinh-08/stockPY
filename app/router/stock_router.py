import logging
import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()
stock_router = APIRouter()
templates = Jinja2Templates(directory="views")

api_url="http://api:8000"

#STOCKS /GET
@stock_router.get("/") # api get co dg dan /
async def index(request: Request): #ham index()
    try:
        #lay token
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login", status_code=303)
        
        #goi API
        response = requests.get(
            f"{api_url}/api/stocks",
            params={
                "fromDate":request.query_params.get("fromDate"),
                "toDate":request.query_params.get("toDate")
            },
            headers={
                "Authorization":f"Bearer {token}"
            }
        )
        if response.status_code != 200:
            return RedirectResponse("/login", status_code=303)
        
        data = response.json() 

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={   
                "stocks": data["stocks"],
                "username":data["username"]
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

#LOGIN /POST
@stock_router.post("/login")
async def login(request:Request):
    form = await request.form()
    response = requests.post(
        f"{api_url}/api/login",
        json={
            "username": form.get("username"),
            "password": form.get("password")
        }
    )
    if response.status_code != 200: 
        return RedirectResponse("/login", status_code=303)
    # nhan tokenn --> luu vao cookie
    token = response.json()["access_token"]
    res= RedirectResponse("/",status_code=303)
    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )
    return res

# REGISTER /GET
@stock_router.get("/register")
async def register_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )

#REGISTER /POST
@stock_router.post("/register")
async def register(request:Request):
    form = await request.form()

    response = requests.post(
        f"{api_url}/api/register",
        json={
            "username": form.get("username"),
            "password": form.get("password")
        }
    )
    if response.status_code == 200: 
        return RedirectResponse("/login", status_code=303) 
    
    return RedirectResponse("/register", status_code=303)