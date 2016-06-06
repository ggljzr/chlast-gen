from wtforms import Form, TextAreaField, BooleanField, TextField, SelectField, SelectMultipleField, validators, widgets
from wtforms.fields.html5 import IntegerRangeField

import pytoml as toml


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class BoozeForm(Form):

    # tady to mozna udelat pres nakej global at se ten config nemusi znova
    # nacitat
    config = []
    with open('config.toml') as config_file:
        config = toml.load(config_file)

    smooth_levels = len(config['booze_gen']['smoothness_levels'])

    booze_name = TextField('Název', [validators.Length(min=1)])
    booze_origin = SelectField('Původ', choices=[
        (choice, choice) for choice in config['booze_gen']['origins']])
    booze_type = SelectField(
        'Typ', choices=[(choice, choice) for choice in config['booze_gen']['types']])
    booze_shop = SelectField(
        'Shop', choices=[(choice, choice) for choice in config['booze_gen']['shops']])
    smoothness = IntegerRangeField('Smoothness')
    juniperness = IntegerRangeField('Jalovcovost')
    pepperness = IntegerRangeField('Pepřovost')
    tonics = MultiCheckboxField('Testováno s toniky', choices=[(
        choice, choice) for choice in config['booze_gen']['tonics']])
    gt_smoothness = IntegerRangeField('Smoothness v G&T')
    party_link = TextField('Pártoška')
    include_img_link = BooleanField('Hledat obrázek', default=True) 


class BoozeGenForm(Form):
    article_name = TextField('Název článku', [validators.Length(min=1)])
    article_text = TextAreaField('', [validators.Length(min=10)])
