from typing import List

from api.request.message.create_message import RequestCreateMessageDto
from api.request.message.patch_message import RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, uid: int) -> DBMessage:
    db_user = session.get_user_by_login(message.recipient)
    if db_user is None:
        raise DBUserNotExistsException

    new_message = DBMessage(
        message=message.message,
        sender_id=uid,
        recipient_id=db_user.id,
    )

    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, uid: int) -> List['DBMessage']:
    return session.get_message_all(uid)


def get_message(session: DBSession, uid: int, mid: int) -> DBMessage:
    db_message = session.get_message_by_id(uid, mid)
    if db_message is None:
        raise DBMessageNotExistsException

    return db_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, user_id: int, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(user_id, message_id)

    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    return db_message


def delete_message(session: DBSession, user_id: int, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(user_id, message_id)
    db_message.is_delete = True
    return db_message
