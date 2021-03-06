# tornado-globus
Globus Authentication Handler for Tornado Web Framework and an example web app showing how to use the handler.

## Install tornado-globus

Create Python 3.x virtual environment and install Tornado
```
$ python --version
Python 3.7.15
$ python -mvenv  venv
$ . venv/bin/activate
$ pip install tornado
```
Download the tornado-globus sample app
```
(venv)$ git clone git@github.com:lukaszlacinski/tornado-globus.git
(venv)$ cd tornado-globus
```
If you still use Tornado v5.x, go to `tornado_v5` directory.

## Register a client

All OAuth2 clients need to register with Globus Auth to get a client id and secret. 
To register your client, go to `https://developers.globus.org/`, 
click 'Register your app with Globus', add a new project and add a new app in the project. 
Enter the name of your app you want to be shown to users when they are asked for a consent 
when redirected to Globus Auth for authentication. Enter the redirect URI: 
`https://example.com/auth/globus/`. Click 'Create App', click 'Generate New Client Secret' 
and copy Client ID and the generated secret to `settings` in `app.py`.

## Set up HTTPS reverse proxy

Set up Apache, nginx or another HTTPS server as a reverse proxy to pass all requests to 
`https://example.com/` to localhost:8888 where the app will be listening on.

For example, on Ubuntu, add the following lines to /etc/apache2/sites-available/default-ssl.conf in `<VirtualHost _default_:443>`
```
        ProxyPass / http://127.0.0.1:8888/
        ProxyPassReverse / http://127.0.0.1:8888/
```
Restart Apache.

## Start the web app

```
(venv)$ python -m tornado.autoreload app.py
```
and open `https://example.com/` in a web browser. If you do not own `example.com` domain, you may need to add:
```
127.0.0.1 example.com
```
to your `/etc/hosts`.
