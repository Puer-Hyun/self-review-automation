# 네이버 부스트코스 셀프리뷰 과정 자동화

네이버 부스트코스의 셀프리뷰 5~7 과정을 자동화하여 엑셀에 저장하는 Python 스크립트입니다. 이 스크립트는 셀프리뷰 작성과정을 효율적으로 관리하도록 돕습니다.

## 시작하기
이 프로젝트를 로컬 컴퓨터에 설치하고 실행하는 방법을 아래에서 설명합니다.

### 필수 요구사항
- Python 3.6 이상
- Poetry (패키지 및 환경 관리)

### 레포지토리 클론
```bash
git clone https://github.com/Puer-Hyun/self-review-automation.git
cd self-review-automation
```

### 가상환경 설정 및 의존성 설치
Poetry를 사용하여 가상환경을 생성하고 필요한 패키지를 설치합니다.
```bash
poetry init --no-interaction  # 기본 설정으로 가상환경 초기화
poetry install                # 의존성 패키지 설치
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
poetry run python main.py 셀프리뷰url 본인수강생시작번호 본인수강생끝번호 셀프리뷰번호

poetry run python main.py https://www.boostcourse.org/boostclass-aibasic-02-202404/lecture/1536640?isDesc=false 2039 2080 5
```
Poetry shell 명령어를 통해 가상환경을 실행시킨 뒤 실행하셔도 괜찮습니다.

```bash
poetry shell
python main.py 셀프리뷰url 본인수강생시작번호 본인수강생끝번호 셀프리뷰번호
```

## 기능
이 스크립트는 다음과 같은 기능을 제공합니다:
- 구글 자동로그인 후 네이버 부스트클래스 자동로그인
- 셀프리뷰 과정의 진행 상태 확인
- 데이터 백업 및 복원 기능

## 기여하기
이 프로젝트에 기여하고 싶으시다면, Pull Request나 Issue를 통해 참여할 수 있습니다.