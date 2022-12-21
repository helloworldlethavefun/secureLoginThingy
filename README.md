# My Drive

This is a clone of google drive that can be self hosted.
Written in python and uses login system as well.

## A little bit about it

This is a flask application that utilizes flask login for the login system, flask mail
for the password resetting and flaskwtf for the forms used on the webpages.
Everything is stored in a sqlite3 database including the files and all passwords
are hashed on entry so they are not stored in clear text. The files are mostly seperate 
to make it easier to work on individual parts but the bulk of it is handled in app.py.

## Requirements

- flask
- flask_login
- flask_mail
- argon2
- pyjwt
