from django.db import models


class User(models.Model):
    pass

    class Meta:
        db_table = "user"


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    class Meta:
        db_table = "company"


class Job(models.Model):
    content = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    reward = models.CharField(max_length=100)
    tech_stack = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user_job = models.ManyToManyField(User)

    class Meta:
        db_table = "job"
