# 네이버 부스트코스 리뷰 과정 자동화

네이버 부스트코스의 셀프리뷰 5~7 과정을 자동화하여 엑셀에 저장하는 Python 스크립트입니다. 이 스크립트는 셀프리뷰 작성과정을 효율적으로 관리하도록 돕습니다.

## 시작하기
이 프로젝트를 로컬 컴퓨터에 설치하고 실행하는 방법을 아래에서 설명합니다.

### 레포지토리 클론
```bash
git clone https://github.com/Puer-Hyun/self-review-automation.git
cd self-review-automation
```

### 가상환경 설정 및 의존성 설치
Poetry를 사용하여 가상환경을 생성하고 필요한 패키지를 설치합니다.
```bash
poetry shell
poetry install
chmod +x self_review.sh
chmod +x code_review.sh
```

### 구글 환경변수 세팅
스크립트가 구글 계정에 접근할 수 있도록 환경 변수를 설정합니다.
```bash
export GOOGLE_ID='YOUR_EMAIL_ADDRESS'
export GOOGLE_PW='YOUR_EMAIL_PASSWORD'
```
환경 변수를 영구적으로 설정하고 싶다면, `.bashrc` 또는 `.zshrc` 파일에 위 명령어를 추가하세요.

### 스크립트 실행 예시
모든 설정이 완료되었으면, 다음 명령어로 스크립트를 실행합니다.

```bash
./self_review.sh url start end self_review_number
```

```bash
poetry shell
./self_review.sh 'https://www.boostcourse.org/boostclass-aibasic-02-202404/lecture/1536640?isDesc=false' 2039 2100 5
./code_review.sh 'https://www.boostcourse.org/boostclass-aibasic-02-202404/project/522/content/436?isDesc=false#review' '박성현코치'
```

### 프로그램 사용법
- chrome driver가 자동으로 설치됩니다.
#### Self Review
- 위의 과정대로 잘 진행했다면, gradio 앱이 실행될 것이고 (Streamlit과 비슷) 이를 화면에 띄워두셔야 합니다.
- 자동으로 구글 로그인이 진행됩니다. 휴대폰에 '본인인증' 과정이 포함되므로, 구글에 로그인이 잘 되는지 확인까지는 해주시면 좋습니다.
- 스크립트 실행 후, Terminal 창에 반복적인 로그가 발생한다면, Gradio 창에서 Load Button을 눌러주시면 됩니다.
    - 해당 수강생분의 모달창이 등장할 것입니다. 우측에 의견을 적어서 Submit 해주시면 됩니다. (반복)

## 기능
이 스크립트는 다음과 같은 기능을 제공합니다:
- 구글 자동로그인 후 네이버 부스트클래스 자동로그인
- 셀프리뷰 과정의 진행 상태 확인
- 구글 시트에 옮겨적을 내용 csv 파일로 작성

#### Code Review
- 터미널창에서 Y를 누를 때까지 종료되지 않습니다.
- '진행중'이신 수강생 분들에 대한 새 탭들이 생성됩니다. 리뷰를 진행하신 뒤 결과 공개를 하시고 터미널창에 'Y' 또는 'y'를 입력하시면 프로세스가 종료됩니다.

## 기여하기
이 프로젝트에 기여하고 싶으시다면, Pull Request나 Issue를 통해 참여할 수 있습니다.