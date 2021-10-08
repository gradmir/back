
import sqlalchemy
from sqlalchemy import orm

from .activities import ActivitySchema
from .db_session import SqlAlchemyBase
from marshmallow import Schema, fields


class Work(SqlAlchemyBase):
    __tablename__ = 'Works'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    done = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    Class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Classes.id"))
    Class = orm.relation('Class')

    activity_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Activities.id"))
    activity = orm.relation('Activity')

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.id"))
    user = orm.relation('User')

    def make_done(self):
        self.done = True

    def make_undone(self):
        self.done = False


class WorkSchema(Schema):
    id = fields.Number()
    date = fields.Date()
    done = fields.Boolean()
    activity = fields.Nested(ActivitySchema)