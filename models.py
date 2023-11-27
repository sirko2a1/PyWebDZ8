from mongoengine import Document, StringField, DateField, ListField, ReferenceField, BooleanField

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=2)
    quote = StringField()

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
    meta = {'auto_create_index': False}

