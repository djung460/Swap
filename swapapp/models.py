# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from sqlite3 import IntegrityError

from django.db import models, connection

from collections import namedtuple


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


# -------------------------------------------------------------------------------------------------------------------
# CLASSES
# -------------------------------------------------------------------------------------------------------------------
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

    @staticmethod
    def getFaculties():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT faculty "
                "FROM Class;")
            return dictfetchall(cursor=cursor)


# -------------------------------------------------------------------------------------------------------------------
# CLASSREQUIRESEQUIPMENT
# -------------------------------------------------------------------------------------------------------------------
class ClassRequiresEquipment(models.Model):
    faculty = models.CharField(primary_key=True, max_length=4)
    classnum = models.CharField(db_column='classNum', primary_key=True, max_length=4)  # Field name made lowercase.
    term = models.CharField(primary_key=True, max_length=7)
    equipmentid = models.IntegerField(db_column='equipmentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClassRequiresEquipment'
        unique_together = (('faculty', 'classnum', 'term', 'equipmentid'),)

    @staticmethod
    def get(faculty, classnum, term):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT E.equipmentid, E.equipmentname, E.equipmenttype "
                "FROM ClassRequiresEquipment CRE, Equipment E "
                "WHERE CRE.faculty=%s AND CRE.classnum=%s AND CRE.term=%s AND CRE.equipmentid=E.equipmentid ",
                [faculty, classnum, term])
            return dictfetchall(cursor=cursor)

    @staticmethod
    def getClasses(equipmentid):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT IFNULL(faculty, 'General') as faculty, classnum "
                "FROM ClassRequiresEquipment "
                "WHERE equipmentid = " + equipmentid + ";"
            )
            return dictfetchall(cursor=cursor)


# -------------------------------------------------------------------------------------------------------------------
# CONFIRMEDTRADES
# -------------------------------------------------------------------------------------------------------------------
class ConfirmedTrade(models.Model):
    tradeid = models.IntegerField(db_column='tradeID', primary_key=True)  # Field name made lowercase.
    requestusername = models.ForeignKey('Student', models.DO_NOTHING, db_column='requestUsername',
                                        related_name='%(class)s_requestUsername')  # Field name made lowercase.
    responseusername = models.ForeignKey('Student', models.DO_NOTHING, db_column='responseUsername',
                                         related_name='%(class)s_responseUsername')  # Field name made lowercase.
    requestequipid = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='requestEquipID',
                                       related_name='%(class)s_requestEquipID')  # Field name made lowercase.
    responseequipid = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='responseEquipID',
                                        related_name='%(class)s_responseEquipID')  # Field name made lowercase.
    dateconfirmed = models.DateTimeField(db_column='dateConfirmed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConfirmedTrade'

    @staticmethod
    def add(pendingtradeid, requestusername, responseusername, requestequipid, responseequipid):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ConfirmedTrade "
                "(tradeid, requestusername, responseusername, requestequipid, responseequipid, dateconfirmed) "
                "VALUES (%s,%s,%s,%s,%s,DATETIME())",
                [pendingtradeid, requestusername, responseusername, requestequipid, responseequipid])

    @staticmethod
    def getMax():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM ConfirmedTrade")
            row = cursor.fetchone()
            return row[0]

    @staticmethod
    def getMaxByUser():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) "
                "FROM ConfirmedTrade "
                "GROUP BY requestUsername "
                "HAVING COUNT(*) >= "
                "(SELECT COUNT(*) FROM ConfirmedTrade c2 GROUP BY c2.requestUsername);"
            )
            row = cursor.fetchone()
            return row[0]

    @staticmethod
    def getAvg():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT AVG(trades) "
                "FROM( "
                "SELECT COUNT(*) as trades "
                "FROM ConfirmedTrade "
                "GROUP BY requestUsername);"
            )
            row = cursor.fetchone()
            return row[0]


