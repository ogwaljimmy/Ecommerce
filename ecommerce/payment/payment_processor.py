# payment/payment_processor.py
import requests
import time
import logging
from django.conf import settings
from requests.exceptions import RequestException
from .models import Order

logger = logging.getLogger(__name__)

class MobileMoneyProcessor:
    def __init__(self):
        self.secret_key = settings.FLUTTERWAVE_SECRET_KEY
        self.callback_url = f"{settings.BASE_URL}/payment/verify-mobile-money/"
        self.base_url = "https://api.flutterwave.com/v3"
    
    def _get_headers(self):
        """Helper method to get authorization headers"""
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
    
    def initiate_payment(self, order, phone_number, provider):
        """
        Initiate mobile money payment
        Returns: dict with status and response data
        """
        provider = provider.lower()
        endpoint = f"{self.base_url}/charges?type=mobile_money_{provider}"

        
        payload = {
            "tx_ref": f"MM-{order.id}-{int(time.time())}",
            "amount": str(order.amount_paid),
            "currency": "UGX",  # Update accordingly
            "email": order.email,
            "phone_number": phone_number,
            "fullname": order.full_name,
            "redirect_url": self.callback_url,
            "meta": {
                "order_id": order.id,
                "user_id": order.user.id if order.user else None
            }
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return {
                'status': 'success',
                'data': response.json()
            }
        except RequestException as e:
            logger.error(f"Payment initiation failed for order {order.id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'code': getattr(e.response, 'status_code', None)
            }
    
    def verify_payment(self, transaction_id):
        """
        Verify a mobile money payment
        Returns: dict with verification status
        """
        endpoint = f"{self.base_url}/transactions/{transaction_id}/verify"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            verification_data = response.json()
            if verification_data.get('status') == 'success':
                return {
                    'status': 'success',
                    'data': verification_data['data']
                }
            else:
                return {
                    'status': 'failed',
                    'message': verification_data.get('message', 'Verification failed')
                }
                
        except RequestException as e:
            logger.error(f"Payment verification failed for transaction {transaction_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'code': getattr(e.response, 'status_code', None)
            }