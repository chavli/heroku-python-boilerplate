"""
    operations dealing with user accounts
"""
import traceback
import datetime
import os
from ..core.utils.security import generate_hash, verify_hash
from ..core.utils.dbsession import dbsession
from ..core.utils.responsejson import MessageResponseJson, ErrorResponseJson, ResponseJson
from ..core.models.account import Account
from ..managers.sessionmanager import SessionManager


class AccountManager():

    def logout(self, user_id: str, token: str) -> ResponseJson:
        """ remove the given session token from our database. this endpoint always
        returns true. """
        try:
            SessionManager().delete(user_id, token)
            return MessageResponseJson("logged out")

        except Exception as e:
            traceback.print_exc()
            raise(e)


    def create(self, email: str, password: str) -> ResponseJson:
        """ create a new user account """
        try:
            with dbsession() as session:
                account = session.query(Account)\
                    .filter(Account.email == email)\
                    .first()

            if not account:
                # woohoo a new account!

                h_password = generate_hash(password)
                account = Account(email, h_password)
                with dbsession() as session:
                    session.add(account)
                    user_id = account.user_id

                # now create the session token the user will use going forward
                session_token = SessionManager().create(user_id, email)
                payload = {
                    "uuid": user_id,
                    "token": session_token,
                }
                return ResponseJson(payload)

            else:
                return ErrorResponseJson("username already taken")

        except Exception as e:
            traceback.print_exc()
            raise(e)

    def login(self, email: str, password: str) -> ResponseJson:
        """ return a new session token if credentials are valid """
        try:
                with dbsession() as session:
                    account = session.query(Account)\
                            .filter(Account.email == email)\
                            .first()

                if not account:
                    return ErrorResponseJson("no account found")
                else:
                    with dbsession() as session:
                        account = session.query(Account)\
                            .filter(Account.email == email)\
                            .with_entities(Account.user_id)\
                            .first()
                        user_id = account.user_id

                    session_token = SessionManager().create(user_id, email)
                    return ResponseJson({
                        "uuid": user_id,
                        "token": session_token,
                    })
        except Exception as e:
            traceback.print_exc()
            raise(e)


    def verify_account(self, email: str, password: str) -> bool:
        """ check if the given credentials are valid """
        verified = False
        with dbsession() as session:
            account = session.query(Account)\
                .filter(Account.email == email)\
                .with_entities(Account.secret)\
                .first()
        if account:
            verified = verify_hash(password, account.secret)

        return verified
