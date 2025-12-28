from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from src.models import User
from db import engine
from src import UserCreate, UserLogin

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.post("/register/")
async def register_user(user_data: UserCreate):
    db: Session = SessionLocal()
    try:
        # Проверка на уникальность имени пользователя
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        # Создаем нового пользователя
        user = User(username=user_data.username, password=user_data.password)
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"username": user.username}
    finally:
        db.close()  # Закрываем сессию после использования


@router.post("/login/")
async def login_user(user_data: UserLogin):
    db: Session = SessionLocal()
    try:
        # Поиск пользователя по имени
        user = db.query(User).filter(User.username == user_data.username).first()
        if user is None:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        # Проверка пароля
        if user_data.password != user.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        return {"user_id": user.id}  # Возвращаем ID пользователя
    finally:
        db.close()  # Закрываем сессию после использования