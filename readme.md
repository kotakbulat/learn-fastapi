# Simple FastAPI Portfolio API Demo

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Libraries](https://img.shields.io/badge/libraries-Pydantic%2C%20Uvicorn-orange.svg)](https://pydantic.dev/)

A simple demonstration project showcasing the essential features of the FastAPI web framework by creating a basic portfolio API.

This project serves as a hands-on example for understanding:

*   API endpoint creation (GET, POST)
*   Data validation using Pydantic
*   Path and Query parameters
*   Request and Response models
*   Dependency Injection fundamentals
*   Error Handling
*   Automatic API documentation (Swagger UI / ReDoc)
*   Serving static files
*   Basic project structuring with APIRouter

## Features

*   Retrieve overall portfolio information (name, title, bio).
*   List portfolio projects with optional pagination (skip, limit).
*   Retrieve a specific project by its ID.
*   Create a new project entry (data stored in-memory).
*   Interactive API documentation via Swagger UI and ReDoc.
*   Simple HTML landing page explaining the features.

## Tech Stack

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Data Validation & Models:** [Pydantic](https://pydantic.dev/)
*   **ASGI Server:** [Uvicorn](https://www.uvicorn.org/) (with `standard` extras for performance)
*   **Language:** Python 3.8+

## Getting Started

Follow these instructions to get the project running locally.

### Prerequisites

*   Python 3.8 or higher installed.
*   `pip` (Python package installer).
*   Git (optional, for cloning the repository).

### Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <repository-url> # Replace with the actual URL if applicable
    cd simple-portfolio-fastapi
    ```
    *If you downloaded the files, navigate to the `simple-portfolio-fastapi` directory.*

2.  **Create and activate a virtual environment (Recommended):**
    *   **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the App

Once the setup is complete, run the development server using Uvicorn:

```bash
uvicorn main:app --reload

FastAPI Features Demonstrated
This project highlights the following core FastAPI features. You can interact with them via the /docs interface:
Automatic Interactive API Docs: Generated at /docs (Swagger UI) and /redoc (ReDoc) based on your code (type hints, path operations, Pydantic models, docstrings).
Async Support: Path operation functions are defined with async def for high performance, especially for I/O-bound tasks.
Pydantic Models: Used in models.py for defining data shapes (Project, PortfolioData, etc.). FastAPI uses these for:
Request Body Validation: Incoming JSON data (e.g., in POST /portfolio/projects) is automatically parsed and validated against the ProjectCreate model. Invalid data returns a clear 422 error.
Response Models: The response_model argument in path operation decorators (@router.get(...)) ensures the output data conforms to the specified model (e.g., response_model=models.Project), filtering extraneous data and providing schema for the docs.
Data Serialization: Automatically converts Pydantic models to JSON for responses.
Path Parameters: Used in GET /portfolio/projects/{project_id}. FastAPI validates the project_id based on the type hint (int) and Path constraints (gt=0).
Query Parameters: Used in GET /portfolio/projects for pagination (skip, limit). FastAPI handles defaults and validation based on type hints and Query constraints (ge=0, le=100).
Dependency Injection: Demonstrated with the get_common_parameters function and Depends in routers/portfolio.py. Allows reusing logic (like DB connections, authentication checks) across endpoints.
Error Handling: Automatic handling of ValidationErrors from Pydantic. Explicit use of HTTPException for standard HTTP errors (e.g., 404 Not Found when a project ID doesn't exist).
APIRouter: Used in routers/portfolio.py to organize related endpoints into modules, keeping main.py clean and promoting code organization (prefix="/portfolio", tags=["Portfolio"]).
Static Files: Serving the index.html file from the static directory using StaticFiles.
Status Codes: Setting appropriate HTTP status codes for responses (e.g., status_code=status.HTTP_201_CREATED for the POST endpoint).