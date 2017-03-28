# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models, connection

from collections import namedtuple


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


class Class(models.Model):
    faculty = models.CharField(primary_key=True, max_length=4)
    classnum = models.CharField(db_column='classNum', primary_key=True, max_length=4)  # Field name made lowercase.
    term = models.CharField(primary_key=True, max_length=7)
    instructorusername = models.ForeignKey('Instructor', models.DO_NOTHING,
                                           db_column='instructorUsername')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'
        unique_together = (('faculty', 'classnum', 'term'),)

    @staticmethod
    def getAll():
        """
        Returns a list of classes
        [{'faculty':APSC, 'classnum':100, 'term':W2014T1, 'instructorusername':username, 'instructorname':name}]
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT C.faculty, C.classnum, C.term, C.instructorusername, I.name "
                "FROM Class C, Instructor I "
                "WHERE C.instructorusername = I.username")
            return dictfetchall(cursor=cursor)


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
    requestusername = models.ForeignKey('Student', models.DO_NOTHING, db_column='requestUsername',
                                        related_name='%(class)s_requestUsername')  # Field name made lowercase.
    responseusername = models.ForeignKey('Student', models.DO_NOTHING, db_column='responseUsername',
                                         related_name='%(class)s_responseUsername')  # Field name made lowercase.
    requestequipid = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='requestEquipID',
                                       related_name='%(class)s_requestEquipID')  # Field name made lowercase.
    reponseequipid = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='reponseEquipID',
                                       related_name='%(class)s_responseEquipID')  # Field name made lowercase.
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

    @staticmethod
    def getAll():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT e.equipmentID, e.equipmentName, e.equipmentType, s.quantity FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid GROUP BY e.equipmentid")
            return dictfetchall(cursor=cursor)

    def updateSearch(keyword, type, faculty, classnum):

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT e.equipmentID, e.equipmentName, e.equipmentType, s.quantity FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid WHERE e.equipmentName LIKE '%" + keyword + "%' GROUP BY e.equipmentid")



class Instructor(models.Model):
    username = models.CharField(primary_key=True, max_length=32)
    pwhash = models.TextField()  # This field type is a guess.
    faculty = models.CharField(max_length=4)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=12)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Instructor'

    def insert(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Instructor (username, pwhash, faculty, email, name, phonenumber) VALUES (%s,%s,%s,%s,%s,%s)",
                (self.username, self.pwhash, self.faculty, self.email, self.name, self.phonenumber))

    def update(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Student SET (username, year, faculty, email, name, phonenumber) VALUES (%s,%s,%s,%s,%s)",
                [self.username, self.faculty, self.email, self.name, self.phonenumber])

    def get(username):
        with connection.cursor() as cursor:
            print(username)
            cursor.execute(
                "SELECT * FROM Instructor WHERE username = %s", [username])
            row = cursor.fetchone()
        return Instructor(username=row[0], pwhash=row[1], faculty=row[2], email=row[3], name=row[4],
                          phonenumber=row[5])

    def remove(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE Student WHERE username = %s AND pwhash = %s",
                [self.username, self.pwhash])

    def addCourse(self, faculty, classnum, term):
        """
        Adds a course to the database
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Class "
                "(faculty, classnum, term, instructorusername) "
                "VALUES (%s,%s,%s, %s)",
                [faculty, classnum, term, self.username])

    def addEquipToClass(self, faculty, classnum, term, equipid):
        """
        Adds a requipred piece of equipment to a class
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ClassRequiresEquipment "
                "(faculty, classnum, term, equipmentid) "
                "VALUES (%s,%s,%s, %s)",
                [faculty, classnum, term, equipid])

    def getClasses(self):
        """
        Gets the classes taught by the instructor
        """
        with connection.cursor() as cursor:
            rows = cursor.execute(
                "SELECT faculty, classnum, term "
                "FROM Class "
                "WHERE instructorusername = %s",
                [self.username])
            return dictfetchall(rows)


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
    pwhash = models.TextField()  # This field type is a guess.
    year = models.IntegerField()
    faculty = models.CharField(max_length=4)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=12)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student'

    def insert(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Student (username, pwhash, year, faculty, email, name, phonenumber) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (self.username, self.pwhash, self.year, self.faculty, self.email, self.name, self.phonenumber))

    def update(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Student SET (username, year, faculty, email, name, phonenumber) VALUES (%s,%s,%s,%s,%s)",
                [self.username, self.year, self.faculty, self.email, self.name, self.phonenumber])

    def get(username):
        with connection.cursor() as cursor:
            print(username)
            cursor.execute(
                "SELECT * FROM Student WHERE username = %s", [username])
            row = cursor.fetchone()
        return Student(username=row[0], pwhash=row[1], year=row[2], faculty=row[3], email=row[4], name=row[5],
                       phonenumber=row[6])

    def getOwnedEquipment(self):
        """
        Returns a list of dictionary of equipment owned by the student with username
        [{'equipmentid':1234, 'equipmentname':name, 'equipmenttype':type, 'quantity':quantity}]
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT E.equipmentid, E.equipmentname, E.equipmenttype, SHE.quantity "
                "FROM Student S, StudentHasEquipment SHE, Equipment E "
                "WHERE S.username = SHE.username AND S.username = %s AND SHE.equipmentid = E.equipmentid",
                [self.username])
            return dictfetchall(cursor=cursor)

    def getEnrolled(self):
        """
        Returns a list of dictionary of equipment owned by the student with username
        [{'equipmentid':1234, 'equipmentname':name, 'equipmenttype':type, 'quantity':quantity}]
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT STC.faculty, STC.classnum, STC.term "
                "FROM Student S, StudentTakesClass STC "
                "WHERE S.username = STC.username AND S.username = %s",
                [self.username])
            return dictfetchall(cursor=cursor)

    def addOwnEquipment(self, equipmentid, quantity):
        """
        Adds an equipment that a student owns
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO StudentHasEquipment "
                "(username, equipmentid, quantity) "
                "VALUES (%s,%s,%s)",
                [self.username, equipmentid, quantity])

    def removeEquipment(self, equipmentid):
        """
        Remove an equipment that a student owns
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM StudentHasEquipment "
                "WHERE  username = %s AND equipmentid = %s ",
                [self.username, equipmentid])

    def enroll(self, faculty, classnum, term):
        """
        Enrolls the student into a class
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO StudentTakesClass "
                "(username, faculty, classnum, term) "
                "VALUES (%s,%s,%s,%s)",
                [self.username, faculty, classnum, term])

    def drop(self, faculty, classnum, term):
        """
        Drops the student from a class
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM StudentTakesClass "
                "WHERE username=%s AND faculty=%s AND classnum=%s AND term=%s ",
                [self.username, faculty, classnum, term])

    def updateOwnedEquipment(self, equipmentid, quantity):
        """
        Updates an equipment that a student owns
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE StudentHasEquipment "
                "SET quantity=%s "
                "WHERE username=%s AND equipmentid=%s",
                [quantity,self.username, equipmentid])

    def remove(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE Student WHERE username = %s AND pwhash = %s",
                [self.username, self.pwhash])


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
