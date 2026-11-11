import mysql.connector

import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sakila"
)

print("Connected to MySQL!")





df = pd.read_csv("ecommerce_orders_project.csv")

print(df.head())

print(df.shape)
print(df.columns)
print(df.dtypes)

#print(df.isnull().sum())

 #print(df[df["CustomerID"].isnull()])

#print(df[df["DiscountPct"].isnull()])


#print(df[df["ShippingFee"].isnull()])

#print(df[df["PaymentMethod"].isnull()])

df["CustomerID"] = df["CustomerID"].fillna(0)

df["ShippingFee"] = df["ShippingFee"].fillna(0)

df["PaymentMethod"] =df["PaymentMethod"].fillna("NA")

df["DiscountPct"] =df["DiscountPct"].fillna(0)

print(df.isnull().sum())



df["OrderDate"] = pd.to_datetime(df["OrderDate"])

 #print(df.duplicated().sum())  TO SEE NO OF DUPLICATE 


df = df.drop_duplicates()

#print(df[df.duplicated(keep=False)]) TO SEE THE DUPLICATE

print(df.shape)

cursor = connection.cursor()

for _, row in df.iterrows():
    sql = """
INSERT INTO adu (
    OrderID, OrderDate, CustomerID, ProductID, ProductName,
    Category, City, State, Region, Quantity,
    UnitPrice, DiscountPct, GrossAmount, DiscountAmount,
    ShippingFee, NetAmount, CostAmount, Profit,
    PaymentMethod, SalesChannel, OrderStatus
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s
)
"""
    values = tuple(row)
    cursor.execute(sql, values)

connection.commit()


print("Data inserted successfully!")

cursor.close()
connection.close()

