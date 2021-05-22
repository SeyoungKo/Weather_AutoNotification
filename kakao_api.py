import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('./datas.ini')
info = config['APIKEY']

class KakaoRestAPI:
    def __init__(self):
        self.apikey = info['REST_API_KEY']
        self.uri = info['REDIRECT_URI']
        self.oacode = info['OAUTH_CODE']

    def oauth_req(self):
        # 한번만 가능
        oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={self.apikey}&redirect_uri={self.uri}&response_type=code"
        response = requests.get(oauth_url)
        print(response.url)

        # access_url = "https://kauth.kakao.com/oauth/token"  # post
        # params = {
        #     "grant_type": "authorization_code",
        #     "client_id": self.apikey,
        #     "redirect_uri": self.uri,
        #     "code": self.oacode
        # }
        # response = requests.post(access_url, params)
        # print(response)


if __name__ == '__main__':
    k = KakaoRestAPI()
    k.oauth_req()
