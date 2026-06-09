# Inventory Management System API

A secure, high-performance REST API for managing product inventories and user authentication. Built with Python using **FastAPI**, **SQLAlchemy ORM**, and **MySQL**.

---

## 🚀 Features

* **User Management:** Secure user registration and hashed password storage using `bcrypt`.
* **JWT Authentication:** OAuth2 password bearer token authentication flow.
* **Inventory Control:** Full CRUD operations for managing products (Name, Category, Price, Quantity).
* **Automated Documentation:** Interactive API playground generated via Swagger UI.
* **Fail-Fast Configuration:** Schema validation for environment variables using Pydantic v2.

---

## 📂 Project Structure

```text
Inventory_project/
│
├── main.py                 # Application entry point & router registration
├── .env                    # Local environment variables (Secret keys, DB URLs)
├── README.md               # Documentation
│
└── app/                    # Main application package
    ├── __init__.py         # Marks folder as a Python module
    ├── config.py           # Pydantic environment configuration
    ├── database.py         # SQLAlchemy connection and session engine
    ├── models.py           # SQLAlchemy database tables (Users, Products)
    ├── schemas.py          # Pydantic data validation schemas
    ├── utils.py            # Password hashing functions
    └── routers/            # API Route controllers
        ├── auth.py         # Login endpoint
        ├── users.py        # User endpoints
        └── products.py     # Product endpoints