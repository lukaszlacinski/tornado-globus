# tornado-globus
Globus Authentication Handler for Tornado Web Framework

## Install tornado-globus

Create Python 3.x virtual environment and install Tornado
```
$ python --version
Python 3.7.15
$ python -mvenv  venv
$ . venv/bin/activate
$ pip install tornado
```
Download tornado-globus
```
(venv)$ git clone git@github.com:lukaszlacinski/tornado-globus.git
(venv)$ cd tornado-globus
```
## Register a client

All OAuth2 clients need to register with Globus Auth to get a client id and secret. 
To register your client, go to `https://developers.globus.org/`, 
click 'Register your app with Globus', add a new project and add a new app in the project. 
Enter a name of your app you want to be shown to users when they are asked for a consent 
when redirected to Globus Auth for authentication. Enter the redirect URI: 
`https://example.com/auth/globus/`. Click 'Create App'. Click 'Generate New Client Secret' 
and copy Client ID and a generated secret to settings in `app.py`.

## Set up HTTPS reverse proxy
Set up Apache, nginx or another HTTPS server as a reverse proxy to pass all requests to 
`https://example.com/` to localhost:8888 where the app is going to listen at.

## Start the web app
```
(venv)$ python -m tornado.autoreload app.py
```
Open `https://example.com` in a web browser. If you do not own `example.com` domain, you may need to add:
```
127.0.0.1 example.com
```
to your `/etc/hosts`.
