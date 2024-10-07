from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('', RedirectView.as_view(url='admin/'), name='redirect-to-admin'),
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
]
