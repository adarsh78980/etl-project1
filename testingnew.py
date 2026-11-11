import pandas as pd

import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ecommerce"
)


cursor = conn.cursor()




def extract_data():
    df = pd.read_csv("ecommerce_orders_project.csv")
    return df

def clean_data(df):

    df = df.drop_duplicates()
    df["CustomerID"] = df["CustomerID"].fillna("Unknown")

    df["DiscountPct"] = df["DiscountPct"].fillna(0)

    df["ShippingFee"] = df["ShippingFee"].fillna(0)

    df["PaymentMethod"] = df["PaymentMethod"].fillna("NA")


    df["OrderDate"] = pd.to_datetime(df["OrderDate"])


    #df["CustomerID"] = df["CustomerID"].replace(0,"Unknown") 

    return df

def validate_data(df):

    nag=df[df["Quantity"]<=0].reset_index()
    
    print("negative quantity",nag.shape[0])

    if (df["OrderID"].isnull().sum() == 0  and df["CustomerID"].isnull().sum() == 0 and  (df["Quantity"] > 0).all()):

        

        

        return True
    else:
        
        return False



def load_data(df):

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

    try:

        cursor.execute("delete from adu_cleaned")


        cursor.executemany(sql, data)
        conn.commit()
        print("successfully executed ")
        return cursor.rowcount

    except Exception as e:

        conn.rollback()
        print("ETL failed:", e)
        return None

    #finally:
       # cursor.close()
       # conn.close()

    

df = extract_data()

print("Before cleaning:", df.shape)

df = clean_data(df)

#df.loc[df.index[0], "Quantity"] = 0  




df.loc[df.index[0],"Quantity"] = 0

invalid = df[df["Quantity"]<=0]



print("quantity",invalid.shape[0])


valid = df[df["Quantity"]>0]

print("quantity",valid.shape[0])

invalid.to_csv("rejected_records.csv", index=False)

ans = validate_data(valid)

if (ans==True):
    inserted = load_data(valid)
    print(inserted)
else:


    print("Data validation failed. Loading cancelled.")

print(ans)





