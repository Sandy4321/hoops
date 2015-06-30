from hoopsapp.models import Teams, Players

#WTForms / Flask-WTForms
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, validators

#Form for the chatroom
class TeamForm(Form):
    team = StringField('Team', [validators.DataRequired()])
    submit = SubmitField("Submit")
    '''
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
          return False
    '''
