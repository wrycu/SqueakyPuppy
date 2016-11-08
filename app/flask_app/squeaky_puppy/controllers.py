from flask import Blueprint, render_template, Response, request
from sqlalchemy import select, join, func, delete
from forms import *
import json
from datetime import datetime
from app import config

squeaky_puppy = Blueprint(
    'squeaky_puppy',
    __name__,
)


@squeaky_puppy.route('/')
def home():
    the_form = MyForm()
    user_form = UserForm()
    assessment_form = AssessmentForm()
    blacklist_form = BlacklistForm()
    callback_form = CallbackForm()
    return render_template(
        'base.html',
        form=the_form,
        user_form=user_form,
        assessment_form=assessment_form,
        blacklist_form=blacklist_form,
        callback_form=callback_form,
    )


@squeaky_puppy.route('/callback', methods=['GET', 'POST', 'DELETE'])
@squeaky_puppy.route('/callback/<string:cb_id>', methods=['GET', 'POST', 'DELETE'])
def callback(cb_id=None):
    if request.method == 'GET':
        callback_form = CallbackForm()

        results = select([
            config.CALLBACK_TABLE.c.id,
            config.CALLBACK_TABLE.c.callback,
            func.count(
                config.HIT_TABLE.c.callback_id
            ),
        ]).select_from(
            config.CALLBACK_TABLE.outerjoin(
                config.HIT_TABLE,
                config.CALLBACK_TABLE.c.id == config.HIT_TABLE.c.callback_id
            )
        ).group_by(
            config.CALLBACK_TABLE.c.id
        ).execute().fetchall()

        callbacks = []

        for result in results:
            callbacks.append({
                'id': result.id,
                'name': result.callback,
                'hits': result[2],
            })

        return render_template(
            'callbacks.html',
            callback_form=callback_form,
            callbacks=callbacks,
        )
    elif request.method == 'DELETE':
        try:
            config.HIT_TABLE.delete(
                config.HIT_TABLE.c.callback_id == cb_id
            ).execute()
            config.CALLBACK_TABLE.delete(
                config.CALLBACK_TABLE.c.id == cb_id
            ).execute()
        except Exception as e:
            return Response(json.dumps({'success': False, 'error': str(e)}), mimetype='application/json'), 500
        return Response(json.dumps({'success': True}), mimetype='application/json')
    elif request.method == 'POST':
        # new
        callback_form = CallbackForm(obj=request.data)
        if not callback_form.validate():
            return 'Bad data', 400
        config.CALLBACK_TABLE.insert(dict(request.form)).execute()
        return Response(json.dumps({'success': True}), mimetype='application/json')


@squeaky_puppy.route('/user', methods=['GET', 'POST', 'DELETE'])
@squeaky_puppy.route('/user/<string:user_id>', methods=['GET', 'POST', 'DELETE'])
def user(user_id=None):
    if request.method == 'GET':
        if not user_id:
            user_form = UserForm()

            results = select([
                config.USER_TABLE.c.id,
                config.USER_TABLE.c.name,
                config.USER_TABLE.c.email,
            ]).execute().fetchall()

            users = []

            for result in results:
                users.append({
                    'id': result.id,
                    'name': result.name,
                    'email': result.email,
                })

            return render_template(
                'users.html',
                user_form=user_form,
                users=users,
            )
        else:
            user_data = select([
                config.USER_TABLE,
            ]).where(
                config.USER_TABLE.c.id == user_id
            ).execute().fetchone()
            edit_user_form = EditUserForm(obj=user_data)
            return render_template(
                'edit_user.html',
                edit_user_form=edit_user_form,
            )
    elif request.method == 'POST':
        # update
        user_form = UserForm(obj=request.data)
        if not user_form.validate():
            return 'Bad data', 400
        if not request.form['id']:
            config.USER_TABLE.insert(dict(request.form)).execute()
        else:
            config.USER_TABLE.update(config.USER_TABLE.c.id == request.form['id'], dict(request.form)).execute()
        return Response(json.dumps({'success': True}), mimetype='application/json')
    elif request.method == 'DELETE':
        try:
            config.USER_TABLE.delete(
                config.USER_TABLE.c.id == user_id
            ).execute()
        except Exception as e:
            return Response(json.dumps({'success': False, 'error': str(e)}), mimetype='application/json'), 500
        return Response(json.dumps({'success': True}), mimetype='application/json')


