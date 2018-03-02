from django.contrib import admin

from .models import Deporte
from .models import Liga
from .models import Temporada
from .models import Jornada
from .models import Equipo
from .models import Encuentro
from .models import PoolAmigos
from .models import relUserPool
from .models import Quiniela
from .models import relQuinEnc
from .models import relQuinPool


admin.site.register(Deporte)
admin.site.register(Liga)
admin.site.register(Temporada)
admin.site.register(Jornada)
admin.site.register(Equipo)
admin.site.register(Encuentro)
admin.site.register(PoolAmigos)
admin.site.register(relUserPool)
admin.site.register(Quiniela)
admin.site.register(relQuinEnc)
admin.site.register(relQuinPool)
