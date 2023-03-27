import glob
from dateutil import parser

import pandas as pd

from init import init


def format_json_users(users):
    users = pd.concat([users.name.apply(pd.Series), users.drop('name', axis=1)], axis=1)
    users = users.drop('location', axis=1)
    users = users.drop('login', axis=1)
    users = users.drop('id', axis=1)
    users = users.drop('picture', axis=1)
    return users


def read(data_path):
    users = pd.DataFrame()
    for file_name in glob.glob(data_path + '**/*', recursive=True):
        if '.csv' in file_name:
            if users.empty:
                users = pd.read_csv(file_name)
            else:
                users.merge(
                    pd.read_csv(file_name),
                    how='inner',
                    left_on=['first_name', 'last_name', 'gender', 'email', 'dob'],
                    right_on=['first_name', 'last_name', 'gender', 'email', 'dob']
                )
        if '.json' in file_name:
            if users.empty:
                users = format_json_users(
                    pd.read_json(file_name, lines=True)
                )
            else:
                users.merge(
                    format_json_users(
                        pd.read_json(file_name, lines=True)
                    ),
                    how='inner',
                    left_on=['first', 'last', 'gender', 'email', 'nat', 'dob'],
                    right_on=['first', 'last', 'gender', 'email', 'nat', 'dob']
                )
    return users


def process(raw_users):
    users = []
    for raw_user in raw_users.itertuples():
        user = {
            'email': raw_user.email,
            'gender': raw_user.gender.lower(),
        }
        if hasattr(raw_user, 'first'):
            user['first_name'] = raw_user.first
        elif hasattr(raw_user, 'first_name'):
            user['first_name'] = raw_user.first_name.lower()
        if hasattr(raw_user, 'last'):
            user['last_name'] = raw_user.last
        elif hasattr(raw_user, 'last_name'):
            user['last_name'] = raw_user.last_name.lower()
        if hasattr(raw_user, 'nat'):
            user['country'] = raw_user.nat
        if hasattr(raw_user, 'dob'):
            if '/' in raw_user.dob:
                user['date_of_birth'] = parser.parse(raw_user.dob)
            else:
                user['date_of_birth'] = parser.parse(raw_user.dob)
        users.append(user)
    return users


def write_to_db(users, app, model, config):
    with app.app_context():
        model.set_users(users)


def run(app, db, config, model):
    write_to_db(
        process(
            read(config['data_folders'][config['type']])
        ),
        app,
        model,
        config['dbs'][config['type']]
    )


run(*init())
