from peewee import *
from creds import *

db = MySQLDatabase('ytbot', user='ytbot',passwd=passwd)

class Comments(Model):
    CommentID = CharField(20)
    TSAdded = DateTimeField()

    class Meta:
        database = db