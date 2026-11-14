from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    pages = Column(Integer, nullable=False)

    chunks = Column(Integer, nullable=False)

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )