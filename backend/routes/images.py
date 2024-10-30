from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from src.models import Image
from sqlalchemy.orm import Session, sessionmaker
from db import engine
import shutil
from fastapi.responses import FileResponse
import os
from PIL import Image as PILImage

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@router.post("/upload/")
async def upload_image(user_id: str = Form(...), file: UploadFile = File(...)):
    db: Session = SessionLocal()
    try:
        # Проверка MIME-типа файла
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid MIME type. Only JPEG and PNG are allowed.")
        
        # Проверка формата файла с помощью Pillow
        try:
            pil_image = PILImage.open(file.file)
            if pil_image.format not in ["JPEG", "PNG"]:
                raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")
            
            # Перемотка указателя файла к началу, так как Pillow считывает часть данных
            file.file.seek(0)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file.")
        
        # Убедимся, что директория существует
        directory = "static/images/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = f"{directory}{file.filename}"
        
        # Сохранение файла
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Сохранение информации в БД
        image = Image(filename=file.filename, path=filepath, user_id=user_id)
        db.add(image)
        db.commit()
        db.refresh(image)
        
        return {"filename": file.filename, "path": filepath}
    finally:
        db.close()

@router.get("/download/{image_id}")
async def download_image(image_id: int):
    # Создание сессии
    db: Session = SessionLocal()
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(image.path)
    finally:
        db.close()  # Закрываем сессию после использования

@router.get('/images/')
async def get_images():
    db: Session = SessionLocal()
    try:
        # Запрашиваем все изображения из базы данных
        images = db.query(Image).all()
        
        # Форматируем данные для возврата
        return [{
            "id": image.id,
            "filename": image.filename,
            "user_id": image.user_id,
            "path": f"http://localhost:8000/download/{image.id}"  # Формируем путь для доступа к изображению
        } for image in images]
    finally:
        db.close() 