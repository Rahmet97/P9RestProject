import os

import requests
from django.conf import settings
from django.shortcuts import render
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import SubscribeSerializer

load_dotenv()


class CardCreateAPIView(APIView):
    permission_classes = ()

    def card_create(self, validated_data):
        cash_id = os.getenv('CASH_ID')
        data = dict(
            id=validated_data['id'],
            method='cards.create',
            params=dict(
                card=dict(
                    number=validated_data['params']['card']['number'],
                    expire=validated_data['params']['card']['expire']
                ),
                save=validated_data['params']['save']
            )
        )
        url = os.getenv('BASE_URL') + '/api'
        response = requests.post(
            url,
            headers={'X-Auth': cash_id, 'Cache-Control': 'no-cache'},
            json=data
        )
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        result = self.card_get_verify_code(token)

        return result

    def card_get_verify_code(self, token):
        cash_id = os.getenv('CASH_ID')
        data = dict(
            method='cards.get_verify_code',
            params=dict(
                token=token
            )
        )
        url = os.getenv('BASE_URL') + '/api'
        response = requests.post(
            url,
            headers={'X-Auth': cash_id, 'Cache-Control': 'no-cache'},
            json=data
        )
        result = response.json()
        if 'error' in result:
            return result

        result.update(token=token)
        return result

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data)
        return Response(result)


class CardVerifyAPIView(APIView):
    permission_classes = ()

    def card_verify(self, validated_data):
        cash_id = os.getenv('CASH_ID')
        data = dict(
            id=validated_data['id'],
            method='cards.verify',
            params=dict(
                token=validated_data['params']['token'],
                code=validated_data['params']['code'],
            )
        )
        url = os.getenv('BASE_URL') + '/api'
        response = requests.post(
            url,
            headers={'X-Auth': cash_id, 'Cache-Control': 'no-cache'},
            json=data
        )
        result = response.json()
        return result

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data)
        return Response(result)


class PaymentApiView(APIView):

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['params']['token']
        result = self.receipts_create(token, serializer.validated_data)

        return Response(result)

    def receipts_create(self, token, validated_data):
        cash_id = os.getenv('CASH_ID')
        cash_secret = os.getenv('CASH_SECRET')
        url = os.getenv('BASE_URL') + '/api'
        data = dict(
            id=validated_data['id'],
            method='receipts.create',
            params=dict(
                amount=validated_data['params']['amount'],
                account=dict(
                    order_id='test'
                    # order_id=validated_data['params']['account'][settings.PAYME_SETTINGS['ACCOUNTS']['KEY_1']]
                )
            )
        )
        response = requests.post(
            url,
            json=data,
            headers={
                'X-Auth': f"{cash_id}:{cash_secret}",
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json'
            }
        )
        result = response.json()
        if 'error' in result:
            return result

        trans_id = result['result']['receipt']['_id']
        trans = Transaction()
        print(result)
        trans.create_transaction(
            trans_id=trans_id,
            request_id=result['id'],
            amount=result['result']['receipt']['amount'],
            account=result['result']['receipt']['account'],
            status=trans.Status.PROCESS,
        )
        result = self.receipts_pay(trans_id, token)
        return result

    def receipts_pay(self, trans_id, token):
        cash_id = os.getenv('CASH_ID')
        cash_secret = os.getenv('CASH_SECRET')
        url = os.getenv('BASE_URL') + '/api'
        data = dict(
            method='',
            params=dict(
                id=trans_id,
                token=token,
            )
        )
        response = requests.post(url, json=data, headers={
            'X-Auth': f"{cash_id}:{cash_secret}",
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        })
        result = response.json()
        trans = Transaction()

        if 'error' in result:
            trans.update_transaction(
                trans_id=trans_id,
                status=trans.Status.FAILED,
            )
            return result

        trans.update_transaction(
            trans_id=result['result']['receipt']['_id'],
            status=trans.Status.PAID,
        )

        return result