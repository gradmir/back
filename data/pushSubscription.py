
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from marshmallow import Schema, fields


class PushSubscription(SqlAlchemyBase):
    __tablename__ = 'PushSubscriptions'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    subscription_json = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
