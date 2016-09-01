from wtforms import Form, TextField, StringField, SelectMultipleField
from widgets import *


class MyForm(Form):
    test = TextField('b', widget=MyTextInput())
    test2 = TextField('a')


class UserForm(Form):
    username = StringField('Username')
    email = StringField('E-mail address')


class AssessmentForm(Form):
    name = StringField('Name')
    assignees = SelectMultipleField('Assignees', choices=[(1, 'tim'), (2, 'jeremy'), (3, 'kevin')])


class BlacklistForm(Form):
    domain = StringField('Domain')


class CallbackForm(Form):
    callback = StringField('Injection string')
