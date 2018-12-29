from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class CountrySelectionForm(FlaskForm):
    country = SelectField('Country', choices=[])
    submit = SubmitField('Submit')


class DoubleCountrySelectionForm(FlaskForm):
    first_country = SelectField('First country', choices=[])
    second_country = SelectField('Second country', choices=[])
    submit = SubmitField('Submit')
