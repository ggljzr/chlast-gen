from wtforms import Form, TextAreaField, BooleanField, TextField, SelectField, validators
from wtforms.fields.html5 import IntegerRangeField

import pytoml as toml


class BoozeForm(Form):

    config = []
    with open('config.toml') as config_file:
        config = toml.load(config_file)
    smooth_levels = len(config['booze_gen']['smoothness_levels'])

    booze_name = TextField('Název', [validators.Length(min=1)])
    booze_origin = SelectField('Původ', choices=[
                         (choice, choice) for choice in config['booze_gen']['origins']])
    booze_type = SelectField('Typ', choices = [(choice, choice) for choice in config['booze_gen']['types']])
    booze_shop = SelectField('Shop', choices = [(choice, choice) for choice in config['booze_gen']['shops']])
    smoothness = IntegerRangeField('Smoothness', default=0)
    

class Booze(object):

    def __init__(self, form, smooth_levels):
        self.name = form['booze_name']
        self.origin = form['booze_origin']
        self.shop = form['booze_shop']
        self.smoothness = int(form['smoothness'])
        self.smoothness_level = smooth_levels[self.smoothness]
        self.booze_type = form['booze_type']

    def generate_text(self):
        text = "{} {} byla pořízena v oblíbeném obchodě {}.\n".format(
            self.booze_type, self.name, self.shop)
        text = text + "Země původu je {}.\n".format(self.origin)
        text = text + \
            "Chuťově je to docela {}.\n".format(self.smoothness_level)
        text = text + "Smoothness je {}.".format(self.smoothness)
        return text
