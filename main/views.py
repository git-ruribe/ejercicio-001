from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import *
import datetime


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

        #Aquí hay que implementar el filtro de fecha
        filtrofecha = Filtros.objects.filter()[:1].get()
        inicial = filtrofecha.fecha_inicial
        final = filtrofecha.fecha_final
        todosEncuentros=Encuentro.objects.filter(fecha_date__gte = inicial, fecha_date__lte = final).order_by('fecha_date')
        listatodosEncuentros=list(todosEncuentros.values_list('pk',flat=True))

        encuentros=list(set(relQuinEnc.objects.filter(quiniela__in=misQuinielas).values_list('encuentro',flat=True)))
        misEncuentros=Encuentro.objects.filter(pk__in=encuentros).filter(fecha_date__gte = inicial, fecha_date__lte = final).order_by('fecha_date')
        print(misEncuentros)
        misPronosticos=Pronostico.objects.filter(encuentro__in=listatodosEncuentros).filter(usuario=usuario)
        pronosticos=list(misPronosticos.values_list('encuentro',flat=True))
        print(misPronosticos)
        conPronostico=misEncuentros.filter(pk__in=pronosticos)
        sinPronostico=misEncuentros.exclude(pk__in=pronosticos)
        otrosEncuentros=todosEncuentros.exclude(pk__in=pronosticos).exclude(pk__in=encuentros)
        print(sinPronostico)

        saludo="Bienvenido " + nombre
        template = loader.get_template('main/inicio.html')
        context = {
            'saludo': saludo,
            'conPronostico_list': misPronosticos,
            'sinPronostico_list': sinPronostico,
            'otrosEncuentros_list': otrosEncuentros,
            'ahora': datetime.datetime.now(),

        }
    else:
        saludo="Ingresa para ver tu página personal"
        template = loader.get_template('main/visitor.html')
        context = {
            'saludo': saludo,
        }

    return HttpResponse(template.render(context, request))

def pronosticar(request):

    recibidos = request.POST
    lista = list(recibidos)
    texto =""
    pronos_L = []
    pronos_E = []
    pronos_V = []

    for cadauno in lista:
        if cadauno[0] == 'P':
            if recibidos.__getitem__(cadauno) == 'L':
                 pronos_L.append(cadauno[1:])
            if recibidos.__getitem__(cadauno) == 'E':
                 pronos_E.append(cadauno[1:])
            if recibidos.__getitem__(cadauno) == 'V':
                 pronos_V.append(cadauno[1:])
            if recibidos.__getitem__(cadauno) == 'N':
                 Pronostico.objects.filter(pk = cadauno[1:]).delete()

        if cadauno[0] == 'E' and recibidos.__getitem__(cadauno)!='N' :
            esteEncuentro = Encuentro.objects.get(pk = cadauno[1:])
            nuevoPron = Pronostico(usuario = request.user, encuentro = esteEncuentro , resultado = recibidos.__getitem__(cadauno))
            nuevoPron.save()

        if cadauno[0] == 'k':
            Pronostico.objects.filter(pk__in = cadauno[1:]).update(candado = True)

    Pronostico.objects.filter(pk__in=pronos_L).update(resultado="L")
    Pronostico.objects.filter(pk__in=pronos_E).update(resultado="E")
    Pronostico.objects.filter(pk__in=pronos_V).update(resultado="V")

    template = loader.get_template('main/pronosticar.html')
    context = {
        'check': texto,
    }
    return HttpResponse(template.render(context, request))

def resultados(request,anio, semana):
    import pandas as pd
    import numpy as np
    from scipy.stats import binom

    def iso_to_gregorian(iso_year, iso_week, iso_day):
        #"Gregorian calendar date for the given ISO year, week and day"
        fourth_jan = datetime.date(iso_year, 1, 4)
        _, fourth_jan_week, fourth_jan_day = fourth_jan.isocalendar()
        return fourth_jan + datetime.timedelta(days=iso_day-fourth_jan_day, weeks=iso_week-fourth_jan_week)

    inicial = iso_to_gregorian (anio, semana, 1)
    final = iso_to_gregorian (anio, semana + 1, 1)

    encuentro_list = Encuentro.objects.filter(fecha_date__gte = inicial, fecha_date__lte = final, termino_bool = True).order_by('fecha_date')[:]
    pronostico_list = Pronostico.objects.filter (encuentro__in = encuentro_list).order_by('usuario')

    #data = pd.DataFrame(list(pronostico_list.values('usuario__username','encuentro__fecha_date','encuentro__local__equipo_text','encuentro__visita__equipo_text','encuentro__resultado', 'resultado')))
    data = pd.DataFrame()
    data['horario'] = pronostico_list.values_list('encuentro__fecha_date',flat=True)
    data['local'] = pronostico_list.values_list('encuentro__local__equipo_text',flat=True)
    data['visita'] = pronostico_list.values_list('encuentro__visita__equipo_text',flat=True)
    data['resultado'] = pronostico_list.values_list('encuentro__resultado',flat=True)
    data['pronostico'] = pronostico_list.values_list('resultado',flat=True)
    data['usuario'] = pronostico_list.values_list('usuario__username',flat=True)

    data['win'] = (data['resultado'] == data['pronostico'])*1

    data['winX'] = 0

    if len(data['pronostico']) >0 :
        data['winX'] = (data['pronostico'] == 'L') *1
        data['winX'] = data['winX'] + (data['pronostico']== 'E') *2
        data['winX'] = data['winX'] + (data['pronostico']== 'V') *3
        data['winX'] = data['winX'] + (data['resultado'] == data['pronostico'])*3



    tabla = pd.DataFrame(data.groupby('usuario')['win'].agg(['count','sum']))
    tabla['puntos'] = np.rint(10/binom.pmf(tabla['sum'],tabla['count'],0.3333))

    partidos = pd.DataFrame(data.groupby(['local','visita','resultado'])['win'].agg(['count','sum']))

    pivote = pd.pivot_table(data, index =['local', 'visita','resultado'], columns = ['usuario'], values=['winX'])
    pivote = pivote.fillna('')
    pivote = pivote.replace(1, 'L-', regex=True)
    pivote = pivote.replace(2, 'E-', regex=True)
    pivote = pivote.replace(3, 'V-', regex=True)
    pivote = pivote.replace(4, 'L+', regex=True)
    pivote = pivote.replace(5, 'E+', regex=True)
    pivote = pivote.replace(6, 'V+', regex=True)

    template = loader.get_template('main/resultados.html')
    context = {
        'partidos' : partidos,
        'tabla': tabla,
        'pivote': pivote,
    }
    return HttpResponse(template.render(context, request))
