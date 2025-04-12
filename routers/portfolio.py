# routers/portfolio.py
from fastapi import APIRouter, Path, Query, HTTPException, Depends, status, Body
from typing import List, Annotated

import models
from portfolio_data import db, get_next_id # Our "database"

# --- Essential Feature: APIRouter ---
# Helps organize endpoints into logical groups.
router = APIRouter(
    prefix="/portfolio", # All routes in this file will start with /portfolio
    tags=["Portfolio"],  # Group endpoints in the Swagger UI docs
    responses={404: {"description": "Resource not found"}} # Default response for this router
)

# --- Essential Feature: Dependency Injection ---
# A simple dependency function. In real apps, this could manage DB sessions,
# check authentication tokens, etc. FastAPI handles calling it and providing
# its return value to the path operation function.
async def get_common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """A sample dependency providing common query parameters."""
    return {"q": q, "skip": skip, "limit": limit}

# Type alias for the dependency result for cleaner type hints
CommonDeps = Annotated[dict, Depends(get_common_parameters)]

# --- Endpoint 1: Get Basic Portfolio Info ---
@router.get("/", response_model=models.PortfolioData)
async def get_portfolio_info():
    """
    Retrieve basic portfolio information (name, title, bio) and all projects.

    *   **Essential Feature:** `async def` - FastAPI supports asynchronous route handlers
        for high concurrency, especially useful for I/O-bound operations (like DB access).
    *   **Essential Feature:** `response_model` - Ensures the output matches the
        `PortfolioData` Pydantic model structure. Filters out extra data.
    """
    return db # Pydantic automatically serializes this object

# --- Endpoint 2: Get List of Projects with Query Parameters ---
@router.get("/projects", response_model=List[models.Project])
async def get_projects(
    # --- Essential Feature: Query Parameters ---
    # Optional parameters passed in the URL after '?' (e.g., /portfolio/projects?skip=0&limit=10)
    # Includes default values and validation (ge=0 means 'greater than or equal to 0').
    skip: int = Query(0, ge=0, description="Number of projects to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of projects to return (1-100)"),
    # --- Using the Dependency ---
    # common: CommonDeps # Uncomment to use the dependency if needed in logic
    ):
    """
    Retrieve a list of projects with pagination.

    *   **Essential Feature:** `Query` Parameters (`skip`, `limit`) with validation.
    *   **Essential Feature:** `response_model=List[models.Project]` - Specifies the response is a list of Project objects.
    *   **Essential Feature:** `Depends` (demonstrated via `CommonDeps` type alias, though not used in logic here) - Shows how dependencies are injected.
    """
    return db.projects[skip : skip + limit]

# --- Endpoint 3: Get a Specific Project by ID ---
@router.get("/projects/{project_id}", response_model=models.Project)
async def get_project_by_id(
    # --- Essential Feature: Path Parameters ---
    # Required parameter embedded in the URL path.
    # Includes type hinting (int) and validation (gt=0 means 'greater than 0').
    project_id: int = Path(..., gt=0, description="The ID of the project to retrieve")
    ):
    """
    Retrieve a single project by its unique ID.

    *   **Essential Feature:** `Path` Parameter (`project_id`) with validation.
    *   **Essential Feature:** Error Handling (`HTTPException`) - Used for standard HTTP errors like 'Not Found'.
    """
    project = next((p for p in db.projects if p.id == project_id), None)
    if project is None:
        # --- Essential Feature: Error Handling ---
        # FastAPI automatically handles ValidationErrors from Pydantic.
        # For other errors (like 'Not Found'), raise HTTPException.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {project_id} not found")
    return project

# --- Endpoint 4: Create a New Project ---
@router.post("/projects", response_model=models.Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    # --- Essential Feature: Request Body ---
    # Data sent by the client (usually JSON). FastAPI reads the body,
    # validates it using the Pydantic model (`ProjectCreate`), and passes
    # it as the `project_data` argument.
    project_data: models.ProjectCreate = Body(..., embed=True) # 'embed=True' expects {"project_data": {...}}
    # Alternatively, without embed=True: project_data: models.ProjectCreate
    ):
    """
    Create a new project.

    *   **Essential Feature:** Request Body (`project_data: models.ProjectCreate`) - Data validation is automatic via Pydantic.
    *   **Essential Feature:** `status_code` - Sets the default HTTP status code for successful responses (201 Created).
    """
    new_id = get_next_id()
    new_project = models.Project(id=new_id, **project_data.model_dump())
    db.projects.append(new_project)
    return new_project # FastAPI serializes this using the response_model