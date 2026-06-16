from django.core.cache import cache
from catalog.models import Product, Category


def get_products_by_category(category_id):
    """
    Возвращает список продуктов в указанной категории с кешированием.
    Ключ: category_{category_id}_products
    TTL: 300 секунд (5 минут)
    """
    cache_key = f'category_{category_id}_products'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            category_id=category_id,
            is_published=True
        )
        cache.set(cache_key, products, timeout=300)

    return products


def get_categories_with_products():
    """
    Возвращает все категории с их продуктами (низкоуровневое кеширование).
    Ключ: categories_with_products
    TTL: 300 секунд (5 минут)
    """
    cache_key = 'categories_with_products'
    data = cache.get(cache_key)

    if data is None:
        categories = Category.objects.prefetch_related('products').all()
        data = [
            {
                'category': cat,
                'products': cat.products.filter(is_published=True)
            }
            for cat in categories
        ]
        cache.set(cache_key, data, timeout=300)

    return data


def clear_category_cache(category_id=None):
    """
    Очищает кеш для категории (или всех категорий).
    Используется при обновлении данных.
    """
    if category_id:
        cache.delete(f'category_{category_id}_products')
    else:
        cache.delete('categories_with_products')