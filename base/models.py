from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Location(models.Model):
    state = models.CharField(max_length=16, db_column='State')  # Field name made lowercase.
    city = models.CharField(max_length=32, db_column='City')  # Field name made lowercase.

    def __str__(self):
        return "{}, {}".format(self.city, self.state)

    class Meta:
        db_table = 'location'

class Weathertype(models.Model):
    typename = models.CharField(db_column='TypeName', max_length=32, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.typename
        
    class Meta:
        db_table = 'weathertype'

class Event(models.Model):
    weathertypeid = models.ForeignKey(Weathertype, models.DO_NOTHING, db_column='WeatherTypeId')  # Field name made lowercase.
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId')  # Field name made lowercase.
    eventdate = models.DateField(db_column='EventDate', blank=True, null=True)  # Field name made lowercase.
    severity = models.CharField(db_column='Severity', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'event'

class Userprofile(models.Model):
    # we used Django build-in User model instead of creating our own. In database, the User model is called auth_user
    userid = models.OneToOneField(User, models.CASCADE, primary_key=True, db_column='UserId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    timezone = models.IntegerField(db_column='TimeZone', blank=True, null=True)  # Field name made lowercase.
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId', blank=True, null=True)  # Field name made lowercase.

    # https://blog.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield
    # https://rohitlakhotia.com/blog/django-custom-user-model/
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    @receiver(post_save, sender=User)
    def create_or_update_profile(sender, instance, created, **kwargs):
        if created:
            Userprofile.objects.create(userid=instance)

        instance.userprofile.save()
    
    class Meta:
        db_table = 'userprofile'

# if a user searched same event multiple times, the searched date will be updated to the latest search date
class Usersearchhistory(models.Model):
    # we used Django build-in User model instead of creating our own. In database, the User model is called auth_user
    userid = models.ForeignKey(User, models.CASCADE, db_column='UserId')  # Field name made lowercase.
    eventid = models.ForeignKey(Event, models.CASCADE, db_column='EventId')  # Field name made lowercase.
    searcheddate = models.DateField(db_column='SearchedDate', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return "searched eventid = {} in {}".format(self.eventid, self.searcheddate)

    class Meta:
        db_table = 'usersearchhistory'
        unique_together = ['userid', 'eventid']