# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from routers import portfolio # Import the router we created

# --- Create FastAPI app instance ---
# Add metadata for the documentation
app = FastAPI(
    title="Simple Portfolio API",
    description="A simple API to manage portfolio data, demonstrating FastAPI features.",
    version="1.0.0",
)

# --- Essential Feature: Include Routers ---
# Mount the endpoints defined in routers/portfolio.py
app.include_router(portfolio.router)

# --- Essential Feature: Static Files ---
# Mount a directory to serve static files (like index.html, css, js)
# The path "/static" means files in the "static" directory are served under "/static" URL path.
# But we mount it at root path "/" to serve index.html directly.
# Note: This should generally come AFTER API routes if you have root ("/") API endpoints.
# However, for serving index.html at the root, we can define a specific root route first.
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Root Endpoint ---
# Redirects the base URL ("/") to the static index.html page for convenience
@app.get("/", include_in_schema=False) # Hide this redirect from API docs
async def root():
    """Redirects to the main documentation page."""
    # return RedirectResponse(url="/docs") # Option 1: Redirect to Swagger Docs
    return RedirectResponse(url="/static/index.html") # Option 2: Redirect to static HTML page


# Optional: Add other routers or middleware here if needed

# --- Running the app (using uvicorn) ---
# You would run this using the command:
# uvicorn main:app --reload
#
# --reload      : automatically restarts the server when code changes (for development)
# main          : the file main.py
# app           : the FastAPI instance created in main.py (app = FastAPI())