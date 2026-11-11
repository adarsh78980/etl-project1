import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sakila"

)

print("Connected to MySQL!")

# connection.close()

import pandas as pd

df = pd.read_csv("store_performance_dataset - Sheet1.csv")

df["Date"] = pd.to_datetime(df["Date"]).dt.date

print(df.head())

print(df.shape)

print(df.columns)

 #print(df.dtypes)


 #print(df[df["Discounts"].isnull()])

 #print(df[df["Returns"].isnull()])

df["Discounts"] = df["Discounts"].fillna(0)

df["Returns"] = df["Returns"].fillna(0)

print(df.isnull().sum())

# print(df.dtypes)

cursor = connection.cursor() 

for _, row in df.iterrows():

    sql = """
    INSERT INTO store_performance (
        Date, DayOfWeek, StoreID, StoreName, City, State, Region,
        StoreType, SalesChannel, Category, Transactions, UnitsSold,
        GrossSales, Discounts, Returns, NetSales, COGS, Profit,
        AvgTicket, ProfitMarginPct
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = tuple(row)

    cursor.execute(sql, values)

connection.commit()

print("Data inserted successfully!")

