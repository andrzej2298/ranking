from flask import render_template
from app import app
from app.queries import all_countries, current_rank, mins_and_maxes
from app.queries import current_federation_rank, plays_currently
from app.queries import all_ranks, current_ranking, top_places
from app.queries import gdp_and_population, averages
from app.queries import best_movement, worst_movement
from app.forms import CountrySelectionForm, DoubleCountrySelectionForm
from math import sqrt


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def get_gdp_rank(gdp_population):
    max_gdp = sqrt(max([entry['gdp'] for entry in gdp_population]))
    new_rank = [{'name': entry['name'],
                 'value': entry['rank'] / max_gdp * sqrt(entry['gdp'])}
                for entry in gdp_population]
    return sorted(new_rank, key=lambda k: k['value'])


def get_population_rank(gdp_population):
    max_population = sqrt(max([entry['population']
                               for entry in gdp_population]))
    new_rank = [{'name': entry['name'],
                 'value':
                 entry['rank'] / max_population * sqrt(entry['population'])}
                for entry in gdp_population]
    return sorted(new_rank, key=lambda k: k['value'])


@app.route('/overall')
def overall():
    map_data = current_ranking()
    countries = [country for (country, rank) in map_data]
    ranks = [rank for (country, rank) in map_data]
    top_thirty = [{'country': c, 'rank': r} for (c, r)
                  in map_data if r <= 30]
    top_ten = top_places(10)
    top_ten_confederations = [conf for (conf, occurrences) in top_ten]
    top_ten_counts = [occurrences for (conf, occurrences) in top_ten]
    top_five = top_places(5)
    top_five_confederations = [conf for (conf, occurrences) in top_five]
    top_five_counts = [occurrences for (conf, occurrences) in top_five]
    first_places = top_places(1)
    first_confederations = [conf for (conf, occurrences) in first_places]
    first_counts = [occurrences for (conf, occurrences) in first_places]
    gdp_population = gdp_and_population()
    gdp_rank = get_gdp_rank(gdp_population)
    top_gdp = [(i + 1, gdp_rank[i]['name']) for i in range(0, 30)]
    population_rank = get_population_rank(gdp_population)
    top_population = [(i + 1, population_rank[i]['name']) for i in range(0, 30)]
    average_ranking = averages()
    best = best_movement()
    worst = worst_movement()
    return render_template('overall.html',
                           countries=countries,
                           ranks=ranks,
                           top_ten_confederations=top_ten_confederations,
                           top_ten_counts=top_ten_counts,
                           top_five_confederations=top_five_confederations,
                           top_five_counts=top_five_counts,
                           first_confederations=first_confederations,
                           first_counts=first_counts,
                           top_thirty=top_thirty,
                           top_gdp=top_gdp,
                           top_population=top_population,
                           average_ranking=average_ranking,
                           best=best,
                           worst=worst)


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    form = DoubleCountrySelectionForm()
    form.first_country.choices = all_countries()
    form.second_country.choices = all_countries()
    if form.validate_on_submit():
        first_code = form.first_country.data
        second_code = form.second_country.data
        first_ranks = all_ranks(first_code)
        second_ranks = all_ranks(second_code)
        first_rank_dates = [date for (rank, date) in first_ranks]
        first_rank_values = [rank for (rank, date) in first_ranks]
        second_rank_dates = [date for (rank, date) in second_ranks]
        second_rank_values = [rank for (rank, date) in second_ranks]
        return render_template('compare.html',
                               first_code=first_code,
                               second_code=second_code,
                               form=form,
                               first_rank_values=first_rank_values,
                               second_rank_values=second_rank_values,
                               first_rank_dates=first_rank_dates,
                               second_rank_dates=second_rank_dates)
    return render_template('compare.html', form=form)


def get_country_name(code, form):
    country_list = [name for (i_code, name) in form.country.choices
                    if i_code == code]
    assert(len(country_list) == 1)
    return country_list[0]


def get_records(code):
    records = mins_and_maxes(code)
    mins = records['mins']
    maxes = records['maxes']
    return {
        'min_dates': [entry['date'] for entry in mins],
        'max_dates': [entry['date'] for entry in maxes],
        'min': mins[0]['rank'],
        'max': maxes[0]['rank']
    }


def world_cup(date):
    year = int(date[0:4])
    return year % 4 == 2


@app.route('/country', methods=['GET', 'POST'])
def country():
    form = CountrySelectionForm()
    form.country.choices = all_countries()
    if form.validate_on_submit() and form.country.data:
        code = form.country.data
        country = get_country_name(code, form)
        records = get_records(code)
        ranks = all_ranks(code)
        rank_values = [rank for (rank, date) in ranks]
        rank_dates = [date for (rank, date) in ranks]
        color = ['grey' if world_cup(date) else 'blue' for date in rank_dates]
        plays = plays_currently(code)
        rank = 0
        federation_rank = 0
        if plays:
            rank = current_rank(code)
            federation_rank = current_federation_rank(code)
        return render_template('country.html',
                               form=form,
                               plays_currently=plays,
                               country=country,
                               rank=rank,
                               min_dates=records['min_dates'],
                               max_dates=records['max_dates'],
                               min=records['min'],
                               max=records['max'],
                               federation_rank=federation_rank,
                               rank_dates=rank_dates,
                               rank_values=rank_values,
                               color=color
                               )
    return render_template('country.html', form=form)
