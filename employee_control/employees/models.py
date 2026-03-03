from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name