@squeaky_puppy.route('/assessment', methods=['GET', 'POST', 'DELETE'])
@squeaky_puppy.route('/assessment/<string:assessment_id>', methods=['GET', 'POST', 'DELETE'])
def assessment(assessment_id=None):
    if request.method == 'GET':
        if not assessment_id:
            assessment_form = AssessmentForm()

            results = select([
                config.ASSESSMENT_TABLE.c.id,
                config.ASSESSMENT_TABLE.c.name,
                config.ASSESSMENT_TABLE.c.date_started,
            ]).execute().fetchall()

            assessments = []

            for result in results:
                assessments.append({
                    'id': result.id,
                    'name': result.name,
                    'date_started': result.date_started,
                })

            return render_template(
                'assessments.html',
                assessment_form=assessment_form,
                assessments=assessments,
            )
        else:
            assessment_data = select([
                config.ASSESSMENT_TABLE,
            ]).where(
                config.ASSESSMENT_TABLE.c.id == assessment_id
            ).execute().fetchone()
            assignee_data = select([
                config.NOTIFY_TABLE,
            ]).where(
                config.NOTIFY_TABLE.c.assessment_id == assessment_id
            ).execute().fetchall()
            full_data = {
                'name': assessment_data['name'],
                'assignees': [],
                'id': assessment_id,
            }
            for assignee in assignee_data:
                full_data['assignees'].append(assignee['user_id'])
            edit_assessment_form = EditAssessmentForm(obj=Struct(**full_data))
            return render_template(
                'edit_assessment.html',
                edit_assessment_form=edit_assessment_form,
            )
    elif request.method == 'POST':
        # update / create
        assessment_form = AssessmentForm(obj=request.data)
        if not assessment_form.validate():
            return 'Bad data', 400
        if not assessment_id:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            assessment_id = config.ASSESSMENT_TABLE.insert({
                'name': request.form['name'],
                'date_started': now,
            }).execute().inserted_primary_key[0]

            for assignee in request.form.getlist('assignees'):
                config.NOTIFY_TABLE.insert({
                    'assessment_id': assessment_id,
                    'user_id': assignee,
                }).execute()
        else:
            config.ASSESSMENT_TABLE.update(
                config.ASSESSMENT_TABLE.c.id == assessment_id,
                {'name': request.form['name']}
            ).execute()
            config.NOTIFY_TABLE.delete(
                config.NOTIFY_TABLE.c.assessment_id == assessment_id
            ).execute()
            for assignee in request.form.getlist('assignees'):
                config.NOTIFY_TABLE.insert({
                    'assessment_id': assessment_id,
                    'user_id': assignee,
                }).execute()
        return Response(json.dumps({'success': True}), mimetype='application/json')
    elif request.method == 'DELETE':
        try:
            config.HIT_TABLE.delete(
                config.HIT_TABLE.c.assessment_id == assessment_id
            ).execute()
            config.NOTIFY_TABLE.delete(
                config.NOTIFY_TABLE.c.assessment_id == assessment_id
            ).execute()
            config.ASSESSMENT_TABLE.delete(
                config.ASSESSMENT_TABLE.c.id == assessment_id
            ).execute()
        except Exception as e:
            return Response(json.dumps({'success': False, 'error': str(e)}), mimetype='application/json'), 500
        return Response(json.dumps({'success': True}), mimetype='application/json')


@squeaky_puppy.route('/domain', methods=['GET', 'POST', 'DELETE'])
@squeaky_puppy.route('/domain/<string:domain_id>', methods=['GET', 'POST', 'DELETE'])
def domain(domain_id=None):
    if request.method == 'GET':
        return 'get'
    elif request.method == 'POST':
        return 'post'
    elif request.method == 'DELETE':
        return 'delete'


@squeaky_puppy.route('/conf', methods=['GET', 'POST', 'DELETE'])
def conf():
    if request.method == 'GET':
        return 'get'
    elif request.method == 'POST':
        return 'post'
    elif request.method == 'DELETE':
        return 'delete'


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
