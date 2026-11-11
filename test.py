import pandas as pd

import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ecommerce"
)

cursor = conn.cursor()

print("Cursor created successfully!")

print("Connected to MySQL!")

#conn.close()


df = pd.read_csv("ecommerce_orders_project.csv")



df = df.drop_duplicates()



df["CustomerID"] = df["CustomerID"].fillna(0)

df["DiscountPct"] = df["DiscountPct"].fillna(0)

df["ShippingFee"] = df["ShippingFee"].fillna(0)

df["PaymentMethod"] = df["PaymentMethod"].fillna("NA")


df["OrderDate"] = pd.to_datetime(df["OrderDate"])


df["CustomerID"] = df["CustomerID"].replace(0,"Unknown")

sql = """
INSERT INTO adu_cleaned (
    OrderID, OrderDate, CustomerID, ProductID, ProductName,
    Category, City, State, Region, Quantity, UnitPrice,
    DiscountPct, GrossAmount, DiscountAmount, ShippingFee,
    NetAmount, CostAmount, Profit, PaymentMethod,
    SalesChannel, OrderStatus
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""

data = list(df.itertuples(index=False, name=None))

print("Rows prepared:", len(data))
print("Columns per row:", len(data[0]))


try:


    cursor.executemany(sql, data)
    conn.commit()
    print("successfully executed ")

except Exception as e:

    conn.rollback()
    print("error",e)


print("Rows inserted:", cursor.rowcount)


cursor.close()
conn.close()


