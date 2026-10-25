import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Connection settings come from environment variables (no passwords in code)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "cats_db")

TEST_CATS = [
    {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
    {"name": "murzik", "age": 5, "features": ["любить рибу", "сірий"]},
    {"name": "lizzy", "age": 1, "features": ["грайлива", "біла"]},
]


def get_collection():
    """Connect to MongoDB and return the cats collection"""
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # fails fast if MongoDB is unavailable
    return client[DB_NAME]["cats"]


def print_cat(cat):
    """Print one cat document"""
    print(f"{cat['_id']} | {cat['name']}, {cat['age']} y.o. | {', '.join(cat['features'])}")


def seed_cats(collection):
    """Fill the collection with test cats (skips names that already exist)"""
    added = 0
    for cat in TEST_CATS:
        if not collection.find_one({"name": cat["name"]}):
            collection.insert_one(dict(cat))  # copy, so _id is not written into TEST_CATS
            added += 1
    print(f"Added {added} test cats")


def show_all_cats(collection):
    """Read: print all documents from the collection"""
    cats = list(collection.find())
    if not cats:
        print("Collection is empty")
    for cat in cats:
        print_cat(cat)


def show_cat(collection, name):
    """Read: print the cat with the given name"""
    cat = collection.find_one({"name": name})
    if cat:
        print_cat(cat)
    else:
        print(f"Cat '{name}' not found")


def update_age(collection, name, age):
    """Update: set a new age for the cat with the given name"""
    result = collection.update_one({"name": name}, {"$set": {"age": age}})
    if result.matched_count:
        print(f"Age of '{name}' updated to {age}")
    else:
        print(f"Cat '{name}' not found")


def add_feature(collection, name, feature):
    """Update: add a new feature to the cat's features list"""
    result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if not result.matched_count:
        print(f"Cat '{name}' not found")
    elif result.modified_count:
        print(f"Feature '{feature}' added to '{name}'")
    else:
        print(f"'{name}' already has feature '{feature}'")


def delete_cat(collection, name):
    """Delete: remove the cat with the given name"""
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Cat '{name}' deleted")
    else:
        print(f"Cat '{name}' not found")


def delete_all_cats(collection):
    """Delete: remove all documents from the collection"""
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} cats")


MENU = """
1. Show all cats
2. Find cat by name
3. Update cat age
4. Add feature to cat
5. Delete cat by name
6. Delete all cats
7. Add test cats
0. Exit"""


def main():
    try:
        collection = get_collection()
    except PyMongoError as e:
        print(f"Cannot connect to MongoDB: {e}")
        return

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                show_all_cats(collection)
            elif choice == "2":
                show_cat(collection, input("Cat name: ").strip())
            elif choice == "3":
                name = input("Cat name: ").strip()
                age = input("New age: ").strip()
                if age.isdigit():
                    update_age(collection, name, int(age))
                else:
                    print("Age must be a non-negative integer")
            elif choice == "4":
                add_feature(collection, input("Cat name: ").strip(), input("New feature: ").strip())
            elif choice == "5":
                delete_cat(collection, input("Cat name: ").strip())
            elif choice == "6":
                if input("Delete ALL cats? (y/n): ").strip().lower() == "y":
                    delete_all_cats(collection)
            elif choice == "7":
                seed_cats(collection)
            elif choice == "0":
                break
            else:
                print("Unknown option")
        except PyMongoError as e:
            print(f"Database error: {e}")


if __name__ == "__main__":
    main()
