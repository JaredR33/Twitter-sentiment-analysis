#libraries
import pymysql
import configparser

config = configparser.ConfigParser()
config.read('gpt3app/config.ini')


db = pymysql.connect(host = config['seandatabase']['host'],
                     user = config['seandatabase']['username'],
                     password = config['seandatabase']['password'],
                     port = int(config['seandatabase']['port']),
                     cursorclass = pymysql.cursors.DictCursor)

cursor = db.cursor()

#Create database
create_db = '''CREATE DATABASE respuestas_GPT'''
cursor.execute(create_db)
cursor.connection.commit()

#Select database and create table
use_db = ''' USE respuestas_GPT'''
cursor.execute(use_db)

create_table_users= '''
CREATE TABLE users (
    author_id INTEGER PRIMARY KEY
)
'''

create_table_tweets = '''
CREATE TABLE tweets (
  id INT,
  text TEXT,
  created_at DATETIME,
  impression_count INT,
  like_count INT,
  quote_count INT,
  reply_count INT,
  retweet_count INT,
  author_id INT,
  primary key (id),
  FOREIGN KEY (author_id) REFERENCES users(author_id)
  )
'''

cursor.execute(create_table_users)
cursor.execute(create_table_tweets)
db.commit()
db.close()