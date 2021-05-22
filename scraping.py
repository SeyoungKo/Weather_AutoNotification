from selenium import webdriver
import re

class Scraping:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://weather.naver.com/today'
        self.driver.get(self.url)

    def get_text(self):
        driver = self.driver
        temperature = driver.find_element_by_css_selector('#content > div > div.card.card_today > div.today_weather > div.weather_area > strong').text
        temperature = re.findall('[0-9]', temperature)
        temperature = ''.join(temperature)
        degree = driver.find_element_by_css_selector('#content > div > div.card.card_today > div.today_weather > div.weather_area > strong > span.degree').text

        compare_before = driver.find_element_by_css_selector('#content > div > div.card.card_today > div.today_weather > div.weather_area > p').text
        fine_dust = driver.find_element_by_css_selector('#content > div > div.card.card_today > div.today_weather > ul > li:nth-child(1) > a > div > em').text
        ultra_fine_dust = driver.find_element_by_css_selector('#content > div > div.card.card_today > div.today_weather > ul > li:nth-child(2) > a > div > em').text

        driver.quit()
        return temperature + degree, compare_before, fine_dust, ultra_fine_dust


if __name__ == '__main__':
    s = Scraping()
    today_temper, compare_before, fine_dust, ultra_fine_dust = s.get_text()

    # print(f'현재 기온은 {today_temper}이며 {compare_before}입니다.')
    # print(f'현재 미세먼지는 {fine_dust}이며 초미세먼지는 {ultra_fine_dust}입니다.')