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
@stock_router.get("/")
async def index(request: Request):
    """
        Hiển thị trang chủ và danh sách dữ liệu cổ phiếu.
        Lấy JWT token từ Cookie, gọi API để lấy dữ liệu cổ phiếu theo
        khoảng thời gian được chọn và hiển thị lên giao diện.
        Args:
            request (Request): Đối tượng Request chứa Cookie và Query Parameters.
        Returns:
            TemplateResponse: Trang index.html chứa danh sách cổ phiếu và
            thông tin người dùng.
    """
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
    """
        Hiển thị trang đăng nhập.
    """
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )

#LOGIN /POST
@stock_router.post("/login")
async def login(request:Request):
    """
        Xử lý đăng nhập người dùng.
        Nhận username và password từ form, gửi đến API xác thực.
        Nếu đăng nhập thành công sẽ lưu JWT token vào Cookie và
        chuyển hướng về trang chủ.
        Args:
            request (Request): Đối tượng Request chứa dữ liệu form.
        Returns:
            RedirectResponse: Chuyển hướng đến trang chủ nếu thành công,
            hoặc quay lại trang đăng nhập nếu thất bại.
    """
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
    """
        Hiển thị trang đăng ki.
    """
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )

#REGISTER /POST
@stock_router.post("/register")
async def register(request:Request):
    """
        Xử lý đăng ký tài khoản.
        Nhận thông tin đăng ký từ form và gửi đến API để tạo tài khoản mới.
        Nếu đăng ký thành công sẽ chuyển đến trang đăng nhập.
        Args:
            request (Request): Đối tượng Request chứa dữ liệu form.
        Returns:
            RedirectResponse: Chuyển đến trang đăng nhập nếu đăng ký thành công,
            hoặc quay lại trang đăng ký nếu thất bại.
    """
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

# LOGIN_GOOGLE
@stock_router.get("/login/google")
async def login_google():
    """
        Chuyển hướng người dùng đến trang đăng nhập Google.

        Tạo URL xác thực OAuth2 của Google và chuyển hướng người dùng
        đến trang đăng nhập Google.

        Returns:
            RedirectResponse: Trang đăng nhập Google.
    """
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
    """
        Xử lý callback sau khi đăng nhập Google.
        Nhận authorization code từ Google, đổi lấy access token,
        lấy thông tin người dùng, gửi đến API để xác thực và
        lưu JWT token vào Cookie.
        Args:
            code (str): Authorization code do Google trả về sau khi
            người dùng đăng nhập thành công.
        Returns:
            RedirectResponse: Chuyển đến trang chủ nếu xác thực thành công,
            hoặc quay lại trang đăng nhập nếu xảy ra lỗi.
    """
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
