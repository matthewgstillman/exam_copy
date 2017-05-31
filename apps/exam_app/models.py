from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserValidation(models.Manager):
    # validate data obtained from register form
    def register(self,postdata):
        errors =[]
        print 'inside register method'
        if User.objects.filter(email=postdata['email']):
            errors.append('Email is already registered')

        if len(postdata['first_name']) <2:
            errors.append("First name must be at least 2 characters")
        elif not NAME_REGEX.match(postdata['first_name']):
            errors.append("First name must only contain alphabet")
        #
        if len(postdata['last_name']) <2:
            errors.append("Last name must be at least 2 characters")
        elif not NAME_REGEX.match(postdata['last_name']):
            errors.append("Last name must only contain alphabet")
        #
        if len(postdata['email']) <1:
            errors.append('Email cannot be empty')
        elif not EMAIL_REGEX.match(postdata['email']):
            errors.append('Invalid email format')
        #
        if len(postdata['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif postdata["password"] != postdata['confirmpassword']:
            errors.append('Password do not match')

        if len(errors) == 0:
            # generate new salt
            salt = bcrypt.gensalt()
            # encode the password obtained from form
            password = postdata['password'].encode()
            # hash password and salt together
            hashed_pw = bcrypt.hashpw(password, salt)
            # add the new users to database
            User.objects.create(first_name=postdata['first_name'], last_name=postdata['last_name'],email=postdata['email'],password=hashed_pw)
        return errors
    def login(self,postdata):
        errors=[]
        # check if the email in the database or not
        if User.objects.filter(email=postdata['email']):
            # encode the password to a specific format since the about email is registered
            form_pw = postdata['password'].encode()
            # encode the registered user's password fro database to a specific format
            db_pw = User.objects.get(email=postdata['email']).password.encode()
            # compare the password with the password in database
            if not bcrypt.checkpw(form_pw, db_pw):
                error.append('Incorrect password')

        else:
            errors.append("Email has not been registered")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # secrets_liked - this is a method on user object that is available through the related name
    objects = UserValidation()

    def __unicode__(self):
        return "id: " + str(self.id) +", first_name: " + self.first_name+ ", last_name: " + self.last_name+ ", email: " + self.email + ", password: " + str(self.password)

class SecretManager(models.Manager):

    def create_secret(self, postData):
        errors = []
        if postData['secret'] == "":
            errors.append("No secret entered! Enter some good gossip, bruh!")
        if len(errors) == 0:
            Secret.objects.create(content=postData['secret'], user_id=postData['user_id'])
        return errors

    def like(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return (False, "This secret is not found in our database!")
        user = User.objects.get(id=userid)
        if secret.user == user:
            return (False, "You can't like your own secret, fucker!")
        secret.likers.add(user)
        return (True, "You liked this secret!")

    def deleteLike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return (False, "You fucker! You can't delete that shit!")
        user = User.objects.get(id=userid)
        if secret.user != user:
            return (False, "Fucker, that's not yours to delete!")
        secret.delete()
        return (True, "Secret deleted, bitch@ss!")


class Secret(models.Model):
    content  = models.TextField()
    user = models.ForeignKey(User, related_name="secrets")
    likers = models.ManyToManyField(User, related_name="secrets_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = SecretManager()

    def __unicode__(self):
        return "content: " + self.content + ", user_foreignkey: " + str(self.user)
    # objects = SecretManager()