# -------------------------------------------------------------------------------------------------------------------
# EQUIPMENT
# -------------------------------------------------------------------------------------------------------------------
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
                "SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid GROUP BY e.equipmentid"
            )
            return dictfetchall(cursor=cursor)

    def updateSearch(keyword, type, faculty, classnum, min):
        baseQuery = "SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid WHERE e.equipmentName LIKE '%" + keyword + "%'"
        with connection.cursor() as cursor:
            if (faculty != ""):
                baseQuery += " AND c.faculty LIKE '%" + faculty + "%'"
            if (classnum != ""):
                baseQuery += " AND c.classNum LIKE '%" + classnum + "%'"
            if (type != ""):
                baseQuery += " AND e.equipmentType LIKE '%" + type + "%'"
            if (min != ""):
                baseQuery = "SELECT * FROM (" + baseQuery + " GROUP BY e.equipmentid) WHERE quantity >=" + min + ";"
                cursor.execute(baseQuery)
                return dictfetchall(cursor=cursor)
            cursor.execute(
                baseQuery + " GROUP BY e.equipmentid;"
            )
            return dictfetchall(cursor=cursor)

    @staticmethod
    def getTypes():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT equipmentType FROM Equipment;")
            return dictfetchall(cursor=cursor)

    @staticmethod
    def getMax():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM (SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum "
                "FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid GROUP BY e.equipmentid)"
                "WHERE quantity = (SELECT MAX(quantity) FROM (SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum "
                "FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid GROUP BY e.equipmentid));")

            return dictfetchall(cursor=cursor)

    @staticmethod
    def getMin():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM (SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum "
                "FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid GROUP BY e.equipmentid)"
                "WHERE quantity = (SELECT MIN(quantity) FROM (SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum "
                "FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid GROUP BY e.equipmentid));")

            return dictfetchall(cursor=cursor)

    @staticmethod
    def getAvg():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT e.equipmentID, e.equipmentName, e.equipmentType, IFNULL(SUM(s.quantity),0) as quantity, IFNULL(c.faculty,'General') as faculty, IFNULL(c.classNum,'') as classNum "
                "FROM Equipment e LEFT JOIN StudentHasEquipment s ON e.equipmentid = s.equipmentid LEFT JOIN ClassRequiresEquipment c ON e.equipmentid = c.equipmentid "
                "WHERE quantity = (SELECT MAX(s2.quantity) FROM StudentHasEquipment s2 GROUP BY s2.equipmentid ORDER BY s2.quantity DESC);")

            return dictfetchall(cursor=cursor)


# -------------------------------------------------------------------------------------------------------------------
# INSTRUCTOR
# -------------------------------------------------------------------------------------------------------------------
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
            if row is None:
                return None
            else:
                return Instructor(username=row[0], pwhash=row[1], faculty=row[2], email=row[3], name=row[4],
                                  phonenumber=row[5])

    def remove(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE Student WHERE username = %s AND pwhash = %s",
                [self.username, self.pwhash])

    def addCourse(self, faculty, classnum, term):
        """
        Adds a class to the database
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Class "
                "(faculty, classnum, term, instructorusername) "
                "VALUES (%s,%s,%s, %s)",
                [faculty, classnum, term, self.username])

    def deleteClass(self, faculty, classnum, term):
        """
        Deletes a class from the database
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Class "
                "WHERE faculty=%s AND classnum=%s AND term=%s",
                [faculty, classnum, term])

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

    def deleteEquipFromClass(self, faculty, classnum, term, equipid):
        """
        Deletes a required piece of equipment from a class
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM ClassRequiresEquipment "
                "WHERE faculty=%s AND classnum=%s AND term=%s AND equipmentid=%s",
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


    def getStudentsWithAllEquipment(self, faculty, classnum, term):
        """
        Gets a list of students with all required equipment for a class they are enrolled in
        Used by the instructor to get an overview

        Returns all students if the table is empty
        """
        with connection.cursor() as cursor:
            rows = cursor.execute(
                "SELECT * "
                "FROM Student S "
                "WHERE "
                "EXISTS (SELECT * FROM ClassRequiresEquipment CRE WHERE CRE.faculty=%s AND CRE.classnum=%s AND CRE.term=%s) "
                "AND NOT EXISTS "
                "(SELECT CRE.equipmentid "
                "FROM ClassRequiresEquipment CRE "
                "WHERE CRE.faculty=%s AND CRE.classnum=%s AND CRE.term=%s "
                "EXCEPT "
                "SELECT SHE.equipmentid "
                "FROM StudentHasEquipment SHE, StudentTakesClass STC "
                "WHERE SHE.username = S.username AND STC.faculty=%s AND STC.classnum=%s AND STC.term=%s AND STC.username=S.username)",
                [faculty, classnum, term, faculty, classnum, term, faculty, classnum, term])
            return dictfetchall(rows)


# -------------------------------------------------------------------------------------------------------------------
# PENDINGTRADES
# -------------------------------------------------------------------------------------------------------------------
class PendingTrade(models.Model):
    tradeid = models.IntegerField(db_column='tradeID', primary_key=True)  # Field name made lowercase.
    requestusername = models.CharField(db_column='requestUsername', max_length=32)  # Field name made lowercase.
    responseusername = models.CharField(db_column='responseUsername', max_length=32)  # Field name made lowercase.
    requestequipid = models.IntegerField(db_column='requestEquipID')  # Field name made lowercase.
    responseequipid = models.IntegerField(db_column='responseEquipID')  # Field name made lowercase.
    requestconfirm = models.IntegerField(db_column='requestConfirm')  # Field name made lowercase.
    responseconfirm = models.IntegerField(db_column='responseConfirm')  # Field name made lowercase.
    daterequested = models.DateTimeField(db_column='dateRequested')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PendingTrade'

    @staticmethod
    def remove(pendingtradeid):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM PendingTrade "
                "WHERE tradeid=%s",
                [pendingtradeid])

    @staticmethod
    def checkExisting(requestusername, responseusername, requestequipid, responseequipid):
        """
        :return: True if existing False otherwise
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT tradeID "
                "FROM PendingTrade "
                "WHERE (requestusername=%s OR responseusername=%s) "
                "AND (requestusername=%s OR responseusername=%s) "
                "AND (requestequipid=%s OR responseequipid=%s) "
                "AND (requestequipid=%s OR responseequipid=%s)",
                [requestusername, requestusername, responseusername, responseusername, requestequipid, requestequipid,
                 responseequipid, responseequipid])
            rows = dictfetchall(cursor)
            return len(rows) != 0


