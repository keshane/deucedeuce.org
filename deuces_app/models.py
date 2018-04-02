#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
from django.db import models
from django.contrib.auth.models import User


class Deucer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        db_table = 'Deucer'


class Establishment(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Establishment'


class Gender(models.Model):
    name = models.CharField(primary_key=True, max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Gender'


class Rating(models.Model):
    value = models.SmallIntegerField(primary_key=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        managed = True
        db_table = 'Rating'


class Feature(models.Model):
    name = models.CharField(primary_key=True, max_length=40)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = True
        db_table = "Feature"


class Restroom(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    gender = models.ForeignKey(Gender, models.DO_NOTHING, db_column='gender')
    level = models.IntegerField()
    establishment = models.ForeignKey(Establishment, models.DO_NOTHING, db_column='establishment')
    features = models.ManyToManyField(Feature, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Restroom'
        unique_together = ("establishment", "name")


class Review(models.Model):
    deucer = models.ForeignKey(Deucer, models.DO_NOTHING, db_column='deucer')
    review = models.TextField(blank=True, null=True)
    rating = models.ForeignKey(Rating, models.DO_NOTHING, db_column='rating')
    restroom = models.ForeignKey(Restroom, models.DO_NOTHING, db_column='restroom')

    def __str__(self):
        return "{} gave {} to {}, {}".format(str(self.deucer),
                                             str(self.rating),
                                             str(self.restroom.establishment.name),
                                             str(self.restroom.name))

    class Meta:
        managed = True
        db_table = 'Review'


