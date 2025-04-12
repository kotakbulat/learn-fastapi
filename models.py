# models.py
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

# --- Essential Feature: Pydantic Models ---
# Used for Request Body validation and Response Model definition.
# Provides automatic data validation, serialization, and documentation.

class ProjectBase(BaseModel):
    title: str = Field(..., example="My Awesome Project", min_length=3)
    description: str = Field(..., example="A description of the project.", min_length=10)
    technologies: List[str] = Field(..., example=["Python", "FastAPI", "React"])
    url: Optional[HttpUrl] = Field(None, example="https://example.com/myproject") # Using HttpUrl for validation

class ProjectCreate(ProjectBase):
    # No 'id' needed when creating
    pass

class Project(ProjectBase):
    id: int = Field(..., example=1) # 'id' is present in the response

class PortfolioData(BaseModel):
    name: str = Field(..., example="Alex Doe")
    title: str = Field(..., example="Software Developer")
    bio: str = Field(..., example="Passionate developer creating web solutions.")
    projects: List[Project] = [] # Will hold the list of projects