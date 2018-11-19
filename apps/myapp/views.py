from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import datetime
from .models import User, Trip
import bcrypt

def index(request):
    if 'user_id' in request.session:
        return redirect('/travels')
    else:
        return redirect('/main')

def main(request):
    if 'user_id' in request.session:
        return redirect('/travels')
    else:
        print("MAIN: User is viewing the main login/register page")
        return render(request, 'myapp/main.html')

def login(request):
    if 'user_id' in request.session:
        return redirect('/dash')
    else:
        if request.method == "POST":
            errors = User.objects.login_validator(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.add_message(request, messages.ERROR, value, extra_tags='login')
                return redirect('/login')
            else:
                user = User.objects.get(username=request.POST['username'])
                request.session['user_id'] = user.id
                print("LOGIN: Returning user successfully logged in")
                return redirect("/travels")
        else:
            return redirect('/')

def register(request):
    if 'user_id' in request.session:
        return redirect('/travels')
    else:
        if request.method == "POST":
            errors = User.objects.register_validator(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.add_message(request, messages.ERROR, value, extra_tags="register")
                return redirect('/main')
            else:
                pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=pw_hash)
                request.session['user_id'] = user.id
                print("REGISTER: User succesfully created. Redirecting to Dashboard")
                return redirect("/travels")

def travels(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    else:
        other_trips = []
        all_trips = Trip.objects.all()
        mytrips = User.objects.get(id=request.session['user_id']).joined_trips.all()
        for trip in all_trips:
            if trip not in mytrips:
                other_trips.append(trip)
        context = {
            "user": User.objects.get(id=request.session['user_id']),
            "trips": other_trips,
            "mytrips": mytrips,
        }
        print("TRAVELS: User is viewing their travels dashboard")
        return render(request, 'myapp/travels.html', context)

def show(request, tripid):
    if 'user_id' not in request.session:
        return redirect('/main')
    else:
        trip = Trip.objects.get(id=tripid)
        trip_attendees = Trip.objects.get(id=tripid).attendees.all()
        other_attendees = []
        for attendee in trip_attendees:
            if attendee.username != trip.planner.username:
                other_attendees.append(attendee)
                
        context = {
            "user": User.objects.get(id=request.session['user_id']),
            "trip": trip,
            "attendees": trip.attendees.all(),
            "other_attendees": other_attendees,
        }
        print("SHOW: User is viewing trip details for a specific destination")
        return render(request, 'myapp/show.html', context)

def join(request, tripid):
    if 'user_id' not in request.session:
        return redirect('/main')
    else:
        trip = Trip.objects.get(id=tripid)
        trip.attendees.add(User.objects.get(id=request.session['user_id']))
        print("JOIN: User just joined a trip being planned by another user. It's been added to their schedule.")
        return redirect('/travels')

def add(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    else:
        print("ADD: User wants to add a new trip. Rendering a new page")
        return render(request, 'myapp/add.html')

def add_trip(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    else:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.add_message(request, messages.ERROR, value, extra_tags="add_trip")
            return redirect('/travels/add')
        else:
            trip = Trip.objects.create(dest=request.POST['dest'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'], planner_id=request.session['user_id'])
            trip.attendees.add(User.objects.get(id=request.session['user_id']))
            print("ADD_TRIP: User just added a new trip to the database. It was also added to their scheduled trips.")
            return redirect('/travels')

def logout(request):
    if 'user_id' not in request.session:
        return redirect("/main")
    else:
        request.session.clear()
        print("LOGOUT: User has logged out. Redirecting to Main")
        return redirect("/main")