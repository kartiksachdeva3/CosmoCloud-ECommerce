**CosmoCloud FastAPI E-commerce API**
This is a CosmoCloud FastAPI Assignment for an e-commerce API with CRUD operations for products and orders. The project uses MongoDB as the database.

**Features**
CRUD operations for products
Order creation with validation of available product quantity
Pagination and filtering for products
...
Prerequisites

Before you begin, ensure you have met the following requirements:

Python 3.8 or later installed
MongoDB installed and running

Getting Started
To get a local copy up and running, follow these simple steps.

Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/fastapi-ecommerce-api.git
Change into the project directory:

bash
Copy code
cd fastapi-ecommerce-api
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
.\venv\Scripts\activate
On macOS and Linux:

bash
Copy code
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configuration
Open the .env file and configure the MongoDB connection URI:

ini
Copy code
MONGODB_URI=mongodb://localhost:27017/your_database_name
Replace your_database_name with the desired database name.

Running the Application
Run the FastAPI application:

bash
Copy code
uvicorn main:app --reload
The application will be accessible at http://127.0.0.1:8000.

**Usage**
Visit the FastAPI documentation at http://127.0.0.1:8000/docs to explore and test the API endpoints.
Use tools like httpie or curl to make HTTP requests to the API.
