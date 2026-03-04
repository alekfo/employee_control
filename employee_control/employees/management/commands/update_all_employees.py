from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from employees.models import Employee

User = get_user_model()

class Command(BaseCommand):
    """"
    Create all employees from user's table
    """

    def handle(self, *args, **options):
        self.stdout.write("Проверяю пользователей без профиля Employee...")

        # Находим всех пользователей, у которых нет связанного Employee
        # (profile — это related_name из OneToOneField в Employee)
        users_without_profile = User.objects.filter(profile__isnull=True)
        count = users_without_profile.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("У всех пользователей уже есть профиль Employee."))
            return

        self.stdout.write(f"Найдено {count} пользователей без профиля. Создаю...")

        created_count = 0
        for user in users_without_profile:
            Employee.objects.create(
                user=user,
                position='Инженер',  # можно оставить пустым или заполнить чем-то по умолчанию
                phone=''
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Успешно создано {created_count} профилей Employee."))