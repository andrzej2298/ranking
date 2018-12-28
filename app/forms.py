from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class CountrySelectionForm(FlaskForm):
    country = SelectField(
        'Country', choices=[]
    )
    submit = SubmitField('Submit')
