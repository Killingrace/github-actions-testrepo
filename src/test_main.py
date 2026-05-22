import os
import pytest
from fastapi.testclient import TestClient

# Припускаємо, що ваш код додатка знаходиться у файлі main.py
import main
from main import app

# Створюємо клієнт для тестування ендпоінтів
client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_counter_file(tmp_path, monkeypatch):
    """
    Фікстура автоматично створює тимчасову папку для кожного тесту
    та підміняє шлях до файлу лічильника.
    """
    # Створюємо шлях: /тимчасова_папка/data
    fake_counter_dir = tmp_path / "data"

    # Створюємо цю папку фізично в тимчасовій директорії РАЗОМ із батьківськими,
    # щоб додаток не падав, коли намагатиметься відкрити файл
    fake_counter_dir.mkdir(parents=True, exist_ok=True)

    # Визначаємо шлях до самого файлу
    fake_counter_file = fake_counter_dir / "counter.txt"

    # Підміняємо глобальну змінну шлях до файлу в модулі main
    monkeypatch.setattr(main, "counter_file", str(fake_counter_file))

    yield


def test_read_counter_empty():
    """Перевіряємо, що якщо файлу немає, лічильник повертає 0"""
    response = client.get("/")
    assert response.status_code == 200
    assert "counter=1" in response.text


def test_counter_increments():
    """Перевіряємо, що лічильник коректно збільшується з кожним запитом"""
    # Перший запит
    response1 = client.get("/")
    assert response1.status_code == 200
    assert "counter=1" in response1.text

    # Другий запит
    response2 = client.get("/")
    assert response2.status_code == 200
    assert "counter=2" in response2.text


def test_env_variable_displayed(monkeypatch):
    """Перевіряємо відображення змінної оточення"""
    # Тимчасово змінюємо значення змінної оточення для цього тесту
    monkeypatch.setattr(main, "myEnvVar", "Production Testing")

    response = client.get("/")
    assert response.status_code == 200
    assert "myEnvVar='Production Testing'" in response.text


def test_logo_endpoint(monkeypatch):
    """Перевіряємо ендпоінт /logo"""
    # Оскільки реального файлу image.png може не бути під час тестів,
    # підмінимо FileResponse або просто перевіримо поведінку.
    # Якщо файл існує у вашому репозиторії, цей тест пройде.

    # Для безпеки підробимо існування файлу через перевірку у FileResponse
    # або переконаємося, що він повертає статус (якщо файл лежить поруч)
    if os.path.exists("image.png"):
        response = client.get("/logo")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    else:
        # Якщо файлу немає, FastAPI поверне помилку, що є очікуваним
        with pytest.raises(RuntimeError):
            client.get("/logo")
