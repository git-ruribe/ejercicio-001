from django.db import models

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
