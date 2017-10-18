import django_filters
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


#Clasificacion por su reputacion Nuevo Obsequiador reciente Obsequiador de meses Obsequiador de anos.
class UserType(models.Model):
    user_type = models.CharField(max_length=25,unique=True)
    description = models.TextField()

    def __unicode__(self):
        return unicode(self.user_type)


class UserProfile(models.Model):
    user = models.OneToOneField(User, default=None)
    type_user = models.ForeignKey(UserType, default=None, null=True)
    address = models.CharField(max_length=128, default=None, null=True)
    phone = models.CharField(max_length=20, default=None, null=True)
    avg_reputation = models.IntegerField(default=0, null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    register_date = models.DateField(default=None, null=True)
    cant_evaluaciones = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.user.username

class CategoryGift(models.Model):
    name_category = models.CharField(max_length=25,unique=True)
    state_category = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.name_category)

#Subcaterias de cada categeria
class SubcategoryGift(models.Model):
    category = models.ForeignKey(CategoryGift, default=None)
    name_subcategory = models.CharField(max_length=25,unique=True)
    state_subcategory = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.name_subcategory)

class GiftWeightType(models.Model):
    weight_type = models.CharField(max_length=2, unique=True, default=None)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.weight_type)

#Horas, dias, semanas, meses y anos
class UsedTimeType(models.Model):
    time_type = models.CharField(max_length=15,unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.time_type)

#Centimetros, metros y km
class GiftDimensionType(models.Model):
    dimension_type = models.CharField(max_length=15,unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.dimension_type)

#Nuevo, Totalmente utilizable, Se debe arreglar, Muy poco, Mucho uso, Uso medio
class GiftStateType(models.Model):
    state_type = models.CharField(max_length=20,unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.state_type)

#Recibiendo postulaciones, Obsequiandose..., Regalado, etc..
class PostStateType(models.Model):
    state_type = models.CharField(max_length=35,unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.state_type)

#Persona a persona, Seleccionado paga despacho, Despacho pagado por obsequiador, A acordador con el seleccionado
class DispatchMethod(models.Model):
    dispatch_type = models.CharField(default=None,max_length=35,unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.dispatch_type)

class RegionPost(models.Model):
    region_name = models.CharField(max_length=50, default=None)
    iso_3166_2_cl = models.CharField(max_length=5, default=None)

    def __unicode__(self):
        return unicode(self.region_name)

class ProvinciaPost(models.Model):
    region = models.ForeignKey(RegionPost, default=0)
    provincia_name = models.CharField(max_length=25, default="")

    def __unicode__(self):
        return unicode(self.provincia_name)

class ComunaPost(models.Model):
    provincia = models.ForeignKey(ProvinciaPost, default=None)
    comuna_name = models.CharField(max_length=25, default=None)

    def __unicode__(self):
        return unicode(self.comuna_name)


class Picture(models.Model):
    picture = models.ImageField(upload_to='post_pictures', blank=True)

    def __unicode__(self):
        return unicode(self.id)


class Gift(models.Model):
    category = models.ForeignKey(CategoryGift, default=None)
    subcategory = models.ForeignKey(SubcategoryGift, default=None, null=True)
    used_time_type = models.ForeignKey(UsedTimeType, default=None)
    dimension_type = models.ForeignKey(GiftDimensionType, default=None)
    state_type = models.ForeignKey(GiftStateType, default=None)
    weight_type = models.ForeignKey(GiftWeightType, default=None, null=True)
    name = models.CharField(max_length=35)
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    cant_used_time = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.id)

class Post(models.Model):
    user_post = models.ForeignKey(User, default=None)
    state_post = models.ForeignKey(PostStateType, default=None)
    region = models.ForeignKey(RegionPost, default=None)
    provincia = models.ForeignKey(ProvinciaPost, default=None, null=True)
    comuna = models.ForeignKey(ComunaPost, default=None, null=True)
    picture = models.ForeignKey(Picture)
    gift = models.ForeignKey(Gift)
    title = models.CharField(max_length=128)
    detail = models.TextField(max_length=800)
    state = models.BooleanField(default=True)
    date = models.DateField(default=datetime.today(), blank=True)
    finish_date = models.DateField(default=datetime.today(), blank=True)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    person2person_dispatch = models.BooleanField(default=False)
    pay_winner_dispatch = models.BooleanField(default=False)
    giver_pay_dispatch = models.BooleanField(default=False)
    according_to_winner_dispatch = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.user_post)

class AttemptGift(models.Model):
    post_attempt = models.ForeignKey(Post, default=None)
    start_date = models.DateField(default=datetime.today(), blank=True)
    finish_date = models.DateField(default=datetime.today(), blank=True)
    user_contacted = models.BooleanField(default=False)
    received_gift = models.BooleanField(default=False)
    process_finished = models.BooleanField(default=False)
    aborted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.id)

class Postulations(models.Model):
    post_postulation = models.ForeignKey(Post, default=None)
    user_postulation = models.ForeignKey(User, default=None)
    reason = models.TextField(blank=False, null=True)
    date = models.DateField(default=datetime.today(), blank=True)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    selected = models.BooleanField(default=False)
    winner = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.id)


class Comment(models.Model):
    user_comment = models.ForeignKey(User, default=None)
    post_comment = models.ForeignKey(Post, default=None)
    postulation_comment = models.ForeignKey(Postulations, default=None)
    text = models.TextField(max_length=500)
    date = models.DateField(default=datetime.today(), blank=True)
    select = models.BooleanField(default=True)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    state_comment = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.id)


class Notifications(models.Model):
    notified_user = models.ForeignKey(User, default=None)
    title = models.CharField(default=None, max_length=50)
    open = models.BooleanField(default=False)
    url = models.URLField(default=None)

    def __unicode__(self):
        return unicode(self.id)

