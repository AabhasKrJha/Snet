## ABOUT THE WEBAPP

This is a minimalistic blogging webapp.
It uses an SQLite database and its not hosted on any platform. However it can run on a local machine with python 3.6 or above installed.

## INSTALLATION

Just clone the repo.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install flask.
```bash
pip install flask
```
This will install all the requirements for the project to run successfully. This may take some seconds.

## FEATURES OF THE WEBAPP

This webapp includes the following features:-
- Login/logout and signup
- Viewing profile of other people
- Following users
- Editing your own profiles
- Viewing your own and other users following, followers and posts
- Writing posts

## WHAT THE WEBAPP DOESN'T INCLUDE

The webapp doesn't include the following features:-
- User feed as in regular social media websites
- Sending follow requests. One may directly follow another user without sending any requests.
- Unfollowing users or removing your own followers
- Personal Messaging and thus blocking users
- A WYSIWYG editor for writing posts
- Profile pictures. The DP will be blue if you set your gender as Male while signing up and pink if  you send the gender to female. 

## RUN THE PROJECT

To see the project running, navigate to the file cloned to your local machine and open the file "main.py" and run it.
Now open your web browser and in the address bar type "localhost:5000" and hit the enter button to see the project running.

## SPECIAL INSTRUCTIONS

Make sure to not use special symbols except in the username else it may create problems.

To search for users just type "localhost:5000/profile/username-of-the-user". This will take you to the user's profile page if the user exists. Here you can follow the user and see the user's posts, following and followers.
To see the following, followers or posts just click on the text "following" , "followers" or "posts".

To create/write posts go to localhost:5000 and click on the plus button. Write the post and click on the "post" button.
