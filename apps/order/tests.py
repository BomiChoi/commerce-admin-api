from rest_framework import status
from rest_framework.test import APITestCase

from apps.country.models import Country, DeliveryCost
from apps.coupon.models import Coupon, CouponType
from .models import Order


class TestOrder(APITestCase):
    def setUp(self):
        """ Test 시작 전 필요한 임시 데이터 생성 """

        self.order_url = '/api/v1/orders'
        self.coupon_url = '/api/v1/coupons'
        self.coupon_type_url = '/api/v1/coupons/types'

        # 국가 정보 저장
        Country.objects.create(
            name='South Korea',
            code='KR',
            dcode='82'
        )
        Country.objects.create(
            name='USA',
            code='US',
            dcode='1'
        )

        # 배송비 정보 저장
        DeliveryCost.objects.create(
            country=Country.objects.get(name='USA'),
            quantity=1,
            cost=33370
        )
        DeliveryCost.objects.create(
            country=Country.objects.get(name='USA'),
            quantity=2,
            cost=42620
        )

    def tearDown(self):
        """ Test를 위해 생성했던 임시 데이터 삭제 """

        Order.objects.all().delete()
        Country.objects.all().delete()
        DeliveryCost.objects.all().delete()
        Coupon.objects.all().delete()
        CouponType.objects.all().delete()

    def test_create_order_korea(self):
        """ 국내 주문 테스트 """

        # 주문 생성
        data = {
            'quantity': 2,
            'price': 100000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미'
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # 요청이 성공적으로 처리되었는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # 배송비가 3000원인지 확인
        self.assertEqual(self.response.data['delivery_cost'], f'{3000:.2f}')

    def test_create_order_usa_1(self):
        """ 미국 주문 테스트 (1개) """

        # 주문 생성
        data = {
            'quantity': 1,
            'price': 50000,
            'buyr_country': Country.objects.get(code='US').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미'
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # 요청이 성공적으로 처리되었는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # 가격에 환율이 제대로 적용되었는지 확인
        rate = 1200
        self.assertEqual(self.response.data['price'], f'{(50000 / rate):.2f}')

        # 배송비가 일치하는지 확인
        self.assertEqual(self.response.data['delivery_cost'], f'{(33370 / rate):.2f}')

    def test_create_order_usa_2(self):
        """ 미국 주문 테스트 (2개) """

        # 주문 생성
        data = {
            'quantity': 2,
            'price': 100000,
            'buyr_country': Country.objects.get(code='US').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미'
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # 요청이 성공적으로 처리되었는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # 가격에 환율이 제대로 적용되었는지 확인
        rate = 1200
        self.assertEqual(self.response.data['price'], f'{(100000 / rate):.2f}')

        # 배송비가 일치하는지 확인
        self.assertEqual(self.response.data['delivery_cost'], f'{(42620 / rate):.2f}')

    def test_apply_coupon_delivery_cost(self):
        """ 배송비 할인 쿠폰 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '배송비 할인',
            'name': '배송비 2000원 할인 쿠폰',
            'value': 2000
        }
        coupon_type = self.client.post(self.coupon_type_url, data, format='json')

        # 쿠폰 생성
        data = {
            'type': coupon_type.data['id'],
            'code': 'ABCD-EFGH-IJKL-MNOP'
        }
        coupon = self.client.post(self.coupon_url, data, format='json')

        # 주문 생성
        data = {
            'quantity': 2,
            'price': 100000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미',
            'coupon': coupon.data['id']
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # 요청이 성공적으로 처리되었는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # 배송비 할인이 적용되었는지 확인
        self.assertEqual(self.response.data['delivery_cost'], f'{(3000 - 2000):.2f}')

    def test_apply_coupon_percent(self):
        """ % 할인 쿠폰 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '% 할인',
            'name': '30% 할인 쿠폰',
            'value': 30
        }
        coupon_type = self.client.post(self.coupon_type_url, data, format='json')

        # 쿠폰 생성
        data = {
            'type': coupon_type.data['id'],
            'code': 'ABCD-EFGH-IJKL-MNOP'
        }
        coupon = self.client.post(self.coupon_url, data, format='json')

        # 주문 생성
        data = {
            'quantity': 2,
            'price': 100000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미',
            'coupon': coupon.data['id']
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # 요청이 성공적으로 처리되었는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # % 할인이 적용되었는지 확인
        self.assertEqual(self.response.data['price'], f'{(100000 * (100 - 30) / 100):.2f}')

    def test_apply_coupon_fixed_amount(self):
        """ 정액 할인 쿠폰 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '정액 할인',
            'name': '10000원 할인 쿠폰',
            'value': 10000
        }
        coupon_type = self.client.post(self.coupon_type_url, data, format='json')

        # 쿠폰 생성
        data = {
            'type': coupon_type.data['id'],
            'code': 'ABCD-EFGH-IJKL-MNOP'
        }
        coupon = self.client.post(self.coupon_url, data, format='json')

        # 주문 생성
        data = {
            'quantity': 2,
            'price': 100000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미',
            'coupon': coupon.data['id']
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # 요청이 성공적으로 처리되었는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # % 할인이 적용되었는지 확인
        self.assertEqual(self.response.data['price'], f'{(100000 - 10000):.2f}')

    def test_coupon_duplicate(self):
        """ 쿠폰 중복 사용 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '배송비 할인',
            'name': '배송비 2000원 할인 쿠폰',
            'value': 2000
        }
        coupon_type = self.client.post(self.coupon_type_url, data, format='json')

        # 쿠폰 생성
        data = {
            'type': coupon_type.data['id'],
            'code': 'ABCD-EFGH-IJKL-MNOP'
        }
        coupon = self.client.post(self.coupon_url, data, format='json')

        # 주문 생성
        data = {
            'quantity': 2,
            'price': 100000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미',
            'coupon': coupon.data['id']
        }

        # 요청이 성공적으로 처리되었는지 확인
        self.response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # ValidationError가 발생하는지 확인
        self.response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_expr_date(self):
        """ 쿠폰 유효기간 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '배송비 할인',
            'name': '배송비 2000원 할인 쿠폰',
            'value': 2000,
            'issue_date': '2022-07-14',
            'expr_date': '2022-08-14'
        }
        coupon_type = self.client.post(self.coupon_type_url, data, format='json')

        # 쿠폰 생성
        data = {
            'type': coupon_type.data['id'],
            'code': 'ABCD-EFGH-IJKL-MNOP'
        }
        coupon = self.client.post(self.coupon_url, data, format='json')

        # 주문 생성
        data = {
            'quantity': 1,
            'price': 50000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미',
            'coupon': coupon.data['id']
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # ValidationError가 발생하는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_min_price(self):
        """ 쿠폰 최소금액조건 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '배송비 할인',
            'name': '배송비 2000원 할인 쿠폰',
            'value': 2000,
            'min_price': 100000
        }
        coupon_type = self.client.post(self.coupon_type_url, data, format='json')

        # 쿠폰 생성
        data = {
            'type': coupon_type.data['id'],
            'code': 'ABCD-EFGH-IJKL-MNOP'
        }
        coupon = self.client.post(self.coupon_url, data, format='json')

        # 주문 생성
        data = {
            'quantity': 1,
            'price': 50000,
            'buyr_country': Country.objects.get(code='KR').id,
            'buyr_zipcode': '08816',
            'buyr_name': '최보미',
            'coupon': coupon.data['id']
        }
        self.response = self.client.post(self.order_url, data, format='json')

        # ValidationError가 발생하는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
