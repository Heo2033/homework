from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.message.patch_message import RequestPatchMessageDto
from api.response.message.message import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBDataException, DBIntegrityException

from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserMessageNotFound, SanicDBException


class UserMessageEndpoint(BaseEndpoint):
    async def method_get(
            self, request: Request, body: dict, session: DBSession, uid: int, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        try:
            db_message = message_queries.get_message(session, uid, mid)
        except DBMessageNotExistsException as e:
            raise SanicUserMessageNotFound(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, uid: int, mid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        request_model = RequestPatchMessageDto(body)

        try:
            message = message_queries.patch_message(session, request_model, uid, mid)
        except DBMessageNotExistsException as e:
            raise SanicUserMessageNotFound(str(e))

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, uid: int, mid: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            message_queries.delete_message(session, uid, mid)
        except DBMessageNotExistsException:
            raise SanicUserMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)
