# portfolio_data.py
from models import PortfolioData, Project
from pydantic import HttpUrl

# --- In-Memory "Database" ---
# For a real application, replace this with a database connection
# (e.g., using SQLAlchemy, Tortoise ORM, databases, etc.)
# and corresponding CRUD operations.

db = PortfolioData(
    name="Alex Doe",
    title="Software Developer",
    bio="Passionate developer creating web solutions with FastAPI!",
    projects=[
        Project(id=1, title="Portfolio API", description="This very API!", technologies=["Python", "FastAPI", "Uvicorn"], url=None),
        Project(id=2, title="E-commerce Platform", description="A conceptual online store backend.", technologies=["Python", "FastAPI", "PostgreSQL", "Docker"], url=HttpUrl("https://example-store.com")),
    ]
)

# Helper to manage IDs for new projects
_next_project_id = max(p.id for p in db.projects) + 1 if db.projects else 1

def get_next_id() -> int:
    global _next_project_id
    current_id = _next_project_id
    _next_project_id += 1
    return current_id

# --- Essential Feature: Dependency Injection (Conceptual Example) ---
# We'll use a simple function dependency later, but this module acts
# like a service layer or data access layer that could be injected.
# A function like `get_db()` could return this `db` object.