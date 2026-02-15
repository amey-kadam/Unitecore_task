A RESTful API for managing company registrations built with FastAPI and MongoDB. This API provides complete CRUD (Create, Read, Update, Delete) operations for company data with features like password hashing, duplicate validation, and pagination.

## Features

- Complete CRUD Operations - Create, Read, Update, and Delete companies
- Secure Password Hashing - Uses bcrypt for password security
- Unique Email & Mobile Validation - Prevents duplicate registrations
- Pagination Support - Efficient data retrieval with skip/limit parameters
- Clean & Simple Code - Easy to understand and maintain
- Interactive API Documentation - Auto-generated with Swagger UI

## Tech Stack

- Framework: FastAPI
- Database: MongoDB
- Password Hashing: bcrypt
- Data Validation: Pydantic
- Server: Uvicorn

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB instance)
- pip (Python package manager)

## Installation & Setup

### 1. Clone the Repository

git clone https://github.com/amey-kadam/Unitecore_task.git
cd Unitecore_task

### 2. Create Virtual Environment

**Windows:**

python -m venv venv
venv\Scripts\activate

**Linux/Mac:**

python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0

DB_NAME=company_db
```

Important: Replace the MongoDB URL with your actual connection string.

## Running the Application

uvicorn main:app --reload

The server will start at: **http://127.0.0.1:8000**

## API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

## 1. Create Company
**POST** `/companies/`

Create a new company registration.

**Request Body:**
```json
{
  "company_name": "Tech Solutions Inc.",
  "email": "contact@techsolutions.com",
  "mobile": "+1234567890",
  "address": "123 Business Street, Tech City, TC 12345",
  "password": "securePassword123"
}
```

**Response:** `201 Created`
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "company_name": "Tech Solutions Inc.",
  "email": "contact@techsolutions.com",
  "mobile": "+1234567890",
  "address": "123 Business Street, Tech City, TC 12345"
}
```

---

## 2. Get All Companies
**GET** `/companies/`

Retrieve all companies with pagination support.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 10, max: 100)

**Examples:**
- Get first 10: `/companies/`
- Get 20 per page: `/companies/?limit=20`
- Get page 2: `/companies/?skip=10&limit=10`

**Response:** `200 OK`
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "company_name": "Tech Solutions Inc.",
    "email": "contact@techsolutions.com",
    "mobile": "+1234567890",
    "address": "123 Business Street, Tech City, TC 12345"
  }
]
```

---

## 3. Get Company by ID
**GET** `/companies/{id}`

Retrieve a specific company by its ID.

**Example:** `/companies/507f1f77bcf86cd799439011`

**Response:** `200 OK` (same as create response)

**Error Responses:**
- `400 Bad Request`: Invalid company ID format
- `404 Not Found`: Company doesn't exist

---

## 4. Update Company
**PUT** `/companies/{id}`

Update company details (partial updates supported).

**Request Body:** (all fields optional)
```json
{
  "company_name": "Updated Company Name",
  "email": "newemail@example.com"
}
```

**Response:** `200 OK` (returns updated company data)

---

## 5. Delete Company
**DELETE** `/companies/{id}`

Delete a company by ID.

**Response:** `204 No Content`

**Error Responses:**
- `400 Bad Request`: Invalid company ID format
- `404 Not Found`: Company doesn't exist

---

## 6. Health Check
**GET** `/health`

Check if the server and database are running.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "message": "Server is running",
  "mongo_url_loaded": true,
  "db_name": "company_db"
}
```

## Testing

Use any of these tools to test the API:

1. **Swagger UI** (built-in): http://127.0.0.1:8000/docs
2. **Postman**: Import the endpoints and test