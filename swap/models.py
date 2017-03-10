# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Class(models.Model):
    faculty = models.CharField(primary_key=True, max_length=4)
    classnum = models.CharField(db_column='classNum', primary_key=True, max_length=4)  # Field name made lowercase.
    term = models.CharField(primary_key=True, max_length=7)
    instructorusername = models.ForeignKey('Instructor', models.DO_NOTHING, db_column='instructorUsername')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'
        unique_together = (('faculty', 'classnum', 'term'),)


class ClassRequiresEquipment(models.Model):
    faculty = models.CharField(primary_key=True, max_length=4)
    classnum = models.CharField(db_column='classNum', primary_key=True, max_length=4)  # Field name made lowercase.
    term = models.CharField(primary_key=True, max_length=7)
    equipmentid = models.IntegerField(db_column='equipmentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClassRequiresEquipment'
        unique_together = (('faculty', 'classnum', 'term', 'equipmentid'),)


class ConfirmedTrade(models.Model):
    tradeid = models.IntegerField(db_column='tradeID', primary_key=True)  # Field name made lowercase.
    requestusername = models.ForeignKey('Student', models.DO_NOTHING, db_column='requestUsername')  # Field name made lowercase.
    responseusername = models.ForeignKey('Student', models.DO_NOTHING, db_column='responseUsername')  # Field name made lowercase.
    requestequipid = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='requestEquipID')  # Field name made lowercase.
    reponseequipid = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='reponseEquipID')  # Field name made lowercase.
    dateconfirmed = models.DateTimeField(db_column='dateConfirmed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConfirmedTrade'


class Equipment(models.Model):
    equipmentid = models.IntegerField(db_column='equipmentID', primary_key=True)  # Field name made lowercase.
    equipmentname = models.CharField(db_column='equipmentName', max_length=128)  # Field name made lowercase.
    equipmenttype = models.CharField(db_column='equipmentType', max_length=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Equipment'


class Instructor(models.Model):
    username = models.CharField(primary_key=True, max_length=32)
    faculty = models.CharField(max_length=4)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=12)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Instructor'


class PendingTrade(models.Model):
    tradeid = models.IntegerField(db_column='tradeID', primary_key=True)  # Field name made lowercase.
    requestusername = models.CharField(db_column='requestUsername', max_length=32)  # Field name made lowercase.
    responseusername = models.CharField(db_column='responseUsername', max_length=32)  # Field name made lowercase.
    requestequipid = models.IntegerField(db_column='requestEquipID')  # Field name made lowercase.
    responseequipid = models.IntegerField(db_column='responseEquipID')  # Field name made lowercase.
    daterequested = models.DateTimeField(db_column='dateRequested')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PendingTrade'


class Student(models.Model):
    username = models.CharField(primary_key=True, max_length=32)
    year = models.IntegerField()
    faculty = models.CharField(max_length=4)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=12)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student'


class StudentHasEquipment(models.Model):
    username = models.ForeignKey(Student, models.DO_NOTHING, db_column='username', primary_key=True)
    equipmentid = models.IntegerField(db_column='equipmentID', primary_key=True)  # Field name made lowercase.
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'StudentHasEquipment'
        unique_together = (('username', 'equipmentid'),)


class StudentTakesClass(models.Model):
    username = models.ForeignKey(Student, models.DO_NOTHING, db_column='username', primary_key=True)
    faculty = models.CharField(primary_key=True, max_length=4)
    classnum = models.CharField(db_column='classNum', primary_key=True, max_length=4)  # Field name made lowercase.
    term = models.CharField(primary_key=True, max_length=7)

    class Meta:
        managed = False
        db_table = 'StudentTakesClass'
        unique_together = (('username', 'faculty', 'classnum', 'term'),)
