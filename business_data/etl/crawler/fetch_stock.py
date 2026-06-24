import os 
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
def fetch_stock():
    url = os.getenv("URLAPI2")
    res = requests.get(url)
    data = res.json()
    if not data:
        print("khong lay duoc du lieu")
        return
    
    #tao folder 
    os.makedirs("data/raw" , exist_ok=True)
    #save data vao raw
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"data/raw/{filename}.json","w") as f: 
        json.dump(data,f) #chuyen obj -->json
    return data