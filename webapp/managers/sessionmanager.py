from ..core.utils.dbsession import dbsession
from ..core.utils.security import generate_token, verify_token
from ..core.models.sessiontoken import SessionToken


class SessionManager():

    def create(self, user_id: str, email: str, expires: int=2592000) -> str:
        """ returns a new JWT representing a new session. this is used to interact
        with all fetchy endpoints. a default token expires after 2592000 seconds (30 days)"""

        try:
            payload = {
                "email": email,
                "uuid": user_id,
                }
            token = generate_token(payload, expires)

            with dbsession() as session:
                session_token = SessionToken(user_id, token)
                session.add(session_token)

            return token

        except Exception as e:
            raise(e)


    def verify(self, user_id: str, token: str) -> bool:
        with dbsession() as session:
            owner_sessions = session.query(SessionToken)\
                .filter(SessionToken.user_id==user_id)\
                .with_entities(SessionToken.token)\
                .all()

        return verify_token(token) and any([token == s.token for s in owner_sessions or []])


    def delete(self, user_id: str, token: str):
        with dbsession() as session:
            session.query(SessionToken)\
                .filter(SessionToken.user_id==user_id, SessionToken.token==token)\
                .delete(synchronize_session=False)

