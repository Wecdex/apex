from sqlalchemy import create_engine, event as sa_event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from userbot import DB_URI

BASE = declarative_base()


def start() -> scoped_session:
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


SESSION = start()


# Hər commit-dən sonra avtomatik backup planla (debounced)
@sa_event.listens_for(SESSION, "after_commit")
def _after_commit(session):
    try:
        from userbot.modules.db_backup import schedule_backup
        schedule_backup()
    except Exception:
        pass
