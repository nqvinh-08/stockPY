import os
import clickhouse_connect
def load_data(df):
    client = clickhouse_connect.get_client(
        host = os.getenv("HOSTCLICKHOUSE"),
        port=int(os.getenv("PORTCLICKHOUSE")),
        username=os.getenv("USERCLICKHOUSE"),
        password=os.getenv("PASSCLICKHOUSE"),
        database=os.getenv("DATABASECLICKHOUSE")
    )
    #duplicate
    existing = client.query("select symbol, datetime from stocks")
    existing_set = set(existing.result_rows)
    #giu lai nhung dong chua co
    df=df[
        ~df.apply( #dao nguoc boolean
            lambda row:(
                row["symbol"],
                row["datetime"]
            ) in existing_set,
            axis =1 # duyet theo tung dong
        )
    ] # co(True), khong co(false) --> ~ dao nguoc lai
    # neu ko co dlieu moi
    if df.empty:
        print("ko co dlieu moi")
        return
    df= df.sort_values("datetime", ascending=False).head(100) #sxep moi--> cu , lay 100 cai dau
    client.insert_df("stocks", df)
    print("them dlieu thanh cong")