import math

from sqlalchemy.sql import func

from init import init


def get_gender_ratio(model, db):
    aggregation = db.session.query(
        model.gender, func.count(model.gender).label('total')
    ).group_by(model.gender).all()
    gcd = math.gcd(aggregation[0][1], aggregation[1][1])
    return f'{aggregation[0][0]} {aggregation[0][1] / gcd} / {aggregation[1][0]} {aggregation[1][1] / gcd}'


def get_top_users_by_age(model, db, country):
    top_youngest = db.session.query(
        model.first_name, model.last_name, model.date_of_birth
    ).filter_by(country=country).order_by(model.date_of_birth.desc()).limit(10).all()
    top_oldest = db.session.query(
        model.first_name, model.last_name, model.date_of_birth
    ).filter_by(country=country).order_by(model.date_of_birth).limit(10).all()
    return top_youngest, top_oldest


app, db, config, model = init()
with app.app_context():
    game_type = config['type']
    country = config['tests']['country']
    gender_ratio = get_gender_ratio(model, db)
    print(f'Gender ratio for {game_type} is {gender_ratio}')
    top_youngest, top_oldest = get_top_users_by_age(model, db, country)
    print(f'Top youngest users for {game_type} in {country}: {top_youngest}')
    print(f'Top oldest users for {game_type} in {country}: {top_oldest}')
