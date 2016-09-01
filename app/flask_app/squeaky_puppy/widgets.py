from wtforms.widgets import TextInput


class MyTextInput(TextInput):
    def __init__(self):
        super(MyTextInput, self).__init__()

    def __call__(self, field, **kwargs):
        return 'hey'

    def __html__(self):
        return 'hello'
