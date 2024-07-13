from django.db import models
from django.db.models import Sum, Max  # Add this line

class Person(models.Model):
    name = models.CharField(max_length=100)
    money_given = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class MealEntry(models.Model):
    date = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    meals_taken = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.person} - {self.date}'

class BazarEntry(models.Model):
    date = models.DateField()
    serial_number = models.PositiveIntegerField(unique=True, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    money_given = models.DecimalField(max_digits=10, decimal_places=2)
    money_take_from_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    money_left = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.serial_number:
            max_serial = BazarEntry.objects.aggregate(models.Max('serial_number'))['serial_number__max']
            self.serial_number = (max_serial or 0) + 1
        self.money_left = self.money_given - self.cost
        total_money_left = BazarEntry.objects.aggregate(total_money_left=Sum('money_left'))['total_money_left'] or 0
        total_money_left -= self.money_take_from_cash
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.serial_number} - {self.item}'
