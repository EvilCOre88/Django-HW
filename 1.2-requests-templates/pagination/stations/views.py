from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings as set
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    bus_list = []
    with open(set.BUS_STATION_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            bus_list.append({
                'direction': row[1],
                'street': row[4],
                'district': row[6]
            })
    bus_list.pop(0)
    paginator = Paginator(bus_list, 10)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)


    context = {
        'bus_stations': page
    }
    return render(request, 'stations/index.html', context)
