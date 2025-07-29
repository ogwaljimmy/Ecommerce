from django.test import TestCase
from unittest.mock import patch
from payment.payment_processor import MobileMoneyProcessor

class MobileMoneyTests(TestCase):
    @patch('requests.post')
    def test_successful_payment_initiation(self, mock_post):
        # Mock Flutterwave API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "status": "success",
            "data": {"link": "https://checkout.flutterwave.com/test/123"}
        }
        
        processor = MobileMoneyProcessor()
        result = processor.initiate_payment(MockOrder(), "256772123456", "mtn")
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('checkout.flutterwave.com', result['data']['link'])