import pika
from time import sleep
from mongoengine import connect
from models import Contact
from bson import ObjectId
import json


def send_email_to_contact(contact_id):
    print(f"Email надіслано на контакт з ID: {contact_id}")
    sleep(1)

    contact = Contact.objects(id=ObjectId(contact_id)).first()
    if contact:
        contact.message_sent = True
        contact.save()

def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode("utf-8"))
        contact_id = message.get("contact_id")
        
        if contact_id:
            send_email_to_contact(contact_id)
        else:
            print("Отримано невалідний contact_id")
    except json.JSONDecodeError as e:
        print(f"Помилка декодування повідомлення: {str(e)}")

if __name__ == "__main__":
    connect("oleksander", host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='contacts')

    channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

    print(' [*] Очікування повідомлень. Для виходу натисніть CTRL+C')
    channel.start_consuming()
