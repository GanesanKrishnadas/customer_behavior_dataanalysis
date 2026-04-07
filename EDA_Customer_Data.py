

# Customer Behavior Data EDA

# Step 1: Import Libraries

import pandas as pd


df = pd.read_csv("C:\\Users\\krish\\Downloads\\customer_shopping_behavior.csv")
print(df.columns.tolist())
print(df.dtypes)
print(df.head() )# top five rows - how data looks
print(df.info())
print(df.describe())  

print(df.describe(include='all'))

print(df.isnull().sum())

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
# 4. Now rename
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

# 5. Print columns to confirm
for col in df.columns:
    print(col)



labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

# Preview the first 10 rows
print(df[['age', 'age_group']].head(10))
# craete column purchase_frequency_days
frequency_mapping ={
    'Fortnightly': 14,
    'Weekly': 4,
    'Monthly':90,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months':90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

print(df[['discount_applied','promo_code_used']].head(10))


print((df['discount_applied'] == df['promo_code_used']).all())

df = df.drop('promo_code_used', axis=1)

print(df.columns)
#########################################################################################################
# PostgreSQL  

from sqlalchemy import create_engine
from urllib.parse import quote_plus


# step 1: connect to postgreSQL
username ="#########"  
password = quote_plus("#########")
host= "localhost"
port = "5432"
database = "customer_behavior" #  created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

 
#Step 2: Load DataFrame into PostgreSQL

table_name ="customer" # choose any table name
df.to_sql(table_name,engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}',")