# Book Service — Outbox + CDC + Kafka

Учебно-практический микросервис магазина книг, демонстрирующий:

- атомарные транзакции
- паттерн Transactional Outbox
- CDC (Change Data Capture) через Debezium
- публикацию доменных событий в Kafka

Проект намеренно минимален и сфокусирован на корректной архитектуре доставки событий.

---

## Возможности сервиса

REST API:

- `POST /books` — добавить книгу
- `DELETE /books/{id}` — удалить книгу
- `GET /books` — получить список актуальных книг

При добавлении или удалении книги:
1. Изменяются данные в таблице `books`
2. Событие записывается в таблицу `outbox`
3. Debezium читает `outbox` через WAL
4. Событие публикуется в Kafka topic `books.events`

---

## Архитектура

Схема потока данных и компонентов описана в файле:

👉 [`docs/flow.md`](docs/flow.md)

---

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Unit of Work
- Transactional Outbox
- Debezium
- Kafka
- Docker Compose

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

### Что намеренно не реализовано
```text
- Kafka consumer
- DLQ и retry-механизмы
- Schema Registry
- Версионирование событий
- Проект сфокусирован на Outbox + CDC как архитектурном паттерне.
```

### Назначение проекта
```text
- Проект можно использовать как:
- Учебный эталон Outbox + CDC
- Основу для расширения (consumer, projection, read-model)
- Reference-архитектуру для микросервисов
```

