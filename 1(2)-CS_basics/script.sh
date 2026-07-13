#!/bin/bash

# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if command -v conda > /dev/null 2>&1; then
    echo "이미 미니콘다가 설치되어 있습니다. 설치를 건너뜁니다."
else
    # OS/아키텍처에 맞는 설치 파일 선택 (Mac / WSL(Linux) 모두 지원)
    if [[ "$(uname)" == "Darwin" ]]; then
        INSTALLER="Miniconda3-latest-MacOSX-$(uname -m).sh"
    else
        INSTALLER="Miniconda3-latest-Linux-$(uname -m).sh"
    fi
    curl -O "https://repo.anaconda.com/miniconda/${INSTALLER}"
    bash "${INSTALLER}" -b
fi

# Conda 환셩 생성 및 활성화
## TODO
echo "conda 초기화중..."
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

echo "가상환경을 생성합니다..."
if conda info --envs | grep -q -w 'myenv'; then
    echo "myenv 가상환경이 이미 존재합니다. 생성을 건너뜁니다."
else
    conda create -n myenv python=3.11 -y
fi

echo "가상환경을 활성화합니다..."
conda activate myenv

echo "현재 파이썬 버전 : "
python --version


## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
echo "필요한 패키지를 설치합니다..."
pip install mypy

echo "mypy_log.txt 초기화"
>mypy_log.txt

mkdir -p output

for file in submission/*.py; do
    ## TODO
    prob_num=$(echo "$file" | cut -d'_' -f2 | cut -d'.' -f1)
    echo "실행 중 : $file (문제번호 : $prob_num)"
    python "$file" < "input/${prob_num}_input" > "output/${prob_num}_output"
    # mypy 실행 결과(원본 출력)를 mypy_log.txt에 저장
    echo "== $file ==" >> mypy_log.txt
    mypy "$file" >> mypy_log.txt 2>&1
done

# # conda.yml 파일 생성
# ## TODO
echo "conda.yml 초기화"
>conda.yml
echo "가상환경 설정을 conda.yml로 내보냅니다..."
conda env export > conda.yml

# # 가상환경 비활성화
# ## TODO
echo "가상환경을 종료합니다..."
conda deactivate

echo "작업 완료"