from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.staticfiles import StaticFiles
import sqlite3
from contextlib import closing

# Initialize FastAPI app
app = FastAPI()
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# Initialize the database
def init_db():
    with closing(sqlite3.connect("phonebook.db")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                number TEXT NOT NULL
            )
            """)
            connection.commit()

init_db()

# Define Pydantic model
class Contact(BaseModel):
    name: str
    number: str

# Get all contacts
@app.get("/contacts", response_model=List[Dict[str, str]])
def get_contacts():
    with closing(sqlite3.connect("phonebook.db")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, number FROM contacts")
            contacts = [{"id": row[0], "name": row[1], "number": row[2]} for row in cursor.fetchall()]
    return contacts

# Add a new contact
@app.post("/contacts", response_model=dict)
def add_contact(contact: Contact):
    with closing(sqlite3.connect("phonebook.db")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO contacts (name, number) VALUES (?, ?)", (contact.name, contact.number))
            connection.commit()
            new_id = cursor.lastrowid
    return {"id": new_id, "name": contact.name, "number": contact.number}

# Update an existing contact
@app.put("/contacts/{contact_id}", response_model=dict)
def update_contact(contact_id: int, contact: Contact):
    with closing(sqlite3.connect("phonebook.db")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE contacts SET name = ?, number = ? WHERE id = ?", (contact.name, contact.number, contact_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Contact not found")
            connection.commit()
    return {"id": contact_id, "name": contact.name, "number": contact.number}

# Delete a contact
@app.delete("/contacts/{contact_id}", response_model=dict)
def delete_contact(contact_id: int):
    with closing(sqlite3.connect("phonebook.db")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Contact not found")
            connection.commit()
    return {"message": "Contact deleted successfully", "id": contact_id}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phonebook API!"}
