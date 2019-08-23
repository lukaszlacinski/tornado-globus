import urllib.parse as urllib_parse
from tornado import escape
from tornado.auth import OAuth2Mixin


class GlobusOAuth2Mixin(OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://auth.globus.org/v2/oauth2/authorize"
    _OAUTH_ACCESS_TOKEN_URL = "https://auth.globus.org/v2/oauth2/token"
    _OAUTH_USERINFO_URL = "https://auth.globus.org/v2/oauth2/userinfo"
    _OAUTH_SETTINGS_KEY = "globus_oauth"

    async def get_tokens(self, redirect_uri, code):
        http = self.get_auth_http_client()
        body = urllib_parse.urlencode({
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": self.settings[self._OAUTH_SETTINGS_KEY]["key"],
            "client_secret": self.settings[self._OAUTH_SETTINGS_KEY]["secret"],
            "grant_type": "authorization_code"
        })
        response = await http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
                         method="POST",
                         headers={"Content-Type": "application/x-www-form-urlencoded"},
                         body=body)
        return escape.json_decode(response.body)

    def get_user_info(self, access_token):
        return self.oauth2_request(self._OAUTH_USERINFO_URL,
                                   access_token=access_token)

    async def oauth2_request(self, url, access_token=None, post_args=None, *args):
        headers = {}
        if access_token:
            headers = {"Authorization": "Bearer " + access_token}
        if args:
            url += "?" + urllib_parse.urlencode(args)
        http = self.get_auth_http_client()
        if post_args is not None:
            response = await http.fetch(url, method="POST", headers=headers, body=urllib_parse.urlencode(post_args))
        else:
            response = await http.fetch(url, headers=headers)
        return escape.json_decode(response.body)