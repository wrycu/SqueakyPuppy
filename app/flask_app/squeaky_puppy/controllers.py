from flask import Blueprint, render_template, Response, request
from sqlalchemy import select, join, func
from forms import *
import json
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
