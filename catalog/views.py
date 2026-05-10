from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from catalog.models import Product, Contact
from .forms import ProductForm


def home(request):
    products = Product.objects.all()

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/home.html', {'page_obj': page_obj})


def contacts(request):
    message_sent = False

    contact_info = Contact.objects.first()

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


def product_detail(request, pk):
    """Контроллер для страницы товара (Задание 1)"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_create(request):
    """Контроллер для добавления нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            print(f"\nДОБАВЛЕН НОВЫЙ ТОВАР: {product.name} (ID: {product.pk})")
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {'form': form})