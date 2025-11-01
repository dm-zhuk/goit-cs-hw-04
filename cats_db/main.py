from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://dmzhuk_db_user:1rtw6pX4vl1PSbSy@cluster0.0uegaih.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi("1"),
)

db = client.cats_book
collection = db.cats

try:
    result_one = collection.insert_one(
        {
            "name": "Barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }
    )
    print(f"Додано Barsik з ID: {result_one.inserted_id}")
except Exception as e:
    print("Помилка insert_one:", e)

result_many = collection.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Luna",
            "age": 4,
            "features": ["любить коробки", "дає себе гладити", "смугастий"],
        },
        {
            "name": "Whiskers",
            "age": 9,
            "features": ["спить на клавіатурі", "не дає себе гладити", "білий"],
        },
        {
            "name": "Muffin",
            "age": 5,
            "features": ["муркоче голосно", "дає себе гладити", "чорно-білий"],
        },
        {
            "name": "Shadow",
            "age": 2,
            "features": ["грається з нитками", "не дає себе гладити", "темні лапи"],
        },
        {
            "name": "Simba",
            "age": 7,
            "features": ["боїться пилососа", "дає себе гладити", "черепаховий"],
        },
        {
            "name": "Pickles",
            "age": 1,
            "features": ["їсть огірки", "не дає себе гладити", "кремовий"],
        },
    ]
)
print(result_many.inserted_ids)


# *********************************************
# --- CRUD ФУНКЦІЇ ---
# *********************************************

# Отримання документа з колекції
barsik = collection.find_one({"name": "Barsik"})
print(barsik)

# Отримання декількох документів з колекції
result = collection.find({})
for el in result:
    print(el)

# Оновлення документа з колекції
collection.update_one({"name": "Barsik"}, {"$set": {"age": 4}})
print(collection.find_one({"name": "Barsik"}))

# Видалення документа з колекції
collection.delete_one({"name": "Barsik"})
print("Після видалення:", collection.find_one({"name": "Barsik"}))

# Очищаємо колекцію
collection.delete_many({})

# --- Закрити з'єднання ---
client.close()
print("\nЗ'єднання закрито. Готово!")
