import logging
import requests
import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()
stock_router = APIRouter()
templates = Jinja2Templates(directory="views")

API_URL= os.getenv("API_URL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


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
            f"{API_URL}/api/stocks",
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
        f"{API_URL}/api/login",
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
        f"{API_URL}/api/register",
        json={
            "username": form.get("username"),
            "password": form.get("password")
        }
    )
    if response.status_code != 200: 
        return RedirectResponse("/register", status_code=303)
    
    return RedirectResponse("/login", status_code=303)

@stock_router.get("/login/google")
async def login_google():
    #chuyen sang trang dang nhap gg
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&redirect_uri=http://localhost:8000/auth/google/callback"
    )
    return RedirectResponse(google_auth_url)

@stock_router.get("/auth/google/callback")
async def callback(code:str):
    #doi code lay access token 
    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type":"authorization_code",
            "redirect_uri":"http://localhost:8000/auth/google/callback"
        }
    )
    if token_response.status_code != 200: 
        return RedirectResponse("/login", status_code=303)
    
    google_token = token_response.json()["access_token"]

    #lay thong tin user
    user_response= requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={
            "Authorization": f"Bearer {google_token}"
        },
    )
    if user_response.status_code !=200:
        return RedirectResponse("/login", status_code=303)
    user_info = user_response.json()

    #chuyen dlieu sang api
    response = requests.post(
        f"{API_URL}/api/oauth-login",
        json={
            "username":user_info.get("email"),
            "google_id": user_info.get("sub")
        }
    )
    if response.status_code !=200:
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
