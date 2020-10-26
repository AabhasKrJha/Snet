# imports below----------------------------------------------------------------

from flask import Flask, render_template, request, redirect, session, flash  # import flask
from user_acc_db_operations import *  # user database operations
from EmailValidator import *  # email validator
import os
import platform
import hashlib  # hashlib for secure passcodes
import secrets

# app variabes below---------------------------------------------------------------

app = Flask(__name__)  # creating insance of 'Flask' Class
app.secret_key = secrets.token_hex()  # for form submission security

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

# creating path for db------------------------------------------------------------

if platform.system() in ['Darwin', 'Linux']:
    db_dir = '{cwd}/database'.format(cwd=os.getcwd())
    db_dir_path = r'{database}'.format(database=db_dir)
    users_db = r'{db_dir_path}{user}'.format(
        db_dir_path=db_dir_path, user='/users.db')


else:  # windows platform
    db_dir = '{cwd}\\database'.format(cwd=os.getcwd())
    db_dir_path = r'{database}'.format(database=db_dir)
    users_db = r'{db_dir_path}{user}'.format(
        db_dir_path=db_dir_path, user='\\users.db')

try:
    os.mkdir(db_dir_path)
except:
    pass

# the main app below---------------------------------------------------------------------


@app.route('/')  # landing page
@app.route('/login/')
@app.route('/login', methods=["GET", "POST"])  # login form
def main():
    if 'user' in session:
        return redirect('/profile')
    else:
        if request.method == 'POST':
            email = request.form['Email']
            password = request.form['Password']
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            try:
                email_details = find_user(users_db, email)
            except:
                # because there is no table forr users to find data
                flash("An error occured.")
                return redirect('/login')

            if check_mail(email):
                try:
                    user_data = find_user(users_db, email)
                    if not user_data:
                        flash("You aren't registered.")

                except:
                    flash("An error occured")
                    return redirect('/login')

                try:
                    email_username = email_details[3]
                except:
                    return redirect('/login')

                if user_data == False:
                    flash("You aren't registered.")
                else:
                    if user_data[5] == hashed_password:
                        session['user'] = email
                        session['username'] = email_username
                        flash('Login Successful')
                        return redirect('/profile')
                    else:
                        flash("Email & password don't match")

            else:
                flash('Invalid E-mail address')

    return render_template('first-view.html')


