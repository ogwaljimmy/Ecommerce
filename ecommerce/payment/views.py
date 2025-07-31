from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from .payment_processor import MobileMoneyProcessor

def checkout(request):
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}
            return render(request, 'payment/checkout.html', context=context)
        except ShippingAddress.DoesNotExist:
            return render(request, 'payment/checkout.html')
    else:
        return render(request, 'payment/checkout.html')


@csrf_exempt
def complete_order(request):
    if request.POST.get('action') == 'post':
        # Collect form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        payment_method = request.POST.get('payment_method', 'paypal')
        tx_id = request.POST.get('transaction_id')  # For Flutterwave
        tx_ref = request.POST.get('tx_ref')

        # Construct shipping address
        shipping_address = f"{address1}\n{address2}\n{city}\n{state}\n{zipcode}"

        # Get cart & total
        cart = Cart(request)
        total_cost = cart.get_total()

        # Flutterwave Payment Flow
        if payment_method == 'flutterwave':
            processor = MobileMoneyProcessor()
            result = processor.verify_payment(tx_id)

            if result.get('status') == 'success':
                data = result['data']
                if (data.get('status') == 'successful' and 
                    float(data.get('amount')) == float(total_cost)):

                    # Create order and items
                    order_data = {
                        'full_name': name,
                        'email': email,
                        'shipping_address': shipping_address,
                        'amount_paid': total_cost,
                        'payment_method': 'flutterwave',
                        'payment_verified': True,
                        'payment_reference': data.get('flw_ref'),
                    }
                    if request.user.is_authenticated:
                        order_data['user'] = request.user

                    order = Order.objects.create(**order_data)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            quantity=item['qty'],
                            price=item['price'],
                            user=request.user if request.user.is_authenticated else None
                        )

                    cart.clear()
                    return JsonResponse({'success': True})

                else:
                    return JsonResponse({'success': False, 'message': 'Invalid amount or payment status'})
            else:
                return JsonResponse({'success': False, 'message': result.get('message', 'Verification failed')})

        # PayPal Flow (payment handled client-side)
        if payment_method == 'paypal':
            order_data = {
                'full_name': name,
                'email': email,
                'shipping_address': shipping_address,
                'amount_paid': total_cost,
                'payment_method': 'paypal',
                'payment_verified': True,  # Trusting PayPal JS confirmation
            }
            if request.user.is_authenticated:
                order_data['user'] = request.user

            order = Order.objects.create(**order_data)

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user if request.user.is_authenticated else None
                )

            cart.clear()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'message': 'Unsupported payment method'})


@csrf_exempt
def verify_mobile_money(request):
    # You can optionally keep this if you still use Flutterwave with redirect_url method.
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        order_id = request.POST.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
            processor = MobileMoneyProcessor()
            verification = processor.verify_payment(transaction_id)

            if verification.get('status') == 'success':
                data = verification.get('data', {})
                if (data.get('status') == 'successful' and 
                    float(data.get('amount')) == float(order.amount_paid)):

                    order.payment_verified = True
                    order.payment_reference = data.get('flw_ref')
                    order.save()

                    if 'cart' in request.session:
                        del request.session['cart']

                    return JsonResponse({'success': True})

            return JsonResponse({
                'success': False, 
                'message': verification.get('message', 'Payment verification failed')
            })

        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid order'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def payment_success(request):
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')
