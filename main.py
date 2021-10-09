from datetime import date
import datetime as datetime
import logging

from sqlalchemy import orm
from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from data import db_session
from data.activities import ActivitySchema, Activity
from data.blackListTokens import BlacklistToken
from data.classes import Class, ClassSchema
from flask_cors import CORS
import json
from marshmallow import Schema, fields
# from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from data.users import User, UserSchema
from data.works import Work, WorkSchema

print(1/0)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# login_manager = LoginManager()
# login_manager.init_app(app)
CORS(app)


def encode_week(start_date, activities_list, data):
    result = dict()
    result['start_date'] = start_date
    result['end_date'] = start_date + datetime.timedelta(days=6)

    # activities_list = []
    # for work in data:
    #     if not work['activity']['name'] in activities_list:
    #         activities_list.append(work['activity']['name'])
    result['week_lines'] = list()
    for activity in activities_list:
        result_line = dict()
        result_line['activity_name'] = activity
        result_line['week_data'] = []
        for x in range(7):
            current_date = (result['start_date'] + datetime.timedelta(days=x)).strftime('%Y-%m-%d')
            work = next(
                filter(lambda work: work['activity']['name'] == activity and work['date'] == current_date, data), None)
            if not work:
                result_line['week_data'].append(False)
            else:
                result_line['week_data'].append(work['done'])
        result['week_lines'].append(result_line)

    return result


def main():
    db_session.global_init("db/blogs.db")
    # klass = Klass()
    # klass.name = "7b"
    # db_sess = db_session.create_session()
    # db_sess.add(klass)
    # db_sess.commit()

    app.run()


@app.route('/classes')
def get_classes():
    # fetching from the database
    session = db_session.create_session()
    exam_objects = session.query(Class).all()

    # transforming into JSON-serializable objects
    schema = ClassSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams)


@app.route('/activities')
def get_activities():
    # fetching from the database
    session = db_session.create_session()
    activities_objects = session.query(Activity).all()

    # transforming into JSON-serializable objects
    schema = ActivitySchema(many=True)
    activities = schema.dump(activities_objects)

    # serializing as JSON
    session.close()
    return jsonify(activities)


@app.route('/works')
def get_works():
    user = get_user_from_token(request)
    if not user:
        return jsonify({'isAuth': 'Nononono'})
    session = db_session.create_session()
    works_objects = session.query(Work).filter(Work.user == user)
    schema = WorkSchema(many=True)
    works = schema.dump(works_objects)

    session.close()
    return jsonify(works)


def decode_week2(user, request):
    session = db_session.create_session()
    activities_objects = list(session.query(Activity).all())
    activitySchema = ActivitySchema(many=True)
    activities = activitySchema.dump(activities_objects)
    session.close()

    session = db_session.create_session()
    user = session.query(User).options(orm.joinedload(User.works)).filter(User.id == user.id).first()
    start_date = date.fromisoformat(request.get_json().get('start_date')[0:10])
    for week_line in request.get_json().get('week_lines'):
        activity_name = week_line.get('activity_name')
        activity = next(filter(lambda a: a.name == activity_name, activities_objects))
        if not activity:
            continue

        for day_of_week, done in enumerate(week_line.get('week_data')):
            work_date = start_date + datetime.timedelta(days=day_of_week)
            work_from_db = list(filter(lambda w: w.date == work_date and w.activity_id == activity.id, user.works))
            if work_from_db:
                if done:
                    work_from_db[0].make_done()
                else:
                    work_from_db[0].make_undone()
                session.commit()
                continue

            work = Work()
            work.date = work_date
            work.done = done
            work.activity = activity
            work.user = user
            work.Class = user.Class
            user.works.append(work)
            session.commit()


