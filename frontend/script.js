// DOM Elements
const contactList = document.getElementById("contact-list");
const addContactForm = document.getElementById("add-contact-form");
const searchInput = document.getElementById("search");

// Contacts Array (for demonstration purposes)
let contacts = [];

// Add a contact
addContactForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;

    // Add to contacts array
    contacts.push({ name, phone });
    renderContacts();

    // Clear form inputs
    addContactForm.reset();
});

// Render contacts
function renderContacts(filter = "") {
    contactList.innerHTML = "";

    const filteredContacts = contacts.filter(contact =>
        contact.name.toLowerCase().includes(filter.toLowerCase()) ||
        contact.phone.includes(filter)
    );

    filteredContacts.forEach(contact => {
        const li = document.createElement("li");
        li.innerHTML = `
            <span>${contact.name} (${contact.phone})</span>
            <button onclick="deleteContact('${contact.name}')">Delete</button>
        `;
        contactList.appendChild(li);
    });
}

// Delete a contact
function deleteContact(name) {
    contacts = contacts.filter(contact => contact.name !== name);
    renderContacts();
}

// Search functionality
searchInput.addEventListener("input", (e) => {
    renderContacts(e.target.value);
});

// Initial Render
renderContacts();
