from sqlalchemy.orm import Session

from app.db.session import SessionLocal


class UnitOfWork:

    def __init__(self):
        self.session: Session | None = None

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()

        self.session.close()