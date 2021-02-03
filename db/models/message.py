from sqlalchemy import Column, VARCHAR, Integer, BOOLEAN

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'message'

    message = Column(VARCHAR(150), nullable=False)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    is_delete = Column(BOOLEAN(), nullable=False, default=False)