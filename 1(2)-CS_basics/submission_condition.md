[1회차] CS 기초 과제

발제자: 김아연

기한
과제 마감: 7월 13일 월요일 23시 59분까지
지각 제출: 7월 14일 23시 59분까지

Intro
이번 과제는 크게 두 단계로 구성됩니다.
1. WSL 접속하기
2. Shell script 작성
Shell script는 Python 과제에서 만든 submission/ 폴더 안의 .py 파일들을 자동 실행
+ 결과 저장 + 타입체크 로그 저장까지 한 번에 수행하는 것을 목표로

과제 명세1. WSL 접속하기
WSL에 접속한 후 터미널 화면을 캡처해 주세요.
Windows: VSCode로 WSL에 접속한 화면을 캡처 후 terminal.png 로 저장
Mac: 기본 터미널 화면을 캡처 후 terminal.png 로 저장
2. Shell Script 작성
Python 과제의 submission 폴더 파일들을 shell script로 실행합니다.
.sh 파일은 제공될 예정이며, ## TODO 라고 표시된 부분만 채워 주세요.
## 건드리지 마세요! 라고 표시된 라인은 수정하지 않아야 합니다.
사전 준비: Python 과제에서 생성한 submission/ 폴더를 이 폴더 1(2)-CS_basics/ 안에 복
사해주세요!

Shell Script 기능 요구사항

[1회차] CS 기초 과제 1

작성한 script.sh 는 아래 기능을 수행해야 합니다.

1. Conda 가상환경 실행
Miniconda가 없는 환경에서도 돌아가야 합니다.
Miniconda가 설치되어 있지 않다면, 설치 과정까지 스크립트에 포함해야 합니다.
2. submission 폴더의 파일 실행
실행 대상: submission/ 폴더 안의 Python 파일들
입력: input/ 디렉토리의 {문제번호}_input 파일을 입력으로 사용
출력: output/ 디렉토리에 {문제번호}_output 파일로 저장
3. mypy test 수행
submission/ 폴더의 Python 파일들에 대해 mypy 테스트를 수행
실행 결과는 자동으로 mypy_log.txt 에 저장되어야 합니다
4. conda.yml 저장
현재 가상환경 정보를 conda.yml 파일러 저장

즉, 채점 시 script.sh 가 실행될 디렉토리 구조는 다음과 같습니다.

1(2)-CS_basics/
├── input/
│ ├── 1260_input
│ ├── 2164_input
│ ├── 11866_input
│ ├── 1629_input
│ ├── 10830_input
│ ├── 3080_input
│ ├── 5670_input
│ ├── 2243_input
│ ├── 3653_input
│ └── 17408_input
│
├── output/ ← output이 저장될 디렉토리
│
├── submission/
│ ├── 1_1260.py
│ ├── 2_2164.py
│ ├── 2_11866.py
│ ├── 3_1629.py

[1회차] CS 기초 과제 2

│ ├── 3_10830.py
│ ├── 4_3080.py
│ ├── 4_5670.py
│ ├── 5_2243.py
│ ├── 5_3653.py
│ └── 5_17408.py
│
└── script.sh

제출 방법
과제 제출용 GitHub 레포지터리에 아래 구조로 제출해 주세요.

YBIGTA_newbie_assignment/
├── 1(1)-Python/
│
└── 1(2)-CS_basics/
├── terminal.png
├── script.sh
├── mypy_log.txt
└── conda.yml

채점 기준
아래 다섯 조건을 모두 만족하면 통과입니다.
터미널 캡처 파일 terminal.png 가 있습니다.
가상환경이 정상적으로 activate 됩니다.
{문제번호}_output 파일이 정답과 일치합니다.
mypy 테스트를 통과합니다.
mypy_log.txt 와 conda.yml 이 자동 저장됩니다.
위 조건 중 하나라도 만족하지 않으면 과제 미흡으로 처리됩니다.
폴더명 및 파일명은 반드시 제공된 가이드라인을 따라 주세요.
첫 과제 제출인 만큼 꼼꼼히 확인 부탁드립니다.