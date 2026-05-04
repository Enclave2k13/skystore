from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    message_sent = False

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

    return render(request, 'catalog/contacts.html', {'message_sent': message_sent})