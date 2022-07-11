from pyexpat import model
from django.db import models


# Create your models here.

class ToolDate(models.Model):
    tool_date_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    lst_extra_hours = models.CharField(max_length=50)
    date_off = models.IntegerField(null=True)
    set_hours_work = models.FloatField(null=True)

    def __str__(self):
        return f"{self.tool_date_id}"


class ToolDateDetails(models.Model):
    tool_date_details_id = models.AutoField(primary_key=True)
    tool_date = models.ForeignKey(ToolDate, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    extra_hours = models.FloatField()
    time_out = models.FloatField()
    
    def __str__(self):
        return self.name
