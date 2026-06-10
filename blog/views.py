from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    """Список блоговых записей (только опубликованные)"""
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница блоговой записи с увеличением просмотров"""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            send_mail(
                subject='Статья набрала 100 просмотров!',
                message=f'Поздравляем! Ваша статья "{obj.title}" набрала 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['your-email@example.com'],
                fail_silently=True,
            )

        return obj


class BlogPostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Создание новой блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        return self.request.user.has_perm('blog.can_manage_blog')


class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.has_perm('blog.can_manage_blog')


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        return self.request.user.has_perm('blog.can_manage_blog')