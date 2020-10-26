# imports below--------------------------------------------------------

import sqlite3
import platform
import os
from datetime import date

# https://www.sqlitetutorial.net/sqlite-python/insert/


# general database operations below--------------------------------------


def create_connection(db_file):  # connectiong to that database
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        return 'error'


def create_table(db_file, create_table_sql):  # creting tables in database
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.close()

# handling signup and login below--------------------------------------------------


# ading user(signing up/ registeing/ creating accoonts)
def add_user(db_file, email, name, username, gender, password, create_table_sql):
    tablename = 'users'
    sql = ''' INSERT INTO {tablename}(email,name,username,gender,password)
              VALUES(?,?,?,?,?)'''.format(tablename=tablename)
    values = (email, name, username, gender, password,)
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, values)
        except:
            create_table(db_file, create_table_sql)
            cur.execute(sql, values)
        conn.commit()


# finding a user in in the users database for verifying login credentials
def find_user(db_file, email):
    tablename = 'users'
    sql = 'select * from {tablename} where email=?'.format(tablename=tablename)
    value = (email,)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql, value)

    row = cur.fetchone()

    if row == None:
        return False
    else:
        return list(row)

    conn.close()


def find_username(db_file, username):
    tablename = 'users'
    sql = f'select * from {tablename} where username=?'
    value = (username,)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql, value)

    row = cur.fetchone()
    conn.close()

    if row == None:
        return False
    else:
        return list(row)


# changing passwords


def change_pwd(db_file, email, new_pwd):

    conn = create_connection(db_file)

    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set password = ? where email = ?'.format(
            tablename=tablename)
        values = (new_pwd, email)

        cur.execute(sql, values)
        conn.commit()


# adding theme
def update_theme(db_file, email, theme):
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set theme = ? where email = ?'.format(
            tablename=tablename)
        values = (theme, email)

        cur.execute(sql, values)
        conn.commit()


def update_bio(db_file, email, bio):
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set bio = ? where email = ?'.format(
            tablename=tablename)
        values = (bio, email)

        cur.execute(sql, values)
        conn.commit()


def update_privacy(db_file, email, privacy):
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set privacy = ? where email = ?'.format(
            tablename=tablename)
        values = (privacy, email)

        cur.execute(sql, values)
        conn.commit()


def update_following(db_file, email):
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set following=following+1 where email=?'.format(
            tablename=tablename)
        values = (email,)

        cur.execute(sql, values)
        conn.commit()


def update_followers(db_file, username):
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set followers=followers+1 where username=?'.format(
            tablename=tablename)
        values = (username,)

        cur.execute(sql, values)
        conn.commit()


def update_followers_table(db_file, username, follower):
    conn = create_connection(db_file)

    with conn as conn:
        cur = conn.cursor()

        tablename = f'{username}followers'

        sql = ''' INSERT INTO {tablename}(username)
              VALUES(?)'''.format(tablename=tablename)
        values = (follower,)

        cur.execute(sql, values)
        conn.commit()


def follow(db_file, user, username):
    conn = create_connection(db_file)
    tablename = f'{user}following'
    with conn as conn:
        sql = ''' INSERT INTO {tablename}(username)
              VALUES(?)'''.format(tablename=tablename)
        value = (username,)

        cur = conn.cursor()
        cur.execute(sql, value)

        conn.commit()


def get_followers(db_file, username):
    tablename = f'{username}followers'
    sql = 'select username from {tablename}'.format(
        tablename=tablename)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql)

    row = cur.fetchall()

    followers = []

    if row == None:
        return False
    else:
        for i in row:
            for j in i:
                followers.append(j)

    conn.close()

    return followers


def get_following(db_file, username):
    tablename = f'{username}following'
    sql = 'select username from {tablename}'.format(
        tablename=tablename)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql)

    row = cur.fetchall()

    following = []

    if row == None:
        return False
    else:
        for i in row:
            for j in i:
                following.append(j)

    conn.close()

    return following


def post(db_file, username, post):
    conn = create_connection(db_file)
    tablename = f'{username}posts'

    with conn as conn:
        cur = conn.cursor()

        sql = ''' INSERT INTO {tablename}(post,date)
              VALUES(?,?)'''.format(tablename=tablename)
        todays_date = date.today()
        values = (post, todays_date)
        cur.execute(sql, values)

        tablename = 'users'
        sql = 'update {tablename} set posts=posts+1 where username = ?'.format(
            tablename=tablename)
        values = (username,)
        cur.execute(sql, values)

        conn.commit()


def get_posts(db_file, username):
    tablename = f'{username}posts'

    sql = 'select post from {tablename}'.format(
        tablename=tablename)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()

    posts = []
    if row == None:
        return False
    else:
        for i in row:
            for j in i:
                posts.append(j)

    sql = 'select date from {tablename}'.format(
        tablename=tablename)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()

    dates = []
    if row == None:
        return False
    else:
        for i in row:
            for j in i:
                dates.append(j)

    conn.close()

    posts_dates = {posts[i]: dates[i] for i in range(len(posts))}

    return (posts_dates)
