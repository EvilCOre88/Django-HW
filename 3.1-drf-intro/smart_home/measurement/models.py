from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30, verbose_name='Датчик')
    description = models.CharField(max_length=30, verbose_name='Описание')

class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, db_column='sensor', on_delete=models.CASCADE, related_name='measurements', verbose_name='ID датчика')
    temp = models.FloatField(verbose_name='Температура')
    measuring_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время замера')
    photo = models.ImageField(upload_to='measurement/measurements', null=True, blank=True)