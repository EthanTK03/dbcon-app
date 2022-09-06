#Code connecting database to project

import sys
import random
import pymysql
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World'
        
# def dbase():
#     db = pymysql.connect(host='localhost', user='root', password='yeetus99', database='hangman')
#     db.autocommit(True)
#     sql = "select `Regions` from regions"
#     crsr = db.cursor()
#     crsr.execute(sql)



@app.route('/resetdb')
def reset():
    # Make sure you modify this connection string to connect to your database, and not mine.
    conn = pymysql.connect(host='localhost', user='root', password='yeetus99', database='session4d')
    conn.autocommit(True)
    crsr = conn.cursor()

    # Drop the tables if they already exist
    sql = 'DROP TABLE IF EXISTS `tracker`.`login`;'
    crsr.execute(sql)
    sql = 'DROP TABLE IF EXISTS `tracker`.`user`;'
    crsr.execute(sql)
    sql = 'CREATE TABLE `tracker`.`user` (`id` INT NOT NULL AUTO_INCREMENT,`login` VARCHAR(255) NULL, PRIMARY KEY (`id`));'
    crsr.execute(sql)
    sql = 'CREATE TABLE `tracker`.`login` (`id` INT NOT NULL AUTO_INCREMENT,`userid` INT NULL,`date` DATETIME, PRIMARY KEY (`id`), FOREIGN KEY (userid) REFERENCES `user`(id));'
    crsr.execute(sql)

    return 'Reset Successful'

# <user> allow us to put values in the web request, in this case, the user's login
@app.route('/login/<user>')
def login(user):
    conn = pymysql.connect(host='localhost', user='root', password='yeetus99', database='session4d')
    conn.autocommit(True)
    crsr = conn.cursor()

    # First, check if this user already exists
    sql = 'select id from user where login=\'' + user + '\''
    crsr.execute(sql)
    print('returned ' + str(crsr.rowcount) + ' rows')
    if crsr.rowcount == 0:
        print('adding ' + user)
        crsr.execute('insert into user (login) values (\'' + user + '\')')
        print('adding ' + str(crsr.rowcount) + ' user')
        print('re-executing ' + sql)
        crsr.execute(sql)
    res = crsr.fetchone()
    userid = res[0]
    # Now, add the login information
    # Note, CURRENT_TIMESTAMP is built into MySQL to get the current time
    sql = 'insert into login (userid, `date`) values (' + str(userid) +', CURRENT_TIMESTAMP)'
    crsr.execute(sql)

    conn.commit()

    # Finally, get the user's login count and the total login count
    sql = 'select count(*) as logins from login where userid=' + str(userid)
    print(sql)
    crsr.execute(sql)
    res = crsr.fetchone()
    usercount = res[0]
    sql = 'select count(*) as logins from login'
    crsr.execute(sql)
    res = crsr.fetchone()
    totalcount = res[0]

    return jsonify({'user': user, 'user count':usercount, 'total count':totalcount })
if __name__ == '__main__':
    app.run()