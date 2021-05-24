from flask import Flask, render_template, redirect, url_for, request
from ast import literal_eval
import configparser
import requests
import json
import scraping

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('./datas.ini')
info = config['APIKEY']
info2 = config['PROFILES']

@app.route('/')
def hello_world():
    apikey = info['REST_API_KEY']
    uri = info['REDIRECT_URI']
    return render_template('index.html', REST_API_KEY=apikey, REDIRECT_URI=uri)

@app.route('/oauth')
def oauth():
    code = request.args.get('code')
    token = getAccessToken(str(code))
    profiles = getProfileData(token)
    sendTextmsg()
    return '<br/> response user data =' + str(profiles)

def getAccessToken(code):
    access_url = "https://kauth.kakao.com/oauth/token"  # post
    params = {
        "grant_type": "authorization_code",
        "client_id": info['REST_API_KEY'],
        "redirect_uri": info['REDIRECT_URI'],
        "code": code,
    }
    response = requests.post(access_url, params)
    user_datas = json.loads((response.text.encode('utf-8')))

    config['PROFILES'] = {}
    config['PROFILES']['USER_DATAS'] = str(user_datas)

    with open('datas.ini', 'w') as configfile:
        config.write(configfile)

    return user_datas

def getProfileData(user_datas):
    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {"Authorization": f"Bearer {user_datas['access_token']}"}
    response = requests.get(url, headers=headers)

    profile_datas = response.json()
    return profile_datas

def setTextmsg():
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    s = scraping.Scraping()
    today_temper, compare_before, fine_dust, ultra_fine_dust = s.get_text()

    main_text = f'현재 기온은 {today_temper}이며 {compare_before}입니다.'
    sub_text = f'현재 미세먼지는 {fine_dust}이며 초미세먼지는 {ultra_fine_dust}입니다.'

    text_obj = {
        'object_type': 'text',
        'text': main_text + sub_text,
        'link': {
            'web_url': 'https://weather.naver.com/today',
            'mobile_web_url': 'https://m.weather.naver.com/today'
        },
        'button_title': '더 자세히 보고싶다면?'
    }
    return url, text_obj

def sendTextmsg():
    user_datas = literal_eval(info2['USER_DATAS'])
    url, full_text = setTextmsg()
    headers = {
        "Authorization": f"Bearer {user_datas['access_token']}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    params = 'template_object=' + str(json.dumps(full_text))
    print(params)
    response = requests.post(url, params, headers=headers)
    print(response, response.text)

if __name__ == '__main__':
    app.run()
