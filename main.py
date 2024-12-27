from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.staticfiles import StaticFiles
import sqlite3

# Initialize FastAPI app
app = FastAPI()
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# Initialize the database
def init_db():
    connection = sqlite3.connect("phonebook.db")  # Corrected `Connection` to `connection`
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number TEXT NOT NULL
    )
    """)
    connection.commit()  # Fixed misplaced `commit()`
    connection.close()

init_db()

# Define Pydantic model
class Contact(BaseModel):
    name: str
    number: str

# Get all contacts
@app.get("/contacts", response_model=List[Dict[str, str]])
def get_contacts():
    connection = sqlite3.connect("phonebook.db")
    cursor = connection.cursor()  # Fixed `connection` variable name
    cursor.execute("SELECT id, name, number FROM contacts")
    contacts = [{"id": row[0], "name": row[1], "number": row[2]} for row in cursor.fetchall()]
    connection.close()
    return contacts

# Add a new contact
@app.post("/contacts", response_model=dict)
def add_contact(contact: Contact):  # Added missing `contact` parameter
    connection = sqlite3.connect("phonebook.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO contacts (name, number) VALUES (?, ?)", (contact.name, contact.number))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return {"id": new_id, "name": contact.name, "number": contact.number}

# Update an existing contact
@app.put("/contacts/{contact_id}", response_model=dict)
def update_contact(contact_id: int, contact: Contact):  # Fixed `contact` capitalization and type
    connection = sqlite3.connect("phonebook.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE contacts SET name = ?, number = ? WHERE id = ?", (contact.name, contact.number, contact_id))
    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Contact not found")
    connection.commit()
    connection.close()
    return {"id": contact_id, "name": contact.name, "number": contact.number}

# Delete a contact
@app.delete("/contacts/{contact_id}", response_model=dict)
def delete_contact(contact_id: int):
    connection = sqlite3.connect("phonebook.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Contact not found")
    connection.commit()
    connection.close()
    return {"message": "Contact deleted successfully", "id": contact_id}
@app.get("/")
def read_root():
    return {"message": "Welcome to the Phonebook API!"}

