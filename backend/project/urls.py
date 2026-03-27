from django.urls import path, include
from django.views import View
from django.http import JsonResponse

class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('api/health/', HealthCheckView.as_view(), name='health'),
    path('api/', include('apps.api.urls')),
]
