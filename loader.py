import json
from mongoengine import connect
from models import Author, Quote

connect("oleksander", host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        
    for author_data in authors_data:
        author = Author(
            fullname=author_data["fullname"],
            born_date=author_data.get("born_date"),
            born_location=author_data.get("born_location"),
            description=author_data["description"]
        )
        author.save()

def load_qoutes():
    with open('qoutes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        
    for quote_data in quotes_data:
        author_fullname = quote_data.get("author")
        author = Author.objects(fullname=author_fullname).first()

        if author:
            quote = Quote(
                tags=quote_data.get("tags", []),
                author=author,
                quote=quote_data["quote"]
            )
            quote.save()

if __name__ == "__main__":
    load_authors()
    load_qoutes()