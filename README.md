# Commerce Admin API

원티드 프리온보딩 백엔드 기업 과제

## 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [과제 요구사항 분석](#과제-요구사항-분석)
3. [프로젝트 기술 스택](#프로젝트-기술-스택)
4. [개발 기간](#개발-기간)
5. [팀 구성](#팀-구성)
6. [역할](#역할)
7. [ERD](#ERD)
8. [API 목록](#API-목록)
9. [프로젝트 시작 방법](#프로젝트-시작-방법)

<br>

## 프로젝트 개요

쇼핑몰 관리 페이지 기능을 제공하는 Django 기반 API 서버입니다.


<br>

## 과제 요구사항 분석

### 1. 주문 내역

- 제품 주문 내역 열람
    - 필터: 주문 상태, 시작일자, 종료일자
    - 검색: 주문자명

### 2. 배송 상태

- 발송 처리
- 제품 배송 상태 업데이트(배송 중, 배송 완료 등)
    - 주문 상태: 결제완료 / 상품준비중 / 배송중 / 배송완료 / 결제취소

### 3. 쿠폰

- 방식: 배송비 할인, % 할인, 정액 할인
- 쿠폰 타입 신설
    - 필드: 유형, 이름, 할인값, 발급일, 만료일, 최소금액조건
    - 쿠폰 만료일이 발급일 이전일 경우 ValidationError 발생
- 신규 쿠폰 코드 발급
    - 필드: 쿠폰타입, 코드, 생성일, 수정일
    - 쿠폰 코드는 중복 불가
- 발급된 쿠폰 사용 내역 열람
- 쿠폰 타입 별 사용 횟수, 총 할인액
    - 쿠폰 타입 모델에 필드 추가
    - 쿠폰 사용할 때마다 업데이트

### 4. 구매하기 테스트 코드

- 쿠폰 사용에 따른 할인 적용
    - 한 번 사용한 쿠폰은 재사용 불가
    - 할인액이 원래 액수보다 클 경우 ValidationError 발생
    - 주문금액이 쿠폰 최소금액조건보다 작을 경우 ValidationError 발생
- 구매 국가, 구매 개수에 따른 배송비 적용
    - 달러단위 배송비인 경우 1200원=1달러로 적용하여 배송비 추가
    - (선택) 현재 원-달러 환율을 가져와서 배송비 적용

<br>

## 프로젝트 기술 스택

### Backend

<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB

<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools

<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord-5865F2?logo=Discord&logoColor=white">
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>


<br>

## 개발 기간

- 2022/09/08~2022/09/15

<br>

## 팀 구성

개인 프로젝트

<br>

## 역할

1. 요구사항 분석
2. 모델 및 API 설계
3. API 구현
4. 프로젝트 문서 작성
5. 테스트코드 작성

<br>

## ERD

![](https://i.imgur.com/FyqNU1j.png)


<br>

## API 목록

https://documenter.getpostman.com/view/17766148/2s7YYva2x5

<br>

## 프로젝트 시작 방법

1. 로컬에서 실행할 경우

```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b develop --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt
# 실행
python manage.py runserver
```

<br>
