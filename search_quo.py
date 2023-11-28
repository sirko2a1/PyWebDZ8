import re
from mongoengine import connect
from models import Quote, Author

def search_quotes(command):
    command_pattern = re.compile(r"^(name|tag|tags|exit):(.+)$", re.IGNORECASE)
    match = command_pattern.match(command)

    if not match:
        if command.lower() == "exit":
            return None
        else:
            return "Invalid command format."

    action, value = match.groups()

    if action == "name":
        author = Author.objects(fullname=value).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes if quotes else "No quotes found for the specified author."
        else:
            return "Author not found."

    elif action == "tag":
        quotes = Quote.objects(tags=value)
        return quotes if quotes else "No quotes found for the specified tag."

    elif action == "tags":
        tags = value.split(",")
        quotes = Quote.objects(tags__in=tags)
        return quotes if quotes else "No quotes found for the specified tags."

    elif action == "exit":
        return None

if __name__ == "__main__":
    connect("oleksander", host="mongodb+srv://olek:09093@oleksander.rvqf6dc.mongodb.net/")

    while True:
        user_input = input("Введіть команду (приклад: tag:world): ")
        result = search_quotes(user_input)
        
        if result is None:
            print("Exiting.")
            break
        elif isinstance(result, str):
            print(result)
        else:
            for quote in result:
                print(f"{quote.author.fullname}: {quote.quote}")

#done