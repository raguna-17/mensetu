from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import users, companies, applications, notes

app = FastAPI()

origins = [os.getenv("FRONT")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE など全部OK
    allow_headers=["*"],  # Authorizationとか全部許可
)

app.include_router(users.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(notes.router)


