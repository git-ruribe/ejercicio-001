from django.db import models
from django.contrib.auth.models import User

class Filtros(models.Model):
    fecha_inicial = models.DateTimeField('Inicial')
    fecha_final = models.DateTimeField('Final')
    def __str__(self):
        return self.fecha_inicial.strftime('%Y-%m-%d %H:%M') + "->" + self.fecha_final.strftime('%Y-%m-%d %H:%M')

class Deporte(models.Model):
    deporte_text = models.CharField(max_length=200)
    def __str__(self):
        return self.deporte_text

class Liga(models.Model):
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    liga_text = models.CharField(max_length=200)
    def __str__(self):
        return self.liga_text

class Temporada(models.Model):
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
    temporada_text = models.CharField(max_length=200)
    inicio_date = models.DateTimeField('Arranque')
    fin_date = models.DateTimeField('Final')
    puntosVictoria_int = models.IntegerField
    puntosEmpate_int = models.IntegerField
    puntosDerrota_int = models.IntegerField
    def __str__(self):
        return self.temporada_text


class Jornada(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    jornada_int = models.IntegerField
    jornada_text = models.CharField(max_length=200)
    inicio_date = models.DateTimeField('Arranque')
    fin_date = models.DateTimeField('Final')
    def __str__(self):
        return self.jornada_text

class Equipo(models.Model):
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE)
    equipo_text = models.CharField(max_length=200)
    escudo_text = models.CharField(max_length=200)
    camiseta_text = models.CharField(max_length=200)
    activo_bool = models.BooleanField(default=True)
    def __str__(self):
        return self.equipo_text

class Encuentro(models.Model):
    RESULTADOS = (
        ('L', 'Local'),
        ('E', 'Empate'),
        ('V', 'Visita'),
        ('N', 'Sin Resultado'),
    )
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    local = models.ForeignKey(Equipo, related_name='local', on_delete=models.CASCADE)
    visita = models.ForeignKey(Equipo, related_name='visita', on_delete=models.CASCADE)
    fecha_date = models.DateTimeField('Fecha', null=True, blank=True)
    resultado = models.CharField(max_length=1, choices=RESULTADOS, null=True, blank=True)
    scoreLocal_int = models.IntegerField(null=True, blank=True)
    scoreVisita_int = models.IntegerField(null=True, blank=True)
    puntosLocal_int = models.IntegerField(null=True, blank=True)
    puntosVisita = models.IntegerField(null=True, blank=True)
    empezo_bool = models.BooleanField(default=False)
    termino_bool = models.BooleanField(default=False)
    def __str__(self):
        return self.jornada.jornada_text + " " +self.local.equipo_text + "-" + self.visita.equipo_text

class PoolAmigos(models.Model):
    pool_text = models.CharField(max_length=200)
    imagen_text = models.CharField(null=True, blank=True, max_length=200)
    creado_date = models.DateTimeField('creado')
    publico_bool = models.BooleanField(default=False)
    def __str__(self):
        return self.pool_text

class relUserPool(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pool = models.ForeignKey(PoolAmigos, on_delete=models.CASCADE)
    creado_date = models.DateTimeField('creado')
    class Meta:
        unique_together = ('usuario', 'pool',)

    def __str__(self):
        return self.usuario.get_username() + "->" + self.pool.pool_text

class Quiniela(models.Model):
    quiniela_text = models.CharField(max_length=200)
    descripcion_text = models.CharField(null=True, blank=True, max_length=200)
    imagen_text = models.CharField(null=True, blank=True, max_length=200)
    creado_date = models.DateTimeField('creado')
    public_bool = models.BooleanField(default=False)
    def __str__(self):
        return self.quiniela_text

class relQuinEnc(models.Model):
    quiniela = models.ForeignKey(Quiniela, on_delete=models.CASCADE)
    encuentro = models.ForeignKey(Encuentro, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('quiniela', 'encuentro',)
    def __str__(self):
        return self.encuentro.local.equipo_text + "-" + self.encuentro.visita.equipo_text + "->" + self.quiniela.quiniela_text

class relQuinPool(models.Model):
    quiniela = models.ForeignKey(Quiniela, on_delete=models.CASCADE)
    pool = models.ForeignKey(PoolAmigos, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('quiniela', 'pool',)
    def __str__(self):
        return self.pool.pool_text + "->" + self.quiniela.quiniela_text

class Pronostico(models.Model):
    RESULTADOS = (
        ('L', 'Local'),
        ('E', 'Empate'),
        ('V', 'Visita'),
        ('N', 'Sin Resultado'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    encuentro = models.ForeignKey(Encuentro, on_delete=models.CASCADE)
    con_marcador = models.BooleanField(default=False)
    candado = models.BooleanField(default=False)
    resultado = models.CharField(max_length=1, choices=RESULTADOS, null=True, blank=True)
    scoreLocal_int = models.IntegerField(null=True, blank=True)
    scoreVisita_int = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'encuentro',)

    def __str__(self):
        return self.encuentro.local.equipo_text +"-"+self.usuario.get_username()+"-"+ self.encuentro.visita.equipo_text
