from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import *
import datetime

def estadistica(request):
    import pandas as pd
    remote_file = 'http://www.football-data.co.uk/new/MEX.csv'
    data = pd.read_csv(remote_file)

    mindata = Filtros.objects.filter()[:1].get().importar_int

    print(str(mindata) + "->" + str(data['Country'].count()))

    for i in range(mindata, data['Country'].count() ):
        fechas = data['Date'][i].split("/")
        fecha = datetime.date(int(fechas[2])+2000,int(fechas[1]),int(fechas[0]))
        subir = Estadistica(country = data['Country'][i],
                            league = data['League'][i],
                            season = data['Season'][i],
                            date = fecha,
                            time = data['Time'][i],
                            home = data['Home'][i],
                            away = data['Away'][i],
                            hg = data['HG'][i],
                            ag = data['AG'][i],
                            res = data['Res'][i],
                            ph = data['PH'][i],
                            pd = data['PD'][i],
                            pa = data['PA'][i],
                            maxh = data['MaxH'][i],
                            maxd = data['MaxD'][i],
                            maxa = data['MaxA'][i],
                            avgh = data['AvgH'][i],
                            avgd = data['AvgD'][i],
                            avga = data['AvgA'][i]
                            )
        subir.save()

    template = loader.get_template('main/stats.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
