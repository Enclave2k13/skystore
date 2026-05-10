from django.shortcuts import render
from catalog.models import Product
from catalog.models import Contact


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]

    print("\n" + "=" * 50)
    print("ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ:")
    for i, product in enumerate(latest_products, 1):
        print(f"{i}. {product.name} — {product.price} руб. (создан: {product.created_at})")
    print("=" * 50 + "\n")

    return render(request, 'catalog/home.html', {'latest_products': latest_products})


def contacts(request):
    message_sent = False

    contact_info = Contact.objects.first

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print("\n" + "=" * 50)
        print("ПОЛУЧЕН POST-ЗАПРОС")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print("=" * 50 + "\n")

        message_sent = True

    return render(request, 'catalog/contacts.html', {
        'message_sent': message_sent,
        'contact': contact_info
    })