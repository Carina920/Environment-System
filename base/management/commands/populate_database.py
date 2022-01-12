from django.core.management.base import BaseCommand
from base import models
from django.conf import settings
from os import path

class Command(BaseCommand):
    help = 'populate database with predefined csv files'
    
    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        
        file_path = path.join(base_dir, 'raw_data', 'location.csv')
        with open(file_path, 'r') as file:
            rows = file.readlines()[1:]

            for row in rows:
                content = row.strip().split(',')
                models.Location.objects.create(city = content[0], state = content[1])
            
            self.stdout.write("imported location data")

        file_path = path.join(base_dir, 'raw_data', 'weathertype.csv')
        with open(file_path, 'r') as file:
            rows = file.readlines()[1:]

            for row in rows:
                row = row.strip()
                models.Weathertype.objects.create(typename = row)
            
            self.stdout.write("imported weathertype data")
            
        file_path = path.join(base_dir, 'raw_data', 'event.csv')
        with open(file_path, 'r') as file:
            rows = file.readlines()[1:]

            for row in rows:
                content = row.strip().split(',')
                w = models.Weathertype.objects.get(id=int(content[0]))
                l = models.Location.objects.get(id=int(content[1]))
                models.Event.objects.create(weathertypeid = w, locationid = l, eventdate = content[2], severity = content[3])
            
            self.stdout.write("imported event data")

        file_path = path.join(base_dir, 'raw_data', 'auth_user.csv')
        with open(file_path, 'r') as file:
            rows = file.readlines()[1:]

            for row in rows:
                content = row.strip().split(',')
                models.User.objects.create_user(username = content[0], password = content[1])
            
            self.stdout.write("imported auth_user data")

        file_path = path.join(base_dir, 'raw_data', 'userprofile.csv')
        with open(file_path, 'r') as file:
            rows = file.readlines()[1:]

            for row in rows:
                content = row.strip().split(',')
                p = models.Userprofile.objects.get(userid=int(content[0])) 
                p.name = content[1]
                p.timezone = content[2]
                p.locationid = models.Location.objects.get(id=int(content[3]))    
                p.save()
            
            self.stdout.write("imported userprofile data")

        file_path = path.join(base_dir, 'raw_data', 'usersearchhistory.csv')
        with open(file_path, 'r') as file:
            rows = file.readlines()[1:]

            for row in rows:
                content = row.strip().split(',')
                u = models.User.objects.get(id=int(content[0]))
                e = models.Event.objects.get(id=int(content[1]))
                models.Usersearchhistory.objects.create(userid = u, eventid = e, searcheddate = content[2])
            
            self.stdout.write("imported usersearchhistory data")