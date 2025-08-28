from fastapi import FastAPI
from app import urls, model, database

# Create all tables
model.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FastAPI User Management App")

# Include your routers
app.include_router(urls.router)
