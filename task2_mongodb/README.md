# Cats CRUD - MongoDB & PyMongo

- `main.py` — interactive menu with read, update and delete operations for the `cats` collection
- `requirements.txt` — Python dependencies

## Setup

Run from the `task2_mongodb` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Connection settings are read from environment variables:

| Variable | Default |
|---|---|
| `MONGO_URI` | `mongodb://localhost:27017` |
| `MONGO_DB` | `cats_db` |

Start MongoDB in Docker:

```bash
export MONGO_PASSWORD=your_password
docker run --name task-mongo -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASSWORD mongo:7
export MONGO_URI="mongodb://root:$MONGO_PASSWORD@localhost:27017"
```

For MongoDB Atlas set the connection string from the Atlas dashboard instead:

```bash
export MONGO_URI="mongodb+srv://<user>:<password>@<cluster>.mongodb.net"
```

## Run

```bash
python main.py
```

Choose `7` first to add test cats (`barsik`, `murzik`, `lizzy`), then try the other options:

1. Show all cats
2. Find cat by name
3. Update cat age
4. Add feature to cat
5. Delete cat by name
6. Delete all cats
