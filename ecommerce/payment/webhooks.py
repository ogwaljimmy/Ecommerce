# payment/webhooks.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Order
from .payment_processor import MobileMoneyProcessor

@csrf_exempt
# payment/webhooks.py
@csrf_exempt
def flutterwave_webhook(request):
    if request.method == 'POST':
        try:
            # Verify the webhook signature
            secret_hash = settings.FLUTTERWAVE_SECRET_HASH
            signature = request.headers.get('verif-hash')
            if signature != secret_hash:
                return HttpResponse(status=401)

            payload = json.loads(request.body)
            
            if payload.get('event') == 'charge.completed':
                data = payload.get('data', {})
                tx_ref = data.get('tx_ref', '')
                
                if tx_ref.startswith('MM-'):  # Mobile Money transaction
                    order_id = tx_ref.split('-')[1]
                    try:
                        order = Order.objects.get(id=order_id)
                        
                        if (data.get('status') == 'successful' and 
                            float(data.get('amount')) == float(order.amount_paid)):
                            
                            order.payment_verified = True
                            order.payment_reference = data.get('flw_ref')
                            order.save()
                            
                            if 'cart' in request.session:
                                del request.session['cart']
                            
                            return HttpResponse(status=200)
                    except Order.DoesNotExist:
                        pass
            
            return HttpResponse(status=200)
        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            return HttpResponse(str(e), status=400)
    
    return HttpResponse(status=405)