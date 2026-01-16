# Book Service — UoW + Outbox + CDC + Kafka

Учебно-практический микросервис магазина книг, демонстрирующий архитектуру доставки доменных событий:

- атомарные транзакции
- паттерн Unit of Work
- Transactional Outbox
- CDC (Change Data Capture) через Debezium
- публикацию событий в Kafka
- запуск в Docker Compose с init-сервисами

Проект намеренно минимален по бизнес-функционалу и сфокусирован на архитектуре.

---

## Возможности сервиса

### REST API

- `POST /books` — добавить книгу
- `DELETE /books/{id}` — удалить книгу
- `GET /books` — получить список актуальных книг

### Поведение

- Добавление и удаление книги выполняются в одной транзакции
- Вместе с бизнес-операцией записывается событие в таблицу `outbox`
- Debezium читает `outbox` через WAL
- События публикуются в Kafka topic `books.events`
- Payload события — **полный снимок состояния книги**

---

## Архитектурные принципы

### Unit of Work

- `UnitOfWork` — контекстный менеджер
- Сам управляет lifecycle `session`
- Выполняет `commit / rollback`
- Предоставляет доступ к репозиториям
- Сервис **не работает с session напрямую**

### Сервисы

- Содержат только бизнес-логику
- Работают через `uow.book_repo` и `uow.outbox_repo`
- Не зависят от FastAPI и HTTP

### Outbox + CDC

- Таблица `outbox` является частью транзакции
- Нет прямых Kafka producer-ов в коде
- Публикация событий полностью вынесена в Debezium

---

## Инфраструктура

### Компоненты

- **PostgreSQL 16**
  - `wal_level=logical`
- **Kafka**
- **Zookeeper**
- **Debezium Connect**
- **init-kafka**
  - гарантирует создание topic `books.events`
- **init-connect**
  - автоматически регистрирует Debezium connector

### Почему init-сервисы

- Исключают race condition при старте
- Убирают ручные `curl` команды
- Приближают окружение к продакшену

---

## Kafka

- Один topic: `books.events`
- Типы событий:
  - `BookAdded`
  - `BookDeleted`
- Заголовок Kafka:
  - `type` — тип доменного события
- Payload:
  - JSON snapshot книги

Пример сообщения:
```json
{
  "id": 22,
  "title": "Harry Potter",
  "author": "Joanne Rowling",
  "price": 1000.0
}
```
---

## Запуск проекта

```bash
  docker compose up -d --build
```

## Проверка работы
```bash
  http://localhost:8000/docs
```

## Проверка PostgreSQL
```bash
  docker exec -it book_service_postgres psql \
  -U $POSTGRES_USER -d $POSTGRES_DB \
  -c "SELECT * FROM books ORDER BY id DESC;"
```

## Outbox
```bash
  docker exec -it book_service_postgres psql \
  -U $POSTGRES_USER -d $POSTGRES_DB \
  -c "SELECT id, event_type, payload, created_at FROM outbox ORDER BY id DESC;"
```

## Проверка Debezium
###### Ожидаемый статус - RUNNING
```bash
  curl http://localhost:8083/connectors
  curl http://localhost:8083/connectors/book-outbox-connector/status
```

## Проверка Kafka
```bash
  docker exec -it book_service_kafka \
  /usr/bin/kafka-console-consumer \
  --bootstrap-server kafka:29092 \
  --topic books.events \
  --property print.headers=true
```
```text
Пример сообщений, тут происходит добавление и удаление книги:

- id:3,type:BookAdded   {"id":3,"title":"Miro","author":"Roqq","price":100.0}
- id:4,type:BookDeleted {"id":3,"title":"Miro","author":"Roqq","price":100.0}
```
