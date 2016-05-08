from django.db import models
from mongoengine import *
from mongoengine import connect
# Create your models here.
connect('crawl_ganji', host='127.0.0.1', port=27017)


class ItemInfo(Document):
    title = StringField()
    pub_date = StringField()
    look = StringField()
    area = ListField(StringField())
    price = IntField()
    url = StringField()
    time = StringField()
    cates = ListField(StringField())
    meta = {'collection': 'item_infoY'}

# for i in ArtiInfo.objects[:1]:
#     print(i.title)