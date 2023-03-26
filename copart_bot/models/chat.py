from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from copart_bot.db import Base


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    name = Column(String, unique=True)
    lots = relationship('Lot', secondary='chat_lot_m2m', backref='chat')
