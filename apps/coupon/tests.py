from rest_framework import status
from rest_framework.test import APITestCase

from .models import Coupon, CouponType


class TestOrder(APITestCase):
    def setUp(self):
        """ Test 시작 전 필요한 임시 데이터 생성 """

        self.coupon_url = '/api/v1/coupons'
        self.coupon_type_url = '/api/v1/coupons/types'

    def tearDown(self):
        """ Test를 위해 생성했던 임시 데이터 삭제 """
        Coupon.objects.all().delete()
        CouponType.objects.all().delete()

    def test_coupon_over_100_percent(self):
        """ 쿠폰 할인율이 100%가 넘는 경우 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '% 할인',
            'name': '200% 할인 쿠폰',
            'value': 200
        }
        self.response = self.client.post(self.coupon_type_url, data, format='json')

        # ValidationError가 발생하는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coupon_issue_expr(self):
        """ 쿠폰 발급일, 만료일 테스트 """

        # 쿠폰 타입 생성
        data = {
            'category': '배송비 할인',
            'name': '배송비 2000원 할인 쿠폰',
            'value': 2000,
            'issue_date': '2022-09-14',
            'expr_date': '2022-08-14'
        }
        self.response = self.client.post(self.coupon_type_url, data, format='json')

        # ValidationError가 발생하는지 확인
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
