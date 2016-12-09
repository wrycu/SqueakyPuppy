from wtforms import Form, TextField, StringField, SelectMultipleField, HiddenField, FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from widgets import *
from app import config


class MyForm(Form):
    test = TextField('b', widget=MyTextInput())
    test2 = TextField('a')


class UserForm(Form):
    name = StringField('Name')
    email = StringField('E-mail address')


class EditUserForm(UserForm):
    id = HiddenField()


class AssessmentForm(Form):
    name = StringField('Name')
    assignees = SelectMultipleField(
        'Assignees',
        choices=[]
    )

    def __init__(self, **kwargs):
        super(AssessmentForm, self).__init__(**kwargs)
        self.assignees.choices = list(select([
            config.USER_TABLE.c.id,
            config.USER_TABLE.c.name,
        ]).execute().fetchall())


class EditAssessmentForm(AssessmentForm):
    id = HiddenField()


class BlacklistForm(Form):
    domain = StringField('Domain')


class CallbackForm(Form):
    callback = StringField('Injection string')
