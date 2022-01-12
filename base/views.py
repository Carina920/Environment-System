from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import connection
from datetime import date

from .models import Event, Location, Usersearchhistory, Weathertype
from .forms import EventForm, ProfileForm

# Global Variables
searchForm = None
events = None
fromSearchQuery = False


# Create your views here.
def signupPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, 'Failed to create a new account, please try it again!')

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'base/signup.html', context)
    

def loginPage(request):
    if request.user.is_authenticated:
        # if user already logged in, automatically redirect user to home page
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password do not match any existing accounts.')

    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'base/login.html', context)


def logoutCurrentUser(request):
    logout(request)
    resetGlobalVariable()

    return redirect('login')


def resetGlobalVariable():
    global events
    global searchForm
    global fromSearchQuery 

    searchForm = EventForm()
    events = Event.objects.raw("SELECT * FROM event ORDER BY eventdate DESC")[:20]
    fromSearchQuery = False


def createNewSearchHistory(request, events):
    # for now, we only add this first searched event to the database
    if (events is None or len(events) == 0):
        return

    userid = request.user.id
    eventid = events[0].id
    searcheddate = date.today().strftime("%Y-%m-%d")
    searchHistory = Usersearchhistory.objects.raw("SELECT * FROM usersearchhistory WHERE userid = %s AND eventid = %s", [userid, eventid])
    if (len(searchHistory) == 0):
        # user never search this event before, create a new entry in history table 
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO usersearchhistory (userid, eventid, searcheddate) VALUES (%s, %s, %s)", [userid, eventid, searcheddate])
    else:
        # user searched this event before, update the searched date to today        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE usersearchhistory SET searcheddate = %s WHERE id = %s", [searcheddate, searchHistory[0].id])
    

@login_required(login_url="/login")
def home(request):
    global fromSearchQuery

    if request.method == 'POST':
        if 'search' in request.POST:
            if request.POST.get('search') == 'new':
                searchQuery(request)
            elif request.POST.get('search') == 'clean':
                cleanSearchForm()
        elif 'vaguesearch' in request.POST:
            vagueSearchQuery(request)

        return redirect('home')
    else:
        if fromSearchQuery:            
            fromSearchQuery = False
        else:
            resetGlobalVariable()

        context = {'events': events, 'searchForm': searchForm}
        return render(request, 'base/home.html', context)


def searchQuery(request):
    global events   
    global searchForm 
    global fromSearchQuery
    
    weathertypeid = request.POST.get('weathertypeid')
    locationid = request.POST.get('locationid')
    eventdate_year = request.POST.get('eventdate_year')
    eventdate_month = request.POST.get('eventdate_month')
    eventdate_day = request.POST.get('eventdate_day')
    severity = request.POST.get('severity')

    # where clause for subquery
    subFilterSet = ""
    # where clause for main query
    filterSet = ""
    if (weathertypeid != 'None'):
        filterSet = "WHERE weathertypeid = {}".format(weathertypeid) if filterSet == "" else filterSet + " AND weathertypeid = {}".format(weathertypeid)

    if (severity != 'None'):
        filterSet = "WHERE severity = '{}'".format(severity) if filterSet == "" else filterSet + " AND severity = '{}'".format(severity)
    
    if (locationid != 'None'):
        filterSet = "WHERE locationid = {}".format(locationid) if filterSet == "" else filterSet + " AND locationid = {}".format(locationid)
    
    if (eventdate_year != ''):
        subFilterSet = "WHERE YEAR(EventDate) = {}".format(eventdate_year) if subFilterSet == "" else subFilterSet + " AND YEAR(eventdate) = {}".format(eventdate_year)
    
    if (eventdate_month != ''):
        subFilterSet = "WHERE MONTH(EventDate) = {}".format(eventdate_month) if subFilterSet == "" else subFilterSet + " AND MONTH(eventdate) = {}".format(eventdate_month)

    if (eventdate_day != ''):
        subFilterSet = "WHERE DAY(EventDate) = {}".format(eventdate_day) if subFilterSet == "" else subFilterSet + " AND DAY(eventdate) = {}".format(eventdate_day)

    if filterSet == "" and subFilterSet == "":
        events = Event.objects.raw("SELECT * FROM event ORDER BY eventdate DESC")[:20]
    else: 
        with connection.cursor() as cursor:
            sqlQuery = """SELECT e.id, eventdate, severity, WeatherTypeId, LocationId 
                          FROM (SELECT * FROM event {}) AS e LEFT JOIN weathertype AS w ON (e.WeatherTypeId = w.id) LEFT JOIN location AS l ON (e.LocationId = l.id) 
                          {} ORDER BY e.EventDate DESC""".format(subFilterSet, filterSet)
            cursor.execute(sqlQuery)
            
            result = cursor.fetchall()[:20]
            if (len(result) == 0):
                events = None
            else:
                events = []
                for r in result:
                    event = Event.objects.get(id=r[0])
                    events.append(event)
        
        createNewSearchHistory(request, events)

    fromSearchQuery = True
    searchForm = EventForm(request.POST)


# # list all rain events happened in January 1st, 2020
# SELECT EventDate, TypeName AS WeatherType, Severity, City, State
# FROM (SELECT * FROM event
#       WHERE EventDate = '2020-01-01') e NATURAL JOIN weathertype NATURAL JOIN location
# WHERE TypeName = 'Rain';


