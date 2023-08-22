from django.db import models


class ResultJobs(models.Model):


    class Meta:
        managed = False

    job_id = models.IntegerField()
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    link = models.URLField(max_length=200)




    


