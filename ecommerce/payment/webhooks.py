# payment/webhooks.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Order
from .payment_processor import MobileMoneyProcessor

@csrf_exempt
def flutterwave_webhook(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            if payload.get('event') == 'charge.completed':
                tx_ref = payload.get('data', {}).get('tx_ref', '')
                if tx_ref.startswith('MM-'):  # Mobile Money transaction
                    order_id = tx_ref.split('-')[1]
                    order = Order.objects.get(id=order_id)
                    
                    processor = MobileMoneyProcessor()
                    verification = processor.verify_payment(payload.get('data', {}).get('id'))
                    
                    if verification.get('status') == 'success':
                        data = verification.get('data', {})
                        if data.get('status') == 'successful':
                            order.payment_verified = True
                            order.payment_reference = data.get('flw_ref')
                            order.save()
            
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(str(e), status=400)
    
    return HttpResponse(status=405)