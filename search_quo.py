from mongoengine import connect
from models import Quote, Author

def search_quotes(command):
    if command.startswith("name:"):
        author_name = command.split(":", 1)[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
        else:
            return "Author not found."

    elif command.startswith("tag:"):
        tag = command.split(":", 1)[1].strip()
        quotes = Quote.objects(tags=tag)
        return quotes

    elif command.startswith("tags:"):
        tags = command.split(":", 1)[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
        return quotes

    elif command.lower() == "exit":
        return None

    else:
        return "Invalid command."

if __name__ == "__main__":
    connect("your_db_name", host="your_mongodb_atlas_uri")

    while True:
        user_input = input("Enter command: ")
        result = search_quotes(user_input)
        
        if result is None:
            print("Exiting.")
            break
        elif isinstance(result, str):
            print(result)
        else:
            for quote in result:
                print(f"{quote.author.fullname}: {quote.quote}")

