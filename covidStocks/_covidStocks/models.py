from django.db import models

class Tweets(models.Model):
    # id = models.AutoField(primary_key=True)
    tweetID = models.DecimalField(primary_key=True,max_digits=21,decimal_places=0)
    companyID = models.ForeignKey('Company',on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField(max_length=280)
    userID = models.TextField(max_length=None)
    score = models.FloatField()
    interactions = models.IntegerField()


class Company(models.Model):
    companyID = models.AutoField(primary_key=True)
    # stockID = models.ForeignKey('ObservedStock',on_delete=models.CASCADE)
    Name = models.TextField(max_length=None)
    symbol = models.TextField(max_length=None)

class ObservedStock(models.Model):
    stockID = models.AutoField(primary_key=True)
    companyID = models.ForeignKey('Company',on_delete=models.CASCADE)
    name = models.TextField(max_length=None)
    timestamp = models.DateTimeField()
    price = models.FloatField()

class ExpectedStock(models.Model):
    derivedStockID = models.AutoField(primary_key=True)
    companyID = models.ForeignKey('Company',on_delete=models.CASCADE)
    name = models.TextField(max_length=None)
    model = models.TextField(max_length=None)
    timestamp = models.DateTimeField()
    price = models.FloatField()
