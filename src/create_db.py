import pymysql
import cryptography
import pandas as pd
from sqlalchemy import create_engine

username = "admin"
password = "TheBridgeSchool"
host = "database-2.cvuovpb4vssk.us-east-2.rds.amazonaws.com" 
port = 3306

db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
)

# El objeto cursor es el que ejecutará las queries y devolverá los resultados

cursor = db.cursor()


# Creamos una BD. Tenemos una instancia de MySQL, pero no una BD
create_db = '''CREATE DATABASE tweets_TheBridge'''
cursor.execute(create_db)

# Para usar la BD  recien creada

cursor.connection.commit()
use_db = ''' USE tweets_TheBridge'''
cursor.execute(use_db)

# Create two normalized tables, tweets and users
create_table_users = '''
CREATE TABLE users (
    author_id INTEGER
)
'''
cursor.execute(create_table_users)

create_table = '''
CREATE TABLE tweets (
  author_id INT,
  created_at TEXT,
  id INT,
  text INT,
  impression_count INT,
  like_count INT,
  quote_count INT,
  reply_count INT,
  retweet_count INT
)

'''
cursor.execute(create_table)


#insert data

df = pd.read_csv('../data/tweets_23&23_@TheBridge.csv', index_col=0)
df_users = pd.DataFrame(df['author_id'])

# create sqlalchemy engine

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user = username, pw = password, host = host, db = 'tweets_TheBridge'))

# insertamos todo el dataframe en users
df_users.to_sql(name='users', con=engine, if_exists= 'append', index=False)

# df into tweets tables
df.to_sql(name='tweets', con=engine, if_exists= 'append', index=False)

db.commit()
# Cerrar conexión mysql
db.close()
# Cerrar conexión sqlalchuemy
engine.dispose()

