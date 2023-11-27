import pika
from time import sleep
from mongoengine import connect
from models import Contact
import argparse


mongodb_username = "olek"
mongodb_password = "09093"
mongodb_database = "oleksander"

connect(mongodb_database, host=f"mongodb+srv://{mongodb_username}:{mongodb_password}@oleksander.rvqf6dc.mongodb.net/")


def send_email_to_contact(contact_id):
    print(f"Email sent to contact with ID: {contact_id}")
    sleep(1)

    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode("utf-8")
    send_email_to_contact(contact_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Consume messages from RabbitMQ and send emails')
    parser.add_argument('--queue', type=str, default='contacts', help='RabbitMQ queue name')
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=args.queue)

    channel.basic_consume(queue=args.queue, on_message_callback=callback, auto_ack=True)

    print(' [*] В очікуванні повідомлень. Щоб вийти - натисність CTRL+C')
    channel.start_consuming()
