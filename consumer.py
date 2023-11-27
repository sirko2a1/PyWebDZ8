import pika
from time import sleep
from mongoengine import connect, Document, StringField, BooleanField
import json


connect("oleksander", host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()
    print(f"Consumer: Email надіслано на контакт {contact_id}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue', durable=True)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='contacts_queue', on_message_callback=callback)

print("Consumer: Очікуємо повідомлень. Для виходу натисніть Ctrl+C")
channel.start_consuming()
