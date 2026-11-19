# Dotin Lab Inventory Management API

An educational inventory management REST API built with Python and FastAPI as part of Dotin Lab backend engineering training.

The project is being developed incrementally throughout the internship. It currently uses in-memory storage; database persistence and a layered architecture are planned for later stages.

## Current Development Stage

**Completed:** FastAPI foundations, routing, REST API design, request validation, response models, error handling, filtering, pagination, and core inventory operations.

**Current implementation:** An in-memory product inventory API.

## Features

- List products with optional category filtering and name search.
- Paginate product results with `limit` and `skip`.
- Retrieve a product by its ID.
- Create products with server-generated IDs.
- Replace a product using `PUT`.
- Partially update a product using `PATCH`.
- Delete a product.
- Increase product stock.
- Validate request data and query parameters with Pydantic.
- Return appropriate HTTP status codes and 404 errors.

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn (through FastAPI standard dependencies)
- uv for dependency and environment management
- pytest and HTTPX for automated API tests
- MyPy for static type checking

## Project Structure

```text
.
├── src/
│   └── dotin_lab_inventory_api/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_products.py
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
```

## Getting Started

### Prerequisites

- Python 3.12 or newer
- uv

Install uv by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### Install dependencies

Clone the repository and move into the project directory:

```bash
git clone https://github.com/ARKN11/dotin-lab-inventory-api.git
cd dotin-lab-inventory-api
```

Install the project and its development dependencies:

```bash
uv sync --group dev
```

### Run the API

```bash
uv run fastapi dev src/dotin_lab_inventory_api/main.py
```

The local API is available at:

- API root: http://127.0.0.1:8000/
- Interactive Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/products` | List products; supports `category`, `search`, `limit`, and `skip` |
| GET | `/products/{product_id}` | Retrieve a product |
| POST | `/products` | Create a product (201 Created) |
| PUT | `/products/{product_id}` | Replace all editable product fields |
| PATCH | `/products/{product_id}` | Partially update supplied fields |
| DELETE | `/products/{product_id}` | Delete a product (204 No Content) |
| POST | `/products/{product_id}/increase-stock` | Increase stock using the `quantity` query parameter |

### Example requests

Create a product:

```http
POST /products
Content-Type: application/json
```

```json
{
  "name": "Webcam",
  "price": 75,
  "stock": 12,
  "category": "Electronics"
}
```

Filter and paginate products:

```http
GET /products?category=electronics&search=key&limit=10&skip=0
```

Increase stock:

```http
POST /products/25/increase-stock?quantity=5
```

## Automated Tests

The repository includes API tests using pytest and FastAPI's `TestClient`.

Run the complete test suite:

```bash
uv run pytest
```

Run tests with a concise summary:

```bash
uv run pytest -q
```

The tests cover:

- Root endpoint behavior.
- Product listing, category filtering, search, and pagination.
- Query parameter validation.
- Product retrieval and 404 responses.
- Product creation and request validation.
- PUT replacement and PATCH partial updates.
- DELETE behavior and empty 204 responses.
- Stock increase and invalid quantities.

Each test receives an isolated copy of the initial in-memory product data, so test execution order does not affect results.

## Static Type Checking

The project uses MyPy to detect type inconsistencies without executing the application.

Run MyPy against the application source:

```bash
uv run mypy src/
```

The initial MyPy configuration is intentionally moderate. Type-checking strictness will be increased as the application architecture and typing practices are developed during the internship.

## Current Limitations

- Product data is stored in memory and resets when the application restarts.
- There is no database integration yet.
- Authentication and authorization are not implemented yet.
- The application has not yet been refactored into separate API, schema, service, and repository layers.
- The automated tests currently cover the API behavior; broader integration and database tests will be added as the project evolves.

These limitations are intentional at this stage of the internship and will be addressed in later development phases.

## Roadmap

Planned improvements include:

- Pydantic schema and validation refinements.
- Modular routing and layered application architecture.
- Dependency injection and centralized error handling.
- PostgreSQL integration with SQLAlchemy 2.
- Database migrations with Alembic.
- User authentication with JWT.
- Role-based authorization.
- Expanded automated test coverage and code quality tooling.

## Project Context

This repository is part of the Dotin Lab backend engineering internship learning path. The implementation is intentionally incremental: new architecture and infrastructure are introduced as their corresponding topics are covered.
