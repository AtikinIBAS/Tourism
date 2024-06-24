from django.shortcuts import render
from .forms import RouteForm
from .models import Attraction, Route
from .tourism_nn import predict_route  # Импортируйте вашу функцию для предсказания маршрута


def home(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            start_point = form.cleaned_data['start_point']
            time_limit = form.cleaned_data['time_limit']

            # Используйте вашу нейронную сеть для предсказания маршрута
            predicted_route, total_time, total_distance = predict_route(start_point, time_limit)

            # Создание маршрута в базе данных
            route = Route.objects.create(start_point=start_point, total_time=total_time, total_distance=total_distance)
            for attraction in predicted_route:
                route.attractions.add(attraction)
            route.save()

            return render(request, 'routes/result.html', {'route': route})
    else:
        form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})
