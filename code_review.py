import os
import time
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import argparse
import re  # 정규 표현식 모듈 추가
import pandas as pd
import json


def google_login(driver) -> None:
    """
    Log in to Google account.
    """
    driver.get(
        "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow"
    )
    driver.type("#identifierId", os.getenv("GOOGLE_ID"))
    driver.click("#identifierNext > div > button")
    driver.sleep(5)  # 3초간 대기

    driver.type(
        "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input",
        os.getenv("GOOGLE_PW"),
    )
    driver.click("#passwordNext > div > button")
    driver.sleep(30)  # 30초간 대기, 이 사이에 휴대폰 인증 해야함.
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button",
    ).click()


def login_boostclass(driver) -> None:
    """
    Open the given URL with the specified driver.
    """
    driver.get(r"https://www.boostcourse.org/login")
    time.sleep(3)  # Adjust sleep time as necessary
    # 구글로 로그인 클릭
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div[2]/div/section/div[1]/ul/li[3]/button"
    ).click()
    time.sleep(3)
    # 계정 클릭
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]",
    ).click()
    time.sleep(5)
    # boostcourse 연결 클릭
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button",
    ).click()
    time.sleep(5)


def move_to_url(driver, url: str) -> None:
    """
    Navigate to the specified URL.
    """
    driver.get(url)
    driver.sleep(10)  # Adjust sleep time as necessary


def click_coach_name(driver, coach_name: str) -> None:
    """
    Find the coach name and click it.
    """
    # Click the reviewer selection box first
    driver.find_element(
        By.CSS_SELECTOR,
        "#project_content > div > div > div > div:nth-child(3) > div.reviewer_selbox > div > div",
    ).click()
    driver.sleep(1)  # Optional: wait for the dropdown to appear

    # Find and click the coach name in the list
    ul_element = driver.find_element(
        By.CSS_SELECTOR,
        "#project_content > div > div > div > div:nth-child(3) > div.reviewer_selbox > div > div > div > ul",
    )
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    for li in li_elements:
        if coach_name in li.text:
            li.click()
            break

    driver.sleep(5)


def check_passed_student(driver) -> None:
    """
    Print the names of students who have passed.
    """
    ul_element = driver.find_element(
        By.CSS_SELECTOR,
        "#project_content > div > div > div > div:nth-child(3) > div.list_box > div.scroll_box > ul",
    )
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    passed_students = []
    for li in li_elements:
        if li.get_attribute("data-active") == "false":
            name = li.find_element(By.CSS_SELECTOR, "span.name_area").text
            passed_students.append(name)

    passed_students.sort()
    for student in passed_students:
        print(student)


def check_progress_student(driver, base_url: str) -> list:
    """
    Return a list of URLs of students who are in progress.
    """
    ul_element = driver.find_element(
        By.CSS_SELECTOR,
        "#project_content > div > div > div > div:nth-child(3) > div.list_box > div.scroll_box > ul",
    )
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    progress_student_urls = []
    for li in li_elements:
        if li.get_attribute("data-active") == "true":
            data_id = li.get_attribute("data-id")
            progress_url = f"{base_url}/{data_id}/overview"
            progress_student_urls.append(progress_url)

    return progress_student_urls


def open_new_windows(driver, urls: list) -> list:
    """
    Open each URL in a new window and return a list of window handles.
    """
    window_handles = []
    for url in urls:
        driver.open_new_window()  # 새 윈도우를 열기
        new_window_handle = driver.driver.window_handles[
            -1
        ]  # 새 윈도우의 핸들 가져오기
        window_handles.append(new_window_handle)  # 핸들 리스트에 추가
        driver.driver.switch_to.window(new_window_handle)  # 새 윈도우로 전환
        driver.get(url)  # URL로 이동
    time.sleep(10)  # 모든 탭이 로드될 때까지 대기
    return window_handles  # 모든 새 윈도우의 핸들을 반환


def main():
    parser = argparse.ArgumentParser(
        description="Log in to Google and navigate to a specified URL."
    )
    parser.add_argument("url", type=str, help="URL to navigate after login")
    parser.add_argument("coach_name", type=str, help="본인 코치 이름 (ex. 박성현코치)")
    args = parser.parse_args()

    with SB(uc=True) as driver:
        google_login(driver)
        login_boostclass(driver)
        move_to_url(driver, args.url)
        click_coach_name(driver, args.coach_name)

        # 이미 완료된 학생을 출력함.
        check_passed_student(driver)

        # 진행중인 학생들의 URL을 가져옴.
        base_url = args.url.split("#")[0] + "#review"
        progress_student_urls = check_progress_student(driver, base_url)

        # Open new tabs for each progress student URL
        open_new_windows(driver, progress_student_urls)

        # Wait for user input to terminate the process
        while True:
            user_input = input("프로세스를 종료하시겠습니까? (y/n): ").lower()
            if user_input == "y":
                break


if __name__ == "__main__":
    main()
