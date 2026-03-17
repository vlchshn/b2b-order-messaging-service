# B2B Order Messaging Service

Asynchronous REST API service for B2B order management and real-time communication. Built with **FastAPI** and **PostgreSQL**, this service allows clients and managers to create orders and discuss them in isolated, real-time WebSocket chat rooms.

## Tech Stack

* **Language:** Python 3.11
* **Framework:** FastAPI
* **Database:** PostgreSQL (Asyncpg) + SQLAlchemy 2.0
* **Migrations:** Alembic
* **Real-time:** WebSockets
* **Authentication:** JWT (JSON Web Tokens) + bcrypt
* **Infrastructure:** Docker & Docker Compose
* **Package Manager:** Poetry

## Project Structure

```text
.
├── alembic/                # Database migrations setup and history
├── app/                    # Main application code
│   ├── api/                # API routers and dependencies (e.g., deps.py)
│   ├── core/               # App configuration, security, and WS manager
│   ├── crud/               # CRUD operations (Create, Read, Update, Delete)
│   ├── db/                 # Database connection and session setup
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic schemas for data validation
│   └── main.py             # FastAPI application entry point
├── .dockerignore           # Excluded files for Docker build context
├── .env.example            # Template for environment variables
├── .gitignore              # Excluded files for Git tracking
├── alembic.ini             # Alembic configuration
├── docker-compose.yml      # Multi-container orchestration (API, DB, Redis)
├── Dockerfile              # Instructions for building the API image
├── poetry.lock             # Exact dependency versions (deterministic build)
├── pyproject.toml          # Poetry dependencies and project metadata
├── websocket_client.html   # Internal QA diagnostic tool for WS testing
└── README.md               # Project documentation
```

## Key Features

* **JWT Authentication:** Secure user registration and login.
* **Order Management:** Creation and tracking of B2B orders.
* **Real-Time Chat:** Isolated WebSocket connections for each specific order. 
* **Role-Based Access:** (Scalable architecture ready for Client/Manager role separation).
* **Fully Containerized:** One-command deployment using Docker Compose.

## Database Architecture

The relational database is structured around three core domains:
1. `Users` - System participants (clients/managers).
2. `Orders` - Business requests linked to specific users (One-to-Many).
3. `Messages` - Chat history linked to specific orders and users (One-to-Many).

## Local Setup & Run

The project is fully dockerized. You don't need to install Python or PostgreSQL locally to run the service.

### 1. Clone the repository
```bash
git clone https://github.com/your-username/b2b-order-messaging-service.git
cd b2b-order-messaging-service
```

### 2. Environment Variables
Create a `.env` file in the root directory based on the following configuration:

```env
# Database configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=b2b_core
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/b2b_core

# Security
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run with Docker Compose
Execute the following command to build the API image, set up the database, apply Alembic migrations, and start the server:
```bash
docker compose up --build
```

### 4. Access the API
Once the containers are running, you can access the interactive API documentation:
* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc

## WebSocket Testing

To test the real-time chat functionality:
1. Authenticate via the `/login` endpoint to get your JWT token.
2. Create an order via `POST /orders`.
3. Connect to the WebSocket endpoint: `ws://localhost:8000/ws/orders/{order_id}`
4. Send messages via the API or directly through the active WebSocket connection.

---
*Developed as a demonstration of production-ready asynchronous Python backend architecture.*