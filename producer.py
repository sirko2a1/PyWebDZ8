import pika
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
import json

contact_create = int(input("кількість контактв для генерації = "))

connect("oleksander", host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue', durable=True)

fake = Faker()
for _ in range(contact_create):
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='',
                          routing_key='contacts_queue',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

print("Producer: контакти створено та надіслано до черги")


connection.close()

#done