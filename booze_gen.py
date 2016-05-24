from wtforms import Form, TextAreaField, BooleanField, TextField, SelectField, SelectMultipleField, validators, widgets
from wtforms.fields.html5 import IntegerRangeField

import pytoml as toml

from api_access import get_image_url


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


class BoozeGenForm(Form):
    article_name = TextField('Název článku', [validators.Length(min=1)])
    article_text = TextAreaField('', [validators.Length(min=10)])


class Booze(object):

    def __init__(self, form, config):
        self.name = form['booze_name']
        self.origin = form['booze_origin']
        self.shop = form['booze_shop']
        self.smoothness = int(form['smoothness'])
        self.smoothness_level = config['booze_gen'][
            'smoothness_levels'][self.smoothness]
        self.booze_type = form['booze_type']
        self.party_link = form['party_link']

        query = '%27{}+{}%27'.format(self.name.replace(' ',
                                                       '+'), self.booze_type)

        # tady pak asi predat celej ten 'bing_api' tag z toho configu protoze
        # tam mozna bude naky dalsi nastaveni toho vyhledavace
        self.img_link = get_image_url(query, config['bing_api']['key'])

    def generate_text(self):
        text = "{} {} byla pořízena v oblíbeném obchodě {}.\n".format(
            self.booze_type, self.name, self.shop)
        text = text + "Země původu je {}.\n".format(self.origin)
        text = text + \
            "Chuťově je to docela {}.\n".format(self.smoothness_level)

        if(len(self.party_link) > 0):
            text = text + \
                "Lahvinka byla zkonzumována na kalbě [[{}]].".format(
                    self.party_link)

        text = text + "Obrázek: {}\n".format(self.img_link)
        return text


class Gin(Booze):

    def __init__(self, form, config):
        Booze.__init__(self, form, config)
        self.juniperness = form['juniperness']
        self.pepperness = form['pepperness']
        self.tonics = form.getlist('tonics')
        self.gt_smoothness = int(form['gt_smoothness'])
        self.gt_smoothness_level = config['booze_gen'][
            'smoothness_levels'][self.gt_smoothness]

    def generate_text(self):
        text = super(Gin, self).generate_text()
        text = text + "Jalovcovost je {}.\n".format(self.juniperness)
        text = text + "Pepřovost je {}.\n".format(self.pepperness)
        # tady ofc zatim neni zadna kontrola jestli to pole je prazdny :-)
        # nebo teda jen primitivne
        if len(self.tonics) > 0:
            text = text + "Testováno s toniky {}. ".format(self.tonics)
            text = text + \
                "V G&T byl docela {}.\n".format(self.gt_smoothness_level)
        return text


class Vodka(Booze):
    pass
