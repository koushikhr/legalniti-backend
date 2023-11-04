from django.urls import path, include

urlpatterns = [
    path('documentation/', include('apps.documentation.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('namegen/', include('apps.namegen.urls')),
    path('trademark/',include('apps.trademark.urls')),
    path('startupindia/',include('apps.startupindia.urls')),
    path('forms/',include('apps.forms.urls')),
    path('services/',include('apps.services.urls')),
]