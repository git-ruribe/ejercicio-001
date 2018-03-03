from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import *


def bienvenida(request):
    return HttpResponse("Vista principal KiNeLa")

def detail(request, encuentro_id):
    return HttpResponse("Página del equipo %s." % encuentro_id)

def results(request, encuentro_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % encuentro_id)

def vote(request, encuentro_id):
    return HttpResponse("You're voting on question %s." % encuentro_id)

def equipos(request):
    equipo_list = Equipo.objects.order_by('-equipo_text')[:18]
    template = loader.get_template('main/equipos.html')
    context = {
        'equipo_list': equipo_list,
    }
    return HttpResponse(template.render(context, request))

def jornada(request, jornada_id):
    jornada_detail = Jornada.objects.get(id=jornada_id)
    encuentro_list = Encuentro.objects.order_by('fecha_date').filter(jornada=jornada_id)[:18]
    template = loader.get_template('main/jornada.html')
    context = {
        'jornada_detail': jornada_detail,
        'encuentro_list': encuentro_list,
    }
    return HttpResponse(template.render(context, request))

def jornadaactual(request):
    actual=1
    jornada_detail = Jornada.objects.get(id=actual)
    encuentro_list = Encuentro.objects.order_by('fecha_date').filter(jornada=actual)[:]
    template = loader.get_template('main/jornada.html')
    context = {
        'jornada_detail': jornada_detail,
        'encuentro_list': encuentro_list,
    }
    return HttpResponse(template.render(context, request))

def inicio(request):
    if request.user.is_authenticated:
        usuario = request.user
        nombre = usuario.first_name

        pools = list(relUserPool.objects.filter(usuario=usuario).values_list('pool',flat=True))
        misPoolAmigos=PoolAmigos.objects.filter(pk__in=pools)
        print(misPoolAmigos)
        quinielas=list(set(relQuinPool.objects.filter(pool__in=misPoolAmigos).values_list('quiniela',flat=True)))
        misQuinielas=Quiniela.objects.filter(pk__in=quinielas)
        print(misQuinielas)
        encuentros=list(set(relQuinEnc.objects.filter(quiniela__in=misQuinielas).values_list('encuentro',flat=True)))
        misEncuentros=Encuentro.objects.filter(pk__in=encuentros)
        print(misEncuentros)
        misPronosticos=Pronostico.objects.filter(encuentro__in=misEncuentros)
        print(misPronosticos)

        saludo="Bienvenido " + nombre
    else:
        saludo="Ingresa para ver tu página personal"

    template = loader.get_template('main/inicio.html')
    context = {
            'saludo': saludo,
    }
    return HttpResponse(template.render(context, request))
