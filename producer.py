import json
import pika
from faker import Faker
from mongoengine import connect
from models import Contact
from bson import ObjectId


def generate_contact_id(contact_data):
    return str(ObjectId(contact_data.get("full_name", "")))

def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []

    for _ in range(num_contacts):
        contact_data = {
            "full_name": fake.name(),
            "email": fake.email(),
            "message_sent": False
        }
        contacts.append(contact_data)

    return contacts

def save_contacts_to_db(contacts):
    for contact_data in contacts:
        contact = Contact(**contact_data)
        contact.save()

def publish_contacts_to_queue(fake_contacts, channel):
    for contact_data in fake_contacts:
        contact_id = contact_data.get("_id", "")
        message = {
            "contact_id": contact_id,
            "contact_data": contact_data
        }
        channel.basic_publish(
            exchange='', routing_key='contact', body=json.dumps(message)
        )
        print(f"ID контакту: {contact_id} надіслано.")
        


if __name__ == "__main__":
    connect("oleksander", host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

    num_fake_contacts = 5
    fake_contacts = generate_fake_contacts(num_fake_contacts)

    save_contacts_to_db(fake_contacts)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='contact')

    publish_contacts_to_queue(fake_contacts, channel)

    connection.close()
