import logging
from passlib.context import CryptContext
from config.database import client

pwd_context = CryptContext(schemes=["argon2","bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

#STOCKS
def get_stocks_data(fromDate,toDate):
    try:
        #fromDate-toDate
        querywhere=""
        if fromDate and toDate:
            querywhere = f"WHERE datetime >= '{fromDate}' AND datetime <= '{toDate}'"
        elif fromDate :
            querywhere= f"where datetime >= '{fromDate}'"
        elif toDate:
            querywhere =f"where datetime <= '{toDate}' "

        result = client.query(f"""
            SELECT * FROM stocks
            {querywhere}
            ORDER BY datetime DESC
        """)
        
        #convert dlieu sang list dictionary
        stocks = [
            dict(zip(result.column_names, row))
            for row in result.result_rows
        ]

        return stocks
    except Exception as e:
        logger.error(f"Error fetching stocks from database: {str(e)}", exc_info=True)
        raise

#LOGIN
def post_user_data(username,password):
    #lay user
    result = client.query(
        "select * from user where username = %(username)s",
        parameters={"username": username} #fix or 1=1(ko ghep chuoi truc tiep) , tach rieng sql va dlieu  
    )
    data = [
        dict(zip(result.column_names, row))
        for row in result.result_rows
    ]
    if not data:
        return False
    
    user = data[0]
    print(user["password"])
    #check user
    isMatch = pwd_context.verify(
        password,
        user["password"]
    )
    return isMatch

# REGISTER
def post_register_user(username, password):
    #check co user chua
    result = client.query(
        "select * from user where username = %(username)s",
        parameters={"username": username}
    )
    if result.result_rows:
        return False
    #hash pass
    hashPassword = pwd_context.hash(password)
    #luu user
    client.command(
        "insert into user(username, password) values(%(username)s, %(password)s)",
        parameters={"username": username, "password": hashPassword}
    )
    return True