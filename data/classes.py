
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from marshmallow import Schema, fields


class Class(SqlAlchemyBase):
    __tablename__ = 'Classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    users = orm.relation("User", back_populates='Class')

class ClassSchema(Schema):
    id = fields.Number()
    name = fields.Str()