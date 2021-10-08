
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from marshmallow import Schema, fields


class Activity(SqlAlchemyBase):
    __tablename__ = 'Activities'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rank = sqlalchemy.Column(sqlalchemy.Integer)


class ActivitySchema(Schema):
    id = fields.Number()
    name = fields.Str()
    rank = fields.Number()

