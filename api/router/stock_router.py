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
    """
        Dang nhap nguoi dung , check username va password. 
        Tao token neu dung tra ve access_token cho client
        Arg:
            username,password
        Retrun :
            access_token
    """
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
    """
        Kiem tra va them nguoi vao db 
        arg: 
            username, password
        return: 
            message
    """
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
    """
        Xác thực JWT token từ Authorization Header, giải mã để lấy thông tin
        người dùng và trả về danh sách cổ phiếu theo khoảng thời gian nếu được chỉ định.

        Args:
            fromDate (str, optional): Ngày bắt đầu lọc dữ liệu (YYYY-MM-DD).
            toDate (str, optional): Ngày kết thúc lọc dữ liệu (YYYY-MM-DD).
            authorization (str): JWT token trong Header theo định dạng
                "Bearer <access_token>".

        Returns:
            dict: Bao gồm username của người đăng nhập và danh sách dữ liệu cổ phiếu.
    """
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
    """
        Kiểm tra username và google_id, tạo JWT token nếu xác thực thành công
        và trả về access token cho client.
        Args:
            payload (OauthLogin): Thông tin đăng nhập Google gồm username và google_id.
        Returns:
            dict: Chứa access_token nếu đăng nhập thành công.
    """
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