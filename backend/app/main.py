from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import users, companies, applications, notes

app = FastAPI()


# ルータ登録
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(notes.router)