def vagueSearchQuery(request):
    global events  
    global searchForm 
    global fromSearchQuery   

    search = request.POST.get('vaguesearch')
    if search != None and not search.isspace():
        sqlQuery = """SELECT e.id, e.WeatherTypeId, e.LocationId, e.EventDate, e.Severity 
                      FROM event AS e LEFT JOIN weathertype AS w ON (e.WeatherTypeId = w.id) LEFT JOIN location AS l ON (e.LocationId = l.id) 
                      WHERE w.TypeName LIKE '%%{}%%' OR l.State LIKE '%%{}%%' OR l.City LIKE '%%{}%%' OR e.Severity LIKE '%%{}%%'
                      ORDER BY e.EventDate DESC""".format(search, search, search, search)

        events = Event.objects.raw(sqlQuery)[:20]
        createNewSearchHistory(request, events)
    else:
        events = Event.objects.raw("SELECT * FROM event ORDER BY eventdate DESC")[:20]
    
    fromSearchQuery = True
    searchForm = EventForm()


def cleanSearchForm():
    resetGlobalVariable()


@login_required(login_url="/login")
def profilePage(request):
    if request.method == 'POST':        
        name = request.POST.get('name')
        timezone = request.POST.get('timezone')
        locationid = request.POST.get('locationid')

        if (timezone == ''):
            timezone = 0

        with connection.cursor() as cursor:
            if (locationid == ''):
                # if user does not choose a location, we cannot update the location, because there is a foreign key constrain
                cursor.execute("UPDATE userprofile SET Name = %s, TimeZone = %s WHERE UserId = %s", [name, timezone, request.user.id])
            else:
                cursor.execute("UPDATE userprofile SET Name = %s, TimeZone = %s, LocationId = %s WHERE UserId = %s", [name, timezone, locationid, request.user.id])      

        return redirect('profile')
    
    summary = ""
    if (request.user.userprofile.locationid is not None and request.user.userprofile.locationid != ''):
        location = Location.objects.raw("SELECT * FROM location WHERE id = %s", [request.user.userprofile.locationid.id])[0]
        summary = "Based on the record in database, in {}".format(str(location))
        with connection.cursor() as cursor:
            cursor.execute("SELECT w.TypeName AS weathertype, COUNT(*) AS count \
                            FROM event AS e LEFT JOIN weathertype AS w ON (e.WeatherTypeId = w.id) \
                            WHERE e.LocationId = %s GROUP BY w.TypeName", [request.user.userprofile.locationid.id])
            counter = cursor.fetchall()
            if (len(counter) == 0):
                summary = summary + " does not have weather event record in database"
            else:
                for c in counter:
                    summary += ", {} event has happended {} times".format(c[0], c[1])   

    profileForm = ProfileForm(instance=request.user.userprofile)
    context = {'profileForm': profileForm, 'summary': summary}
    return render(request, 'base/profile.html', context)


@login_required(login_url="/login")
def searchHistoryPage(request):
    if request.method == 'POST':
        toDeleteId = request.POST.get('to_delete_id')
        if toDeleteId is None or toDeleteId == '':
            messages.warning(request, "Input cannot be empty! Try again!")
        else:
            toDeleteId = int(toDeleteId)
            searchHistory = Usersearchhistory.objects.raw("SELECT * FROM usersearchhistory WHERE id = %s", [toDeleteId])
            if (len(searchHistory) == 0):
                messages.warning(request, "Cannot find the history matching input value! Try again!")
            else:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM usersearchhistory WHERE id = %s", [toDeleteId])
                return redirect('searchhistory')
    
    searchHistory = Usersearchhistory.objects.raw("SELECT * FROM usersearchhistory WHERE UserId = %s ORDER BY SearchedDate DESC, id DESC", [request.user.id])[:20]
    history = []
    for h in searchHistory:
        details = {}
        details['id'] = h.id
        details['searcheddate'] = h.searcheddate
        details['eventdate'] = h.eventid.eventdate
        details['location'] = h.eventid.locationid
        details['weathertype'] = h.eventid.weathertypeid
        details['severity'] = h.eventid.severity
        history.append(details)

    hotSearchInThisMonth = {}
    with connection.cursor() as cursor:
        cursor.callproc('hotevent', [request.user.id])        
        hotSearch = cursor.fetchone()
        hotSearchInThisMonth['hotsearchedweather'] = hotSearch[0]
        hotSearchInThisMonth['hotsearchedweathersearchedtimes'] = hotSearch[1]
        hotSearchInThisMonth['hotsearchedstate'] = hotSearch[2]
        hotSearchInThisMonth['hotsearchedcity'] = hotSearch[3]
        hotSearchInThisMonth['hotsearchedlocationsearchedtimes'] = hotSearch[4]
        hotSearchInThisMonth['numofuserhassimilarsearchhistory'] = hotSearch[5]
        hotSearchInThisMonth['userwithsimilarsearchhistory'] = hotSearch[6]

    context = {'history': history, 'hotSearchInThisMonth': hotSearchInThisMonth}
    return render(request, 'base/search_history.html', context)
