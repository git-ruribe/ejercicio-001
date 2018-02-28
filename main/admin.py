from django.contrib import admin

from .models import Deporte
from .models import Liga
from .models import Temporada
from .models import Jornada
from .models import Equipo
from .models import Encuentro


admin.site.register(Deporte)
admin.site.register(Liga)
admin.site.register(Temporada)
admin.site.register(Jornada)
admin.site.register(Equipo)
admin.site.register(Encuentro)