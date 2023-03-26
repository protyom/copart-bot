from sqlalchemy import Column, Table, ForeignKey, UniqueConstraint
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from copart_bot.db import Base


class Lot(Base):
    __tablename__ = "lot"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    lot_id = Column(Integer, unique=True, index=True)
    name = Column(String, unique=True)
    auction_date = Column(Integer, default=0)
    chats = relationship('Chat', secondary='chat_lot_m2m', backref='lot')


chat_lot_m2m = Table(
    "chat_lot_m2m",
    Base.metadata,
    Column("chat_id", ForeignKey("chat.id")),
    Column("lot_id", ForeignKey("lot.id")),
    UniqueConstraint('chat_id', 'lot_id', name='chat_lot_unique'),
)
