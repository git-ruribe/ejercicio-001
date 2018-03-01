from django.http import HttpResponse
from django.template import loader
from .models import Equipo
from .models import Jornada
from .models import Encuentro


def bienvenida(request):
    return HttpResponse("Vista principal KiNeLa")

def detail(request, encuentro_id):
    return HttpResponse("You're looking at question %s." % encuentro_id)

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
