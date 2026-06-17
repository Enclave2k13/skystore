from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from catalog.models import Product, Contact
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class HomeView(ListView):
    """Главная страница со списком товаров и пагинацией"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ContactsView(TemplateView):
    """Страница контактов с формой обратной связи"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        context['message_sent'] = False
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print("\n" + "=" * 50)
        print("ПОЛУЧЕН POST-ЗАПРОС")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print("=" * 50 + "\n")

        context['message_sent'] = True
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Страница добавления нового товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        product = form.save()
        print(f"\n✅ ДОБАВЛЕН НОВЫЙ ТОВАР: {product.name} (ID: {product.pk})")
        return redirect('catalog:product_detail', pk=product.pk)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление товара"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_product')

class ProductTogglePublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Переключение статуса публикации"""
    model = Product
    fields = []
    http_method_names = ['post']

    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_published = not product.is_published
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)
