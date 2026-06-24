import pandas as pd
def clean_data(data):
    stocks=[]
    time_series= data["Time Series (Daily)"] #lay du lieu
    for date, values in time_series.items():
        stock ={
            "symbol":data.get("Meta Data",{}).get("2. Symbol"),
            "open":float(values["1. open"]),
            "high":float(values["2. high"]),
            "low": float(values["3. low"]),
            "close":float(values["4. close"]),
            "volume":float(values["5. volume"]),
            "datetime": pd.to_datetime(date) #chueyn ve kieu datetime cua pd
        }
        stocks.append(stock) #them vao mang
    df = pd.DataFrame(stocks) # list-->bang
    df= df.dropna()
    df= df.drop_duplicates()
    return df