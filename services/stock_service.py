import logging
import bcrypt
from config.database import client
from passlib.hash import bcrypt



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
    result = client.query(f"""
        select *from user
        where username ='{username}'
    """)
    data = [
        dict(zip(result.column_names, row))
        for row in result.result_rows
    ]
    if not data:
        return False
    
    user = data[0]

    #check user
    isMatch = bcrypt.verify(
        password,
        user["password"]
    )
    return isMatch

# REGISTER
def post_register_user(username, password):
    result = client.query(f"""
        select *from user
        where username ='{username}'
    """)
    if result.result_rows:
        return False
    
    hashPassword = bcrypt.hash(password)

    client.command(f"""
        insert into user(username, password)
        values('{username}','{hashPassword}')
    """)
    return True