from booze import Booze, Gin
import pykov as kov
import pytoml as toml

config = []

test_form = {'booze_name': 'Hendricks',
                 'booze_origin': 'Anglie',
                 'booze_shop': 'Lavin',
                 'smoothness': 4,
                 'booze_type': 'Gin',
                 'party_link': ''}


with open('config.toml', 'rb') as config_file:
    config = toml.load(config_file)


test_booze = Booze(test_form, config, link=False)

