from flask import render_template
from app import app
from app.queries import all_countries, current_rank, mins_and_maxes
from app.queries import current_federation_rank, plays_currently
from app.forms import CountrySelectionForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/country', methods=['GET', 'POST'])
def country():
    form = CountrySelectionForm()
    form.country.choices = all_countries()
    code = ""
    if form.validate_on_submit():
        code = form.country.data
        country_list = [name for (i_code, name) in form.country.choices
                        if i_code == code]
        assert(len(country_list) == 1)
        country = country_list[0]
        records = mins_and_maxes(code)
        mins = records['mins']
        maxes = records['maxes']
        min_dates = [entry['date'] for entry in mins]
        max_dates = [entry['date'] for entry in maxes]
        min = mins[0]['rank']
        max = maxes[0]['rank']
        if plays_currently(code):
            rank = current_rank(code)
            federation_rank = current_federation_rank(code)
            return render_template('country.html',
                                   form=form,
                                   plays_currently=True,
                                   country=country,
                                   rank=rank,
                                   min_dates=min_dates,
                                   max_dates=max_dates,
                                   min=min,
                                   max=max,
                                   federation_rank=federation_rank
                                   )
        else:
            return render_template('country.html',
                                   form=form,
                                   plays_currently=False,
                                   country=country,
                                   min_dates=min_dates,
                                   max_dates=max_dates,
                                   min=min,
                                   max=max,
                                   )
    return render_template('country.html', form=form)
