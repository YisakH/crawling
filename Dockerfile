# 파이썬 이미지를 기반으로 합니다.
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app
COPY . /app

# 필요한 패키지 설치
RUN pip install requests beautifulsoup4 pymongo

# 스크립트 실행 권한 부여
RUN chmod +x run.sh

# 실행할 명령어 설정
CMD ["./run.sh"]