def decode_week(user, request):
    session = db_session.create_session()
    activities_objects = list(session.query(Activity).all())
    start_date = date.fromisoformat(request.get_json().get('start_date')[0:10])
    for week_line in request.get_json().get('week_lines'):
        activity_name = week_line.get('activity_name')
        activity_id = next(filter(lambda a: a.name == activity_name, activities_objects)).id
        if not activity_id:
            continue

        for day_of_week, done in enumerate(week_line.get('week_data')):

            work_date = start_date + datetime.timedelta(days=day_of_week)
            work_from_db = session.query(Work).filter(Work.user == user, Work.date == work_date,
                                                      Work.activity_id == activity_id).first()
            if work_from_db:
                #  session.query(Work).filter(Work.user == user, Work.date == work_date,
                #                            Work.activity_id == activity_id).update({'done': done})  # .first()
                continue

            work = Work()
            work.date = work_date
            work.done = done
            work.activity_id = activity_id
            work.user = user
            work.Class = user.Class
            session.add(work)
            session.commit()
    session.commit()


@app.route('/setWeek', methods=['POST'])
def set_week():
    user = get_user_from_token(request)
    if not user:
        return jsonify({'isAuth': 'Nononono'})
    works = decode_week2(user, request)

    return jsonify({'status': 'ok'})


@app.route('/week', methods=['POST'])
def get_week():
    # json_data = request.json
    user = get_user_from_token(request)
    if not user:
        return jsonify({'isAuth': 'Nononono'})
    session = db_session.create_session()
    start_date = datetime.date.fromisoformat(request.args.get('start_date'))
    date_range = [start_date + datetime.timedelta(days=x) for x in range(7)]
    works_objects = session.query(Work).filter(Work.user == user, Work.date.in_(date_range))
    schema = WorkSchema(many=True)
    works = schema.dump(works_objects)
    activities_objects = session.query(Activity).all()
    activities_list = list(map(lambda a: a.name, activities_objects))
    week = encode_week(start_date, activities_list, works)
    session.close()
    return jsonify(week)


@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(
        nick_name=json_data['nick_name'],
        hashed_password=json_data['password']
    )
    try:
        session = db_session.create_session()
        session.add(user)
        session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    session.close()
    return jsonify({'result': status})


@app.route('/status')
def status():
    # json_data = request.json
    user = get_user_from_token(request)
    if not user:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route('/rank')
def rank():
    start_date = date.fromisoformat(request.args.get('start_date')[0:10])
    end_date = date.fromisoformat(request.args.get('end_date')[0:10])

    db_sess = db_session.create_session()
    activities_objects = list(db_sess.query(Activity).all())
    users = db_sess.query(User).options(orm.joinedload(User.works)).all()
    rank = list()
    for user in users:
        row = dict()
        row['name'] = user.name
        row['points'] = 0
        for activity in activities_objects:
            filtered = list(filter(lambda work: work.activity == activity and work.done
                                                and start_date <= work.date <= end_date, user.works))
            row[activity.name] = len(filtered)
            row['points'] += activity.rank * len(filtered)
        rank.append(row)

    return jsonify(rank)


@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.nick_name == json_data['nick_name']).first()
    if user and user.check_password(json_data['password']):
        # status = login_user(user, remember=True)
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token
            }
            return jsonify(response_object)
    else:
        status = False
        return jsonify({'result': status})


@app.route('/logout', methods=['POST'])
def logout():
    try:
        blacklistToken = BlacklistToken(request.headers.get('Authorization'))
        db_sess = db_session.create_session()
        db_sess.add(blacklistToken)
        db_sess.commit()

        return jsonify({'status': 'logged out'})
    except Exception as e:
        return jsonify({'status': str(e)})


def get_user_from_token(request):
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return jsonify(response_object)
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token, db_session)
        if not isinstance(resp, str):
            session = db_session.create_session()
            user_object = session.query(User).options(orm.joinedload(User.Class)).filter_by(id=resp).first()
            # schema = UserSchema()
            # user = schema.dump(user_object)
            session.close()
            return user_object
        return None
    else:
        return None


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.debug('Main started')
    main()
