import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import schedule

# 상태 변수
job_executed = False

def create_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)

def fetch_server_time():
    driver = create_driver()
    driver.get('https://time.navyism.com/?host=www.hi-sns.or.kr')

    try:
        time_element = driver.find_element(By.CSS_SELECTOR, '#time_area')
        server_time = time_element.text.strip()
        print("서버 시간:", server_time)
        return server_time
    except Exception as e:
        print("시간 정보를 찾을 수 없습니다.", e)
        return None
    finally:
        driver.quit()

def move_to_site(url):
    driver = create_driver()
    driver.get(url)
    print("사이트로 이동했습니다:", url)

def job():
    global job_executed
    if job_executed:
        return

    server_time = fetch_server_time()
    if server_time:
        try:
            server_time_dt = datetime.strptime(server_time, "%Y년 %m월 %d일 %H시 %M분 %S초")
            target_time_dt = datetime(2024, 8, 27, 12, 5, 0)

            # 시와 분만 비교
            if server_time_dt.hour == target_time_dt.hour and server_time_dt.minute == target_time_dt.minute:
                move_to_site('https://google.com')
                job_executed = True
        except ValueError as e:
            print("시간 형식이 잘못되었습니다.", e)

schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(2)
