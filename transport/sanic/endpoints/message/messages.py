from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.message.create_message import RequestCreateMessageDto
from api.response.message.message import ResponseMessageDto
from db.database import DBSession
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserConflictException

from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException, DBUserNotExistsException


class MessageEndpoint(BaseEndpoint):
    # create user
    async def method_post(
            self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        request_model = RequestCreateMessageDto(body)

        try:
            db_message = message_queries.create_message(session, request_model, uid)
        except DBUserNotExistsException:
            raise SanicUserConflictException('recipient is none')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    # get users
    async def method_get(
            self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        db_message = message_queries.get_messages(session, uid)
        response_model = ResponseMessageDto(db_message, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())
