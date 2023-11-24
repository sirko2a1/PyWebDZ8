import json
from mongoengine import connect
from models import Author, Quote

def load_authors(file_path):
    with open(file_path, 'r') as file:
        authors_data = json.load(file)


    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

def load_quotes(file_path):
    with open(file_path, 'r') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Author.objects(fullname=author_name).first()
        if author:
            quote_data['author'] = author
            quote = Quote(**quote_data)
            quote.save()

if __name__ == "__main__":
    connect("database", host="mongodb")

    load_authors("C:\\Users\\katya\\Documents\\GitHub\\PyWebDZ8\\authors.json")
    load_quotes("C:\\Users\\katya\\Documents\\GitHub\\PyWebDZ8\\quotes.json")
