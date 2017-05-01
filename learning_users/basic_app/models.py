from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    '''
    we don't inherit as may mess up db by thinking  it has multiple instances
    of the same user

    A ForeignKey is a one-to-many relationship - ie a user could have many
    profiles. A OneToOne is, as the name implies, a one-to-one relationship - a
    user can only have one profile, which sounds more likely.

    see ManyToMany, OneToOne and ForeignKey
    '''

    user = models.OneToOneField(User)
    
    # additional
    portfolio = models.URLField(blank=True) # blank means optional
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.user.username
