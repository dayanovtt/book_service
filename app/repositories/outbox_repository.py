from sqlalchemy.orm import Session

from app.models.outbox import Outbox


class OutboxRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, outbox: Outbox):
        self.session.add(outbox)