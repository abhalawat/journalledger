from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    profile_photo = models.ImageField(default="default.png", upload_to='profile_photos')


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(user_did_save, sender=User)


class Book(models.Model):
    book_name = models.CharField(max_length=20, default="Bank")

    def __str__(self):
        return self.book_name


class INRTransaction(models.Model):
    user = models.CharField(max_length=10)
    debitAcc = models.ForeignKey(Book, on_delete=models.CASCADE, default=1, related_name='debitAcc')
    creditAcc = models.ForeignKey(Book, on_delete=models.CASCADE, default=1, related_name='creditAcc')
    description = models.CharField(max_length=20, default='purchase')
    dr = models.FloatField(default=0.0)
    cr = models.FloatField(default=0.0)
    dateTime = models.DateTimeField(auto_now_add=True, null=True)


class BookEntries(models.Model):
    book_name = models.CharField(max_length=20, default="Bank")
    dateTime = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=20, default='purchase')
    debit = models.IntegerField(default=0.0)
    credit = models.IntegerField(default=0.0)

    def __str__(self):
        return self.book_name
