from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Создаёт группу "Контент-менеджер" и назначает права на блог'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Контент-менеджер')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана'))

        content_type = ContentType.objects.get_for_model(BlogPost)

        perms = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS('Права на управление блогом назначены'))