# -------------------------------------------------------------------------------------------------------------------
# STUDENT
# -------------------------------------------------------------------------------------------------------------------
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
            if row is None:
                return None
            else:
                return Student(username=row[0], pwhash=row[1], year=row[2], faculty=row[3], email=row[4], name=row[5],
                               phonenumber=row[6])

    def getOwnedEquipment(self):
        """
        Returns a list of dictionary of equipment owned by the student with username
        [{'equipmentid':1234, 'equipmentname':name, 'equipmenttype':type, 'quantity':quantity}]
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT E.equipmentid, E.equipmentname, E.equipmenttype, SHE.quantity, SHE.tradeable "
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
            try:
                cursor.execute(
                    "INSERT INTO StudentHasEquipment "
                    "(username, equipmentid, quantity, tradeable) "
                    "VALUES (%s,%s,%s,0)",
                    [self.username, equipmentid, quantity])
            except IntegrityError:
                raise IntegrityError

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

    def updateOwnedEquipment(self, equipmentid, quantity, tradeable):
        """
        Updates an equipment that a student owns
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE StudentHasEquipment "
                "SET quantity=%s, tradeable=%s "
                "WHERE username=%s AND equipmentid=%s",
                [quantity, tradeable, self.username, equipmentid])

    def remove(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE Student WHERE username = %s AND pwhash = %s",
                [self.username, self.pwhash])

    def findPossibleTrades(self):
        """
        Lists pairs of items that you want and that someone else has, and that the 2nd person wants and you have
        """
        with connection.cursor() as cursor:
            cursor.execute(
                # TODO remove pairs that are already in pendingtable and where requestusername is your username
                "SELECT DISTINCT StudentHasEquipment.equipmentID as ID1, "
                "Equipment.equipmentName as Name, "
                "StudentHasEquipment2.equipmentID as ID2, "
                "Equipment2.equipmentName as Name2, "
                "StudentHasEquipment2.username as OwnerUsername "

                "FROM "
                "StudentHasEquipment, "
                "StudentTakesClass, "
                "ClassRequiresEquipment, "
                "Equipment, "

                "StudentHasEquipment as StudentHasEquipment2, "
                "StudentTakesClass as StudentTakesClass2, "
                "ClassRequiresEquipment as ClassRequiresEquipment2, "
                "Equipment as Equipment2 "

                "WHERE StudentTakesClass.username=%s "
                "AND StudentTakesClass.faculty=ClassRequiresEquipment.faculty "
                "AND StudentTakesClass.classNum=ClassRequiresEquipment.classNum "
                "AND StudentTakesClass.term=ClassRequiresEquipment.term "
                "AND ClassRequiresEquipment.equipmentID=Equipment.equipmentID "
                "AND ClassRequiresEquipment.equipmentID=StudentHasEquipment2.equipmentID "

                "AND StudentTakesClass2.username=StudentHasEquipment2.username "
                "AND StudentTakesClass2.faculty=ClassRequiresEquipment2.faculty "
                "AND StudentTakesClass2.classNum=ClassRequiresEquipment2.classNum "
                "AND StudentTakesClass2.term=ClassRequiresEquipment2.term "
                "AND ClassRequiresEquipment2.equipmentID=Equipment2.equipmentID "
                "AND ClassRequiresEquipment2.equipmentID=StudentHasEquipment.equipmentID "

                "AND StudentHasEquipment.username=StudentTakesClass.username "
                "AND StudentHasEquipment.tradeable = 1 "
                "AND StudentHasEquipment2.tradeable = 1 "
                # Username is different
                "AND StudentTakesClass2.username <> StudentTakesClass.username "
                # Equipment is different
                "AND ClassRequiresEquipment.equipmentID <> ClassRequiresEquipment2.equipmentID "
                "AND StudentHasEquipment2.equipmentID ",
                #"NOT IN SELECT equipmentID FROM ClassRequresEquipment2 WHERE ClassRequiresEquipment2 ",
                [self.username])
            return dictfetchall(cursor=cursor)

    def addPendingTrade(self, responseusername, requestequipid, responseequipid):
        """
        Adds the chosen trade to the Pending Trade list
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO PendingTrade"
                "(requestUsername, responseUsername, requestEquipID, responseEquipID,requestConfirm,responseConfirm, dateRequested)"
                "VALUES (%s, %s, %s, %s,0,0, DATETIME())",
                [self.username, responseusername, requestequipid, responseequipid])

    def getPendingTrades(self, type):
        """
        Gets pending trades for this user
        """
        with connection.cursor() as cursor:
            if type == 'request':
                cursor.execute(
                    "SELECT PT.tradeID AS tradeID, "
                    "PT.responseConfirm AS responseConfirm, "
                    "PT.requestConfirm AS requestConfirm, "
                    "PT.responseusername AS responseUsername, "
                    "S.name AS responseName, "
                    "S.email AS responseEmail, "
                    "PT.requestequipid AS requestEquipID, "
                    "PT.responseequipid AS responseEquipID, "
                    "E1.equipmentname AS responseEquipName, "
                    "E2.equipmentname AS requestEquipName "
                    "FROM PendingTrade PT, Student S, Equipment E1, Equipment E2 "
                    "WHERE requestusername=%s "
                    "AND responseusername=S.username "
                    "AND E1.equipmentid = PT.responseequipid "
                    "AND E2.equipmentid = PT.requestequipid",
                    [self.username])
            else:
                cursor.execute(
                    "SELECT PT.tradeID AS tradeID, "
                    "PT.responseConfirm AS responseConfirm, "
                    "PT.requestConfirm AS requestConfirm, "
                    "PT.responseusername AS responseUsername, "
                    "S.name AS responseName, "
                    "S.email AS responseEmail, "
                    "PT.requestequipid AS requestEquipID, "
                    "PT.responseequipid AS responseEquipID, "
                    "E1.equipmentname AS responseEquipName, "
                    "E2.equipmentname AS requestEquipName "
                    "FROM PendingTrade PT, Student S, Equipment E1, Equipment E2 "
                    "WHERE responseusername=%s "
                    "AND requestusername=S.username "
                    "AND E1.equipmentid = PT.requestequipid "
                    "AND E2.equipmentid = PT.responseequipid",
                    [self.username])
            return dictfetchall(cursor)

    def getConfirmedTrades(self, type):
        """
        Gets confirmed trades for this user
        """
        with connection.cursor() as cursor:
            if type == 'request':
                # Confirmed trades that you've requested
                cursor.execute(
                    "SELECT  CT.tradeID AS tradeID, "
                    "CT.requestusername AS requestusername, "
                    "S.username AS responseUsername, "
                    "S.name AS responseName, "
                    "S.email AS responseEmail, "
                    "CT.requestequipid AS requestEquipID, "
                    "CT.responseequipid AS responseEquipID, "
                    "E1.equipmentname AS responseEquipName, "
                    "E2.equipmentname AS requestEquipName "
                    "FROM ConfirmedTrade CT, Student S, Equipment E1, Equipment E2 "
                    "WHERE requestusername=%s "
                    "AND responseusername=S.username "
                    "AND E1.equipmentid = CT.responseequipid "
                    "AND E2.equipmentid = CT.requestequipid",
                    [self.username])
            else:
                # Confirmed trades that you've responded to
                cursor.execute(
                    "SELECT CT.tradeID AS tradeID, "
                    "CT.requestUsername AS requestUsername, "
                    "S.name AS requestName, "
                    "S.email AS responseEmail, "
                    "CT.requestequipid AS requestEquipID, "
                    "CT.responseequipid AS responseEquipID, "
                    "E1.equipmentname AS responseEquipName, "
                    "E2.equipmentname AS requestEquipName "
                    "FROM ConfirmedTrade CT, Student S, Equipment E1, Equipment E2 "
                    "WHERE responseusername=%s "
                    "AND requestusername=S.username "
                    "AND E1.equipmentid = CT.requestequipid "
                    "AND E2.equipmentid = CT.responseequipid",
                    [self.username])
            return dictfetchall(cursor)

    def updatePendingTrade(self, tradeid, requestconfirm=None, responseconfirm=None):
        """
        updates a pending trade the chosen trade from the PendingTrade list, add it to the confirmedTrade list,
        and switch the username of the two items in userHasEquipment
        """
        with connection.cursor() as cursor:
            if requestconfirm != None:
                cursor.execute(
                    "UPDATE PendingTrade "
                    "SET requestconfirm=%s "
                    "WHERE tradeid=%s",
                    [requestconfirm, tradeid])
            elif responseconfirm != None:
                cursor.execute(
                    "UPDATE PendingTrade "
                    "SET responseconfirm=%s "
                    "WHERE tradeid=%s",
                    [responseconfirm, tradeid])

            # Return the updated row
            cursor.execute(
                "SELECT * "
                "FROM PendingTrade "
                "WHERE tradeid=%s",
                [tradeid])
            return dictfetchall(cursor)

    @staticmethod
    def remove(pendingtradeid):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM PendingTrade "
                "WHERE tradeid=%s",
                [pendingtradeid])

    @staticmethod
    def getNum():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM Student")
            return cursor.fetchone()[0]


# -------------------------------------------------------------------------------------------------------------------
# STUDENTHASEQUIPMENT
# -------------------------------------------------------------------------------------------------------------------

class StudentHasEquipment(models.Model):
    username = models.ForeignKey(Student, models.DO_NOTHING, db_column='username', primary_key=True)
    equipmentid = models.IntegerField(db_column='equipmentID', primary_key=True)  # Field name made lowercase.
    quantity = models.IntegerField()
    tradeable = models.IntegerField(db_column='tradeable')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StudentHasEquipment'
        unique_together = (('username', 'equipmentid'),)

    @staticmethod
    def getNum():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sum(quantity)"
                "FROM StudentHasEquipment;")
            return cursor.fetchone()[0]

    @staticmethod
    def getMaxNum():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sum(quantity)"
                "FROM StudentHasEquipment "
                "GROUP BY username "
                "ORDER BY sum(quantity) DESC;")
            return cursor.fetchone()[0]

    @staticmethod
    def decrementQuantity(username, equipid):
        with connection.cursor() as cursor:
            # decrement the quantity
            cursor.execute(
                "UPDATE StudentHasEquipment "
                "SET quantity= quantity - 1 "
                "WHERE username=%s AND equipmentid=%s",
                [username, equipid])
            # return the new quantity
            cursor.execute(
                "SELECT quantity "
                "FROM StudentHasEquipment "
                "WHERE username=%s AND equipmentid=%s",
                [username, equipid])
            return dictfetchall(cursor=cursor)

    @staticmethod
    def remove(username, equipid):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE "
                "FROM StudentHasEquipment "
                "WHERE username=%s AND equipmentid=%s",
                [username, equipid])

    @staticmethod
    def addOrIncrement(username, equipid):
        """
        Gives the student a new piece of equipment or increments the quantity if already owned
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * "
                "FROM StudentHasEquipment "
                "WHERE username=%s AND equipmentid=%s",
                [username, equipid])
            rows = dictfetchall(cursor)
            if len(rows) != 0:
                cursor.execute(
                    "UPDATE StudentHasEquipment "
                    "SET quantity = quantity+1 "
                    "WHERE username=%s AND equipmentid=%s",
                    [username, equipid])
            else:
                cursor.execute(
                    "INSERT INTO StudentHasEquipment "
                    "(username, equipmentid, quantity, tradeable) "
                    "VALUES(%s,%s,1,0)",
                    [username, equipid])


# -------------------------------------------------------------------------------------------------------------------
# STUDENTTAKESCLASS
# -------------------------------------------------------------------------------------------------------------------
class StudentTakesClass(models.Model):
    username = models.ForeignKey(Student, models.DO_NOTHING, db_column='username', primary_key=True)
    faculty = models.CharField(primary_key=True, max_length=4)
    classnum = models.CharField(db_column='classNum', primary_key=True, max_length=4)  # Field name made lowercase.
    term = models.CharField(primary_key=True, max_length=7)

    class Meta:
        managed = False
        db_table = 'StudentTakesClass'
        unique_together = (('username', 'faculty', 'classnum', 'term'),)

    @staticmethod
    def getEnrolled(faculty, classnum, term):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * "
                "FROM StudentTakesClass STC, Student S "
                "WHERE STC.faculty=%s AND STC.classnum=%s AND STC.term=%s AND STC.username=S.username",
                [faculty, classnum, term])
            return dictfetchall(cursor=cursor)
