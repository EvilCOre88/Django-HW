from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'помидор, шт': 0.5,
        'макароны, г': 0.3,
        'сыр, г': 0.05
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    }
}

def cooking(request, cook):
    template_name = 'calculator/index.html'
    ask_recept = DATA.get(cook, {})
    count = int(request.GET.get('servings', 1))
    context = {'recipe': cook, 'item': {}}
    for name, quantity in ask_recept.items():
        context['item'][name] = round(quantity * count, 2)
    return render(request, template_name, context)

def home(request):
    template_name = 'calculator/home.html'
    context = {'dish': {}}
    for name in DATA.keys():
        context['dish'][name] = reverse('recept', kwargs={'cook': name})
    return render(request, template_name, context)