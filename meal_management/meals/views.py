from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Max
from .models import MealEntry, BazarEntry, Person
from .forms import MealEntryForm, BazarEntryForm, PersonForm

def home(request):
    return render(request, 'meals/home.html')

def meal_entry(request):
    if request.method == 'POST':
        form = MealEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meal_entry')
    else:
        form = MealEntryForm()
    
    persons = Person.objects.all()
    return render(request, 'meals/meal_entry.html', {'form': form, 'persons': persons})

def bazar_entry(request):
    if request.method == 'POST':
        form = BazarEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bazar_entry')
    else:
        form = BazarEntryForm()
    return render(request, 'meals/bazar_entry.html', {'form': form})

def meal_summary(request):
    summary_data = []
    persons = Person.objects.all()

    year = request.GET.get('year')
    if not year:
        year = datetime.now().year
    month = request.GET.get('month')
    if not month:
        month = datetime.now().month
    first_day = datetime(int(year), int(month), 1)
    last_day = datetime(int(year), int(month) + 1, 1) - timedelta(days=1)
    total_meals = MealEntry.objects.filter(date__range=(first_day, last_day)).aggregate(total_meals=Sum('meals_taken'))['total_meals'] or 0
    total_cost = BazarEntry.objects.filter(date__range=(first_day, last_day)).aggregate(total_cost=Sum('cost'))['total_cost'] or 0

    person_costs = {}
    for person in persons:
        person_cost = BazarEntry.objects.filter(person=person).filter(date__range=(first_day, last_day)).aggregate(person_cost=Sum('cost'))['person_cost'] or 0
        person_costs[person.name] = person_cost

    cost_per_meal = total_cost / total_meals if total_meals > 0 else 0

    for person in persons:
        person_meals = MealEntry.objects.filter(person=person).filter(date__range=(first_day, last_day)).aggregate(person_meals=Sum('meals_taken'))['person_meals'] or 0
        person_cost = cost_per_meal * person_meals

        total_money_given = BazarEntry.objects.filter(person=person).filter(date__range=(first_day, last_day)).aggregate(total_money_given=Sum('money_given'))['total_money_given'] or 0
        money_balance = total_money_given - person_cost

        money_left_in_cash = sum(total_money_given for total_money_given in BazarEntry.objects.filter(date__range=(first_day, last_day)).values_list('money_given', flat=True)) - total_cost

        data = {
            'person': person,
            'person_meals': person_meals,
            'person_cost': person_cost,
            'person_costs': person_costs[person.name],
            'total_cost': total_cost,
            'total_money_given': total_money_given,
            'money_balance': money_balance,
        }
        summary_data.append(data)

    context = {
        'summary_data': summary_data,
        'cost_per_meal': cost_per_meal,
        'total_cost': total_cost,
        'money_left_in_cash': money_left_in_cash,
    }
    return render(request, 'meals/meal_summary.html', context)

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'meals/person_list.html', {'persons': persons})

def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'meals/person_form.html', {'form': form})

def person_edit(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)
    return render(request, 'meals/person_form.html', {'form': form})

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if MealEntry.objects.filter(person=person).exists():
        return render(request, 'meals/cannot_delete_person.html', {'person': person})
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'meals/person_confirm_delete.html', {'person': person})

def meal_details(request):
    meal_entries = MealEntry.objects.all().order_by('date')
    
    meal_data = {}
    for entry in meal_entries:
        date = entry.date
        person = entry.person
        meals_taken = entry.meals_taken
        
        if date not in meal_data:
            meal_data[date] = {}
        
        if person not in meal_data[date]:
            meal_data[date][person] = 0
        
        meal_data[date][person] += meals_taken
    
    context = {
        'meal_data': meal_data
    }
    return render(request, 'meals/meal_details.html', context)

def bazar_details(request):
    bazar_entries = BazarEntry.objects.all().order_by('date')
    
    bazar_data = {}
    for entry in bazar_entries:
        date = entry.date
        person = entry.person
        item = entry.item
        given_money = entry.money_given
        cost = entry.cost
        money_left = given_money - cost
        
        if date not in bazar_data:
            bazar_data[date] = {}
        if person not in bazar_data[date]:
            bazar_data[date][person] = {}
        if item not in bazar_data[date][person]:
            bazar_data[date][person][item] = {'given_money': 0, 'cost': 0, 'money_left': 0}
        
        bazar_data[date][person][item]['given_money'] += given_money
        bazar_data[date][person][item]['cost'] += cost
        bazar_data[date][person][item]['money_left'] = money_left
        
    context = {
        'bazar_data': bazar_data
    }
    return render(request, 'meals/bazar_details.html', context)
