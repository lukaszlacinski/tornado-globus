import tornado.ioloop
import tornado.web
import globus


class GlobusOAuth2LoginHandler(tornado.web.RequestHandler,
                               globus.GlobusOAuth2Mixin):
    async def get(self):
        if self.get_argument("code", False):
            tokens = await self.get_tokens(
                redirect_uri=self.settings["globus_oauth"]["redirect_uri"],
                code=self.get_argument("code"))
            user_info = await self.get_user_info(tokens["access_token"])
            # Save the user with e.g. set_secure_cookie
            self.set_secure_cookie("user_id", user_info["sub"])
            self.set_secure_cookie("username", user_info["preferred_username"])
            self.set_secure_cookie("email", user_info["email"])
            self.set_secure_cookie("name", user_info["name"])
            self.set_secure_cookie("organization", user_info["organization"])
            self.set_secure_cookie("access_token", tokens["access_token"])
            self.set_secure_cookie("refresh_token", tokens["refresh_token"])
            self.redirect("/")
        else:
            await self.authorize_redirect(
                redirect_uri=self.settings["globus_oauth"]["redirect_uri"],
                client_id=self.settings["globus_oauth"]["key"],
                scope=self.settings["globus_oauth"]["scope"],
                response_type="code",
                extra_params={"access_type": "offline"})


class LogoutHandler(tornado.web.RequestHandler):
    async def get(self):
        self.clear_cookie("user_id")
        self.redirect("/")


class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user_id")

    def get(self):
        self.render("../home.html",
                    user_id=self.current_user,
                    username=self.get_secure_cookie("username"),
                    email=self.get_secure_cookie("email"),
                    name=self.get_secure_cookie("name"),
                    organization=self.get_secure_cookie("organization"),
                    access_token=self.get_secure_cookie("access_token"),
                    refresh_token=self.get_secure_cookie("refresh_token"))


def make_app():
    settings = {
        "cookie_secret": "32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "xsrf_cookies": True,
        "globus_oauth": {
            "key": "<Globus_OAuth2_Client_Id>",
            "secret": "<Globus_OAuth2_Client_Secret>",
            "redirect_uri": "https://example.org/auth/globus",
            "scope": [
                "openid",
                "profile",
                "email",
                "urn:globus:auth:scope:transfer.api.globus.org:all"
            ]
        }
    }
    handlers = [
        (r"/", MainHandler),
        (r"/login", GlobusOAuth2LoginHandler),
        (r"/auth/globus", GlobusOAuth2LoginHandler),
        (r"/logout", LogoutHandler),
    ]
    return tornado.web.Application(handlers, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
