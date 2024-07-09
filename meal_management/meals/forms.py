from django import forms
from .models import MealEntry, BazarEntry, Person

class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ['date', 'person', 'meals_taken']

class BazarEntryForm(forms.ModelForm):
    class Meta:
        model = BazarEntry
        fields = ['date', 'person', 'money_given', 'item', 'cost']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),

        }

    def save(self, *args, **kwargs):
        money_given = self.cleaned_data['money_given']
        cost = self.cleaned_data['cost']
        money_left = money_given - cost
        self.instance.money_left = money_left
        super().save(*args, **kwargs)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name']
