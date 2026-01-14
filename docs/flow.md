# Архитектура и Flow

Ниже описан полный поток обработки команд (add / delete book)  
с использованием **Unit of Work + Outbox + Debezium (CDC) + Kafka**.

---

## Sequence Diagram — Command Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client (Swagger)
    participant API as FastAPI Router
    participant Service as BookService
    participant UoW as UnitOfWork
    participant PG as PostgreSQL
    participant Outbox as Outbox table
    participant Debezium as Debezium (CDC)
    participant Kafka as Kafka (books.events)

    Client->>API: POST /books
    API->>Service: add_book()
    Service->>UoW: begin transaction
    UoW->>PG: INSERT INTO books
    UoW->>Outbox: INSERT BookAdded event
    UoW->>PG: COMMIT
    API-->>Client: 200 OK

    Debezium-->>Outbox: reads new row (CDC)
    Debezium-->>Kafka: publish BookAdded

    Client->>API: DELETE /books/{id}
    API->>Service: delete_book()
    Service->>UoW: begin transaction
    UoW->>PG: DELETE FROM books
    UoW->>Outbox: INSERT BookDeleted event
    UoW->>PG: COMMIT
    API-->>Client: 200 OK

    Debezium-->>Outbox: reads new row (CDC)
    Debezium-->>Kafka: publish BookDeleted
```

## Flowchart — Component Map

```mermaid
flowchart LR
    A[Client / Swagger] --> B[FastAPI API]
    B --> C[BookService]
    C --> D[UnitOfWork]
    D --> E[(PostgreSQL: books)]
    D --> F[(PostgreSQL: outbox)]
    F --> G[Debezium<br/>Postgres Connector]
    G --> H[(Kafka topic: books.events)]
```