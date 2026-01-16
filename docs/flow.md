# Архитектура и Flow

Ниже описан полный поток обработки команд добавления и удаления книги  
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
    Service->>UoW: enter
    UoW->>PG: INSERT INTO books
    UoW->>Outbox: INSERT BookAdded
    UoW->>PG: COMMIT
    API-->>Client: 200 OK

    Debezium-->>Outbox: CDC (WAL)
    Debezium-->>Kafka: publish BookAdded

    Client->>API: DELETE /books/{id}
    API->>Service: delete_book()
    Service->>UoW: enter
    UoW->>PG: DELETE FROM books
    UoW->>Outbox: INSERT BookDeleted
    UoW->>PG: COMMIT
    API-->>Client: 200 OK

    Debezium-->>Outbox: CDC (WAL)
    Debezium-->>Kafka: publish BookDeleted
```

## Flowchart — Component Map

```mermaid
flowchart LR
    A[Client / Swagger]
    B[FastAPI Router]
    C[BookService]
    D[UnitOfWork]
    E[(PostgreSQL: books)]
    F[(PostgreSQL: outbox)]
    G[Debezium<br/>Postgres Connector]
    H[(Kafka topic: books.events)]

    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    F --> G
    G --> H
```