@app.route('/signup')
@app.route('/signup', methods=["GET", "POST"])  # register user form
def signup():

    if 'user' in session:
        return redirect('/profile')
    else:

        create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        name text NOT NULL,
                                        email text UNIQUE NOT NULL,
                                        username text UNIQUE NOT NULL,
                                        gender text NOT NULL,
                                        password text NOT NULL,
                                        DP blob,
                                        header_cover blob,
                                        bio text,
                                        theme text DEFAULT light,
                                        followers integer DEFAULT 0,
                                        following integer DEFAULT 0,
                                        posts integer DEFAULT 0,
                                        privacy text DEFAULT public
                                    ); """

        if request.method == 'POST':
            email = request.form['Email']
            name = request.form['FullName']
            username = request.form['Username']
            gender = request.form['gender']
            password = request.form['Password']
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            if check_mail(email):
                create_table(users_db, create_users_table)
                try:
                    add_user(users_db, email, name, username, gender,
                             hashed_password, create_users_table)
                except:  # if the user is alredy present due to email being a unique key
                    flash('Account already created')
                    return redirect('/login')
            else:
                flash('Invalid E-mail address')

            if find_user(users_db, email):
                session['user'] = email
                session['username'] = username
                return redirect('/profile')
            else:
                flash('Invalid credentials provided')

    return render_template('signup.html')


@app.route('/logout/')
@app.route('/logout')  # logout
def logout():
    try:
        session.pop('user')
        session.pop('username')
        return redirect("/login")
    except:
        return redirect('/login')


@app.route('/profile/')
@app.route('/profile', methods=['GET', 'POST'])  # profile page
def profile():
    if 'user' in session:
        user_email = session.get('user')
        user_info = find_user(users_db, user_email)
        user_name = user_info[1]
        user_gender = user_info[4]
        user_username = user_info[3]
        user_followers = user_info[10]
        user_following = user_info[11]
        user_posts = user_info[12]
        user_bio = user_info[8]

        return render_template('profile.html', name=user_name, gender=user_gender, bio=user_bio,
                               followers=user_followers, following=user_following, posts=user_posts,
                               session=session, logged_in_username=user_username, profile_editable=True, user_found=True)
    else:
        return redirect('/login')


@app.route('/profile/<username>/')
@app.route('/profile/<username>', methods=["GET", "POST"])
def show_profile(username):

    try:
        if find_username(users_db, username):
            username_info = find_username(users_db, username)
            user_name = username_info[1]
            user_gender = username_info[4]
            user_bio = username_info[8]
            user_followers = username_info[10]
            user_following = username_info[11]
            user_posts = username_info[12]

            if "user" in session:
                try:
                    if username in get_following(users_db, find_user(users_db, session['user'])[3]):
                        follow = True
                    else:
                        follow = False
                except:
                    follow = False

                if username == find_user(users_db, session['user'])[3]:
                    profile_editable = True
                    return render_template('profile.html', name=user_name, gender=user_gender, bio=user_bio,
                                           followers=user_followers, following=user_following, posts=user_posts,
                                           session=session, username=username, profile_editable=profile_editable, user_found=True,
                                           session_username=find_user(users_db, session['user'])[3], follow=follow)
                else:
                    profile_editable = False
                    return render_template('profile.html', name=user_name, gender=user_gender, bio=user_bio,
                                           followers=user_followers, following=user_following, posts=user_posts,
                                           session=session, username=username, profile_editable=profile_editable, user_found=True,
                                           session_username=find_user(users_db, session['user'])[3], follow=follow)
            else:
                profile_editable = False
                return render_template('profile.html', name=user_name, gender=user_gender, bio=user_bio,
                                       followers=user_followers, following=user_following, posts=user_posts,
                                       session=session, username=username, profile_editable=profile_editable, user_found=True, follow=False)
        else:
            return render_template('profile.html', user_found=False, username=username)

    except:
        return render_template('profile.html', user_found=False, username=username)


@app.route('/settings/')
@app.route('/settings', methods=['GET', 'POST'])  # edit profile page
def settings():
    if 'user' in session:

        if request.method == "POST":

            if 'settings' in request.form:

                """ this if statement ass there are 2 forms submitting to this route
                one is profile.html and the other in setting.html
                and the name settings is the name of the input field in profile.html"""
                return redirect('/settings')

            if 'follow-user' in request.form:

                username = request.form['follow-user']

                create_users_following_table = """ CREATE TABLE IF NOT EXISTS {user}following (
                                                        id integer PRIMARY KEY AUTOINCREMENT,
                                                        username text UNIQUE NOT NULL
                                                        ); """.format(user=find_user(users_db, session['user'])[3])

                create_users_follower_table = """ CREATE TABLE IF NOT EXISTS {user}followers (
                                                        id integer PRIMARY KEY AUTOINCREMENT,
                                                        username text UNIQUE NOT NULL
                                                        ); """.format(user=username)

                if 'user' in session:

                    try:
                        create_table(users_db, create_users_following_table)
                        create_table(users_db, create_users_follower_table)

                        follow(users_db, find_user(
                            users_db, session['user'])[3], username)

                        update_following(users_db, session['user'])
                        update_followers_table(users_db, username, find_user(
                            users_db, session['user'])[3])
                        update_followers(users_db, username)
                    except:
                        return redirect('/profile')

                flash(f'followed {username}')
                return redirect('/profile')

            else:
                try:
                    theme = request.form['theme']
                except:
                    flash('Please provide the theme.')

                try:
                    privacy = request.form['privacy']
                except:
                    flash('Please give privacy settings.')

                bio = request.form['bio']
                new_pwd = request.form['new-pwd']
                new_hashed_pwd = hashlib.md5(new_pwd.encode()).hexdigest()
                user_email = session.get('user')

                update_theme(users_db, user_email, theme)

                if bio:
                    update_bio(users_db, user_email, bio)

                if new_pwd:
                    change_pwd(users_db, session['user'], new_hashed_pwd)

                update_privacy(users_db, user_email, privacy)

                flash('profile updated')
                return redirect('/profile')

        return render_template('settings.html', session=session)

    else:
        return redirect('/')


@app.route('/profile/<username>/followers/')
@app.route('/profile/<username>/followers')
def followers(username):
    try:
        followers = get_followers(users_db, username)
        return render_template('view_follow.html', followers=followers)
    except sqlite3.OperationalError as e:
        error_message = e.args[0]
        if error_message.startswith("no such table"):
            if "user" in session:
                if username == find_user(users_db, session['user'])[3]:
                    flash('No followers')
                    return redirect('/profile')
                else:
                    flash('No followers')
                    return redirect(f'/profile/{username}')
            else:
                flash('No followers')
                return redirect(f'/profile/{username}')
        else:
            flash('No followers')
            return redirect('/profile')


@app.route('/profile/<username>/following/')
@app.route('/profile/<username>/following')
def following(username):
    try:
        following = get_following(users_db, username)
        return render_template('view_follow.html', following=following)
    except sqlite3.OperationalError as e:
        error_message = e.args[0]
        if error_message.startswith("no such table"):
            if "user" in session:
                if username == find_user(users_db, session['user'])[3]:
                    flash('Not following anyone')
                    return redirect('/profile')
                else:
                    flash('Not following anyone')
                    return redirect(f'/profile/{username}')
            else:
                flash('Not following anyone')
                return redirect(f'/profile/{username}')
        else:
            flash('Not following anyone')
            return redirect('/profile')


@app.route('/<username>/posts/')
@app.route('/<username>/posts')
def view_posts(username):
    try:
        posts_and_dates = get_posts(users_db, username)
        return render_template('posts.html', posts=posts_and_dates)
    except sqlite3.OperationalError as e:
        error_message = e.args[0]
        if error_message.startswith("no such table"):
            if "user" in session:
                if username == find_user(users_db, session['user'])[3]:
                    flash('No Posts.')
                    return redirect('/profile')
                else:
                    flash('No Posts.')
                    return redirect(f'/profile/{username}')
            else:
                flash('No Posts.')
                return redirect(f'/profile/{username}')
        else:
            flash('No Posts.')
            return redirect('/profile')


@app.route('/posts/')
@app.route('/posts', methods=['GET', 'POST'])
def posts():

    username = session['username']
    posts_table_sql = f""" CREATE TABLE IF NOT EXISTS {username}posts (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        post text  NOT NULL,
                                        date text NOT NULL
                                    ); """

    create_table(users_db, posts_table_sql)

    if request.method == "POST":
        if 'post' in request.form:
            POST = request.form['post']
            post(users_db, username, POST)
            flash('POSTED !')
            return redirect('/')


@app.route('/reset-password/')
@app.route('/reset-password', methods=['GET', 'POST'])
def forgot_pass():

    reset_pwd_table = """ CREATE TABLE IF NOT EXISTS reset_pwd_links (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        link text UNIQUE NOT NULL
                                    ); """

    create_table(users_db, reset_pwd_table)

    if request.method == "POST":

        if 'mail-confirm' in request.form:
            reset_email = request.form['Email']
            session['mail'] = reset_email

            if check_mail(reset_email):
                if find_user(users_db, reset_email):
                    return render_template('reset_password.html', email=reset_email)
                else:
                    flash('No such user found.')
            else:
                flash('Invalid Email entered')

        elif 'set-new-pass' in request.form:

            new_pwd = request.form['Password']
            new_hashed_password = hashlib.md5(new_pwd.encode()).hexdigest()
            change_pwd(users_db, session['mail'], new_hashed_password)
            session.pop('mail')
            flash('Password Changed')
            return redirect('/')

    return render_template('mail_check.html')


@app.route('/instructions')
def instructions():
    return render_template("instructions.html")


if __name__ == "__main__":
    app.run()
