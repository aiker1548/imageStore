import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from main import app
from src.models import User

client = TestClient(app)


class TestUserRegistration:
    """Тесты регистрации с моками."""
    
    @patch('routes.users.SessionLocal')
    def test_register_duplicate_username(self, mock_session):
        """Тест: регистрация с существующим username возвращает 400."""
        # Настраиваем mock
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Мокаем существующего пользователя
        existing_user = User(id=1, username="testuser", password="pass123")
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user
        
        # Отправляем запрос
        response = client.post(
            "/register/",
            json={"username": "testuser", "password": "newpass"}
        )
        
        # Проверяем результат
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already registered"
    
    @patch('routes.users.SessionLocal')
    def test_register_new_user_success(self, mock_session):
        """Тест: успешная регистрация нового пользователя."""
        # Настраиваем mock
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Мокаем что пользователя НЕ существует
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Отправляем запрос
        response = client.post(
            "/register/",
            json={"username": "newuser", "password": "newpass123"}
        )
        
        # Проверяем результат
        assert response.status_code == 200
        assert response.json()["username"] == "newuser"


class TestUserLogin:
    """Тесты логина с моками."""
    
    @patch('routes.users.SessionLocal')
    def test_login_wrong_password(self, mock_session):
        """Тест: вход с неверным паролем возвращает 400."""
        # Настраиваем mock
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Мокаем существующего пользователя с правильным паролем
        existing_user = User(id=1, username="testuser", password="correctpass")
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user
        
        # Отправляем запрос с НЕВЕРНЫМ паролем
        response = client.post(
            "/login/",
            json={"username": "testuser", "password": "wrongpass"}
        )
        
        # Проверяем результат
        assert response.status_code == 400
        assert response.json()["detail"] == "Incorrect username or password"
    
    @patch('routes.users.SessionLocal')
    def test_login_nonexistent_user(self, mock_session):
        """Тест: вход несуществующего пользователя возвращает 400."""
        # Настраиваем mock
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Мокаем что пользователя НЕ существует
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Отправляем запрос
        response = client.post(
            "/login/",
            json={"username": "nonexistent", "password": "anypass"}
        )
        
        # Проверяем результат
        assert response.status_code == 400
        assert response.json()["detail"] == "Incorrect username or password"
    
    @patch('routes.users.SessionLocal')
    def test_login_success(self, mock_session):
        """Тест: успешный вход с правильными данными."""
        # Настраиваем mock
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Мокаем существующего пользователя
        existing_user = User(id=42, username="testuser", password="correctpass")
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user
        
        # Отправляем запрос с ПРАВИЛЬНЫМ паролем
        response = client.post(
            "/login/",
            json={"username": "testuser", "password": "correctpass"}
        )
        
        # Проверяем результат
        assert response.status_code == 200
        assert response.json()["user_id"] == 42


if __name__ == '__main__':
    pytest.main([__file__, '-v'])