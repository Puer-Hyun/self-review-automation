import os
import time
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import argparse
import re  # 정규 표현식 모듈 추가
import pandas as pd
import json


# 학생 정보와 의견을 저장할 JSON 파일 이름
DATA_FILE = "student_data.json"


def get_user_opinion(html_content, student_info, self_review_number):
    """
    FastAPI 서버에 HTML과 학생 정보를 전달하고 Gradio이 의견을 제출할 때까지 대기합니다.
    """
    review_folder = f"self_review_{self_review_number}"
    os.makedirs(review_folder, exist_ok=True)

    data_file = os.path.join(review_folder, "student_data.json")

    print(f"Sending HTML content: {html_content}")
    print(f"Sending student info: {student_info}")

    # JSON 데이터를 저장합니다.
    data = {"modal_html": html_content, "student_info": student_info}
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print("Data saved successfully in:", data_file)

    # Gradio에서 의견을 제출할 때까지 대기합니다.
    while True:
        print(f"Waiting for user opinion for {student_info}...")
        opinion = check_opinion(student_info, self_review_number)
        if opinion:
            print(f"Received opinion: {opinion}")
            return opinion


def check_opinion(student_info, self_review_number):
    """
    해당 학생의 의견을 JSON 파일에서 가져옵니다.
    """
    review_folder = f"self_review_{self_review_number}"
    file_path = os.path.join(review_folder, f"{student_info}_opinion.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("opinion")
    return None


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


def find_last_page_number(driver):
    current_page = 1
    last_first_item_text = None
    while True:
        try:
            first_item = driver.find_element(
                By.CSS_SELECTOR,
                "#taskSubmit > table > tbody > tr:nth-child(1) > td.title > div",
            )
            first_item_text = first_item.text
            if first_item_text == last_first_item_text:
                print("No more new pages.")
                break
            last_first_item_text = first_item_text
            next_button = driver.find_element(
                By.CSS_SELECTOR, "#taskSubmit > nav > div > a.next"
            )
            if not next_button.is_enabled():
                break
            next_button.click()
            time.sleep(1)  # wait for the page to load
            current_page += 1
        except NoSuchElementException:
            break
    return current_page - 1


def check_and_write_opinion(
    driver, row_index, student_info: str, self_review_number: int
):
    # 해당 학생 정보에 대한 버튼 클릭하여 모달 창 띄우기
    selector = f"#taskSubmit > table > tbody > tr:nth-child({row_index + 1}) > td:nth-child(4) > button"
    opinion_button = driver.find_element(By.CSS_SELECTOR, selector)

    # 스크롤을 통해 버튼을 가시화
    driver.execute_script("arguments[0].scrollIntoView(true);", opinion_button)
    time.sleep(1)  # 스크롤 후 잠시 대기

    opinion_button.click()
    time.sleep(2)  # 모달 창이 뜰 시간을 기다림

    # 모달 창의 HTML을 가져옴
    modal_html = driver.find_element(
        By.CSS_SELECTOR,
        "#taskSubmit > div.modal_wrap.eval_task._warp_assignment_eval > div > div.modal_container > div",
    ).get_attribute("outerHTML")

    # 모달 창 닫기 버튼 클릭
    close_modal_button = driver.find_element(
        By.CSS_SELECTOR,
        "#taskSubmit > div.modal_wrap.eval_task._warp_assignment_eval > div > div.modal_container > div > button",
    )
    close_modal_button.click()
    time.sleep(1)

    # FastAPI 서버를 통해 Gradio 인터페이스 실행
    opinion = get_user_opinion(modal_html, student_info, self_review_number)

    return opinion


def extract_students_data(
    driver, start, end, last_page_number, processed_names, self_review_number
):
    result = []

    for page in range(1, last_page_number + 1):
        rows = driver.find_elements(By.CSS_SELECTOR, "#taskSubmit > table > tbody > tr")
        for index, row in enumerate(rows):
            try:
                student_info = row.find_element(By.CSS_SELECTOR, "td.title > div").text
                student_number_match = re.search(r"\d+", student_info)
                if student_number_match:
                    student_number = int(student_number_match.group(0))

                    if start <= student_number <= end:
                        student_name = student_info.split(" ")[0][6:]
                        print(f"Extracted student name: {student_name}")

                        if student_name in processed_names:
                            print(f"Already processed: {student_name}")
                            continue  # 이미 처리된 학생은 건너뜀

                        student_details = row.find_element(
                            By.CSS_SELECTOR, "td:nth-child(2)"
                        ).text
                        print(f"Found student details: {student_details}")

                        opinion = check_and_write_opinion(
                            driver, index, student_info, self_review_number
                        )
                        print(f"Retrieved opinion: {opinion}")

                        student_data = {
                            "student_info": student_info,
                            "student_details": student_details,
                            "opinion": opinion,
                        }
                        result.append(student_data)
                        print(
                            f"Processed Student Info: {student_info}, Details: {student_details}, Opinion: {opinion}"
                        )
            except Exception as e:
                print(f"Error processing row {index + 1} on page {page}: {e}")

        if page < last_page_number:
            try:
                next_button = driver.find_element(
                    By.CSS_SELECTOR, "#taskSubmit > nav > div > a.next"
                )
                print(f"Clicking next button to go to page {page + 1}")
                next_button.click()
                time.sleep(1)  # 페이지 로드 기다림
            except Exception as e:
                print(f"Error clicking next button on page {page}: {e}")
                break

    print("Data extraction complete.")
    print(f"Extracted data: {result}")
    return result


def create_or_update_csv(
    filename, extracted_students_data, start, end, self_review_number
):
    print(f"Creating or updating {filename}.")
    print(f"Extracted data: {extracted_students_data}")
    print(f"Start: {start}, End: {end}, Self Review Number: {self_review_number}")

    review_column = f"셀프리뷰{self_review_number}"
    date_column = "제출일"
    opinion_column = "의견"

    # 초기 테이블 구조 설정
    # 데이터 타입을 명시적으로 지정
    columns = {
        "번호": int,
        "훈련생ID": str,
        "성함": str,
        date_column: str,
        review_column: str,
        opinion_column: str,
    }

    if not os.path.exists(filename):
        # 파일이 없으면 새로운 파일 생성
        df = pd.DataFrame(columns=columns.keys())
        df["번호"] = range(1, end - start + 2)  # 1부터 시작, end-start+1까지 번호 부여
        df["훈련생ID"] = [f"ca{num}" for num in range(start, end + 1)]
        df = df.astype(columns)  # 데이터 타입 적용
        df.to_csv(filename, index=False)
        print("New file created with initial columns.")
    else:
        # 파일이 있으면 기존 데이터 불러오기
        df = pd.read_csv(filename)
        df = df.astype(columns)  # 데이터 타입 적용

    # 새로운 데이터 업데이트
    new_data = pd.DataFrame(extracted_students_data)
    for index, row in new_data.iterrows():
        if "student_info" in row and "student_details" in row and "opinion" in row:
            student_id = re.search(r"ca\d+", row["student_info"]).group(0)
            # 성함과 제출일 업데이트
            df.loc[
                df["훈련생ID"] == student_id, ["성함", date_column, opinion_column]
            ] = [
                row["student_info"].split(" ")[0][6:],  # 성함 추출 부분 수정 필요
                row["student_details"],
                row["opinion"],
            ]
            print(f"Update for {student_id}")

    df.to_csv(filename, index=False)
    print(f"Updated {filename} with new data for {review_column} and {opinion_column}.")


def load_student_names(filename):
    try:
        df = pd.read_csv(filename)
        return set(df["성함"].dropna().unique())
    except FileNotFoundError:
        return set()


def main():
    parser = argparse.ArgumentParser(
        description="Log in to Google and navigate to a specified URL."
    )
    parser.add_argument("url", type=str, help="URL to navigate after login")
    parser.add_argument("start", type=int, help="본인 수강생 시작 번호")
    parser.add_argument("end", type=int, help="본인 수강생 마지막 번호")
    parser.add_argument("self_review_number", type=int, help="셀프리뷰 회차")
    args = parser.parse_args()

    filename = f"self_review_{args.self_review_number}/self_review_{args.self_review_number}.csv"
    processed_names = load_student_names(filename)

    with SB(uc=True) as driver:
        google_login(driver)
        login_boostclass(driver)
        move_to_url(driver, args.url)
        driver.find_element(
            By.XPATH, "/html/body/div[3]/div[1]/div[2]/section/header/div/div[1]/a[1]"
        ).click()
        driver.sleep(5)
        last_page_number = find_last_page_number(driver)
        driver.refresh()
        extracted_students_data = extract_students_data(
            driver,
            args.start,
            args.end,
            last_page_number,
            processed_names,
            args.self_review_number,
        )

        create_or_update_csv(
            filename,
            extracted_students_data,
            args.start,
            args.end,
            args.self_review_number,
        )
        driver.sleep(5)
        print("Done")


if __name__ == "__main__":
    main()
