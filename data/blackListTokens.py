import datetime as datetime

from marshmallow import Schema, fields
import sqlalchemy as sqlalchemy

from data import db_session
from data.db_session import SqlAlchemyBase


class BlacklistToken(SqlAlchemyBase):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    token = sqlalchemy.Column(sqlalchemy.String(500), unique=True, nullable=False)
    blacklisted_on = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token, db_session):
        # check whether auth token has been blacklisted
        session = db_session.create_session()
        black_listed_token = session.query(BlacklistToken).filter_by(token=str(auth_token)).first()
        schema = BlacklistTokenSchema(many=True)
        res = schema.dump(black_listed_token)
        session.close()
        if res:
            return True
        else:
            return False

class BlacklistTokenSchema(Schema):
    id = fields.Number()
    token = fields.Str()
    blacklisted_on = fields.Date()
