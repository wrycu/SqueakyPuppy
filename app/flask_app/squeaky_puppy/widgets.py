from wtforms.widgets import TextInput, HiddenInput
from sqlalchemy import select


class MyTextInput(TextInput):
    def __init__(self):
        super(MyTextInput, self).__init__()

    def __call__(self, field, **kwargs):
        return 'hey'

    def __html__(self):
        return 'hello'


class MyHiddenInput(HiddenInput):
    def __call__(self, field, **kwargs):
        kwargs['data-id'] = field.data
        kwargs['data-action'] = 'modify assessment'
        return super(MyHiddenInput, self).__call__(field, **kwargs)


def get_assignees(user_table):
    return select([
        user_table.c.id,
        user_table.c.name,
    ]).execute().fetchall()
