from django.db import models
from authentication.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField

SERVICE_TYPES = [('Sunday ThanksGiving Service', 'Sunday ThanksGiving Service'),
                 ('Sunday Service', 'Sunday Service'), ('Sunday Special Service', 'Sunday Special Service'),
                 ('Tuesday Bible Study', 'Tuesday Bible Study'),
                 ('Thursday Revival Service', 'Thursday Revival Service')]

MONTHS = [('January', 'January'), ('February', 'February'), ('March', 'March'),('April', 'April'), ('May', 'May'),
          ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'),
          ('November', 'November'), ('December', 'December')]


class Service(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=255, choices=SERVICE_TYPES)
    announcement = models.TextField(max_length=255, default='Bible Study')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.FileField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.FileField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Tithe(models.Model):
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()
    month = models.CharField(max_length=15, choices=MONTHS)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, null=True, blank=True)
    transaction_date = models.CharField(max_length=15, null=True, blank=True)
    reference = models.CharField(max_length=15)

    def __int__(self):
        return self.amount


class Donation(models.Model):
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(verbose_name='email address', max_length=255, default='temi@temitopesolesi.com.ng')
    status = models.CharField(max_length=15, null=True, blank=True)
    transaction_date = models.CharField(max_length=15, null=True, blank=True)
    telephone = PhoneNumberField(null=True, unique=True, help_text='E.g. +234 803 123 4567')
    reference = models.CharField(max_length=15)

    def __int__(self):
        return self.amount


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=255)

    def __str__(self):
        return '{} created a comment'.format(self.user.get_full_name())
