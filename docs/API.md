Документация API Aurea
Базовый URL: https://api.aurea.com/v1

Аутентификация
Большинство эндпоинтов требуют JWT-токен в заголовке Authorization.
Authorization: Bearer <your_jwt_token>

Основные эндпоинты
Товары
GET /products — Получить список товаров (с пагинацией и фильтрами).

GET /products/{id} — Получить информацию о конкретном товаре.

GET /categories — Получить список категорий.

Пользователи
POST /auth/register — Регистрация нового пользователя.

POST /auth/login — Вход в систему.

GET /users/profile — Получить профиль текущего пользователя.

Заказы
POST /orders — Создать новый заказ.

GET /orders — Получить историю заказов пользователя.

GET /orders/{id} — Получить детали заказа.