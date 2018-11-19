from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        # Validation Rules for Login Username
        if len(postData['username']) < 1:
            errors["username"] = "Username is required"
        # Validation rules for Login Password
        elif len(postData['password']) < 1:
            errors["password"] = "Password is required"
        elif not User.objects.filter(username = postData['username']):
            errors["username"] = "This account does not exist. Please register."
        else:
            user = User.objects.get(username=postData['username'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors["password"] = "Incorrect password"
        return errors

    def register_validator(self, postData):
        errors = {}
        # Validation Rules for Name
        if len(postData['name']) < 1:
            errors["name"] = "Name is required"
        elif len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"

        # Validation Rules for Username
        if len(postData['username']) < 1:
            errors["username"] = "Username is required"
        elif len(postData['username']) < 3:
            errors["username"] = "Username should be at least 3 characters"
        elif User.objects.filter(username=postData['username']):
            errors["username"] = "Username is taken. If this is you, please login."

        # Validation Rules for Password
        if len(postData['password']) < 1:
            errors["password"] = "Password is required"
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        
        # Validation Rules for Confirm Password
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Password and Password Confirmation did not match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # planned_trips ---> One to Many Relationship - One planner can plan many trips
    # joined_trips ---> Many to Many Relationship - Many attendees can attend many trips
    def __repr__(self):
        return f"<User #{self.id}: {self.name} {self.username}>"
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        # Validation Rules for Destination
        if len(postData['dest']) < 1:
            errors["dest"] = "Destination is required"

        # Validation Rules for Plan (Description)
        if len(postData['plan']) < 1:
            errors["plan"] = "Description is required"

        # Validation Rules for Trip Start Date
        if not postData['start']:
            errors['start'] = "Travel start date is required"
        elif not postData['end']:
            errors['end'] = "Travel end date is required"
        elif postData['start'] < str(datetime.now()):
            errors['start'] = "Travel dates must be in the future"
        elif postData['start'] > postData['end']:
            errors['end'] = "Travel end date must occur after the start date"
        return errors

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    plan = models.TextField(max_length=500)
    start = models.DateTimeField()
    end = models.DateTimeField()
    planner = models.ForeignKey(User, related_name="planned_trips")
    attendees = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"<Trip #{self.id}: {self.dest}, {self.plan}, from {self.start} to {self.end}>"
    objects = TripManager()
