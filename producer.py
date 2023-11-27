import json
import pika
from faker import Faker
from mongoengine import connect
from models import Contact

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
        # Виключимо _id зі словника перед створенням об'єкта Contact
        contact_data.pop("_id", None)
        contact = Contact(**contact_data)
        contact.save()

def publish_contacts_to_queue(contacts, channel):
    for contact_data in contacts:
        contact_id = str(contact_data["_id"])
        channel.basic_publish(exchange='', routing_key='contacts', body=contact_id)

if __name__ == "__main__":
    try:
        db_name = "oleksander"
        connect(db_name, host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

        num_fake_contacts = 5
        fake_contacts = generate_fake_contacts(num_fake_contacts)

        save_contacts_to_db(fake_contacts)

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='contacts')

        publish_contacts_to_queue(fake_contacts, channel)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
