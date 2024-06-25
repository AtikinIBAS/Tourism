# from django.shortcuts import render
# from .forms import RouteForm
# from .models import Attraction, Route
# from .tourism_nn import predict_route  # Импортируйте вашу функцию для предсказания маршрута
#
#
# def home(request):
#     if request.method == 'POST':
#         form = RouteForm(request.POST)
#         if form.is_valid():
#             start_point = form.cleaned_data['start_point']
#             time_limit = form.cleaned_data['time_limit']
#
#             # Используйте вашу нейронную сеть для предсказания маршрута
#             predicted_route, total_time, total_distance = predict_route(start_point, time_limit)
#
#             # Создание маршрута в базе данных
#             route = Route.objects.create(start_point=start_point, total_time=total_time, total_distance=total_distance)
#             for attraction in predicted_route:
#                 route.attractions.add(attraction)
#             route.save()
#
#             return render(request, 'routes/result.html', {'route': route})
#     else:
#         form = RouteForm()
#     return render(request, 'routes/home.html', {'form': form})


# routes/views.py


from django.shortcuts import render
from .models import Attraction, Route
from .tourism_nn import predict_route

def home(request):
    if request.method == 'POST':
        start_point_id = request.POST.get('start_point')
        time_limit = int(request.POST.get('time_limit'))
        try:
            start_point = Attraction.objects.get(pk=start_point_id)
            predicted_route, total_time, total_distance = predict_route(start_point.name, time_limit)
            context = {
                'route': predicted_route,
                'total_time': total_time,
                'total_distance': total_distance,
                'attractions': Attraction.objects.all()  # Передача всех достопримечательностей для выпадающего списка
            }
            return render(request, 'home.html', context)
        except Attraction.DoesNotExist:
            return render(request, 'home.html', {'error': 'Invalid start point or other error'})
    else:
        attractions = Attraction.objects.all()
        return render(request, 'home.html', {'attractions': attractions})

