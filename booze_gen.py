from wtforms import Form, TextAreaField, BooleanField, TextField, SelectField, validators
from wtforms.fields.html5 import IntegerRangeField

import pytoml as toml

from api_access import get_image_url

class BoozeForm(Form):

    #tady to mozna udelat pres nakej global at se ten config nemusi znova nacitat
    config = []
    with open('config.toml') as config_file:
        config = toml.load(config_file)

    smooth_levels = len(config['booze_gen']['smoothness_levels'])

    booze_name = TextField('Název', [validators.Length(min=1)])
    booze_origin = SelectField('Původ', choices=[
                         (choice, choice) for choice in config['booze_gen']['origins']])
    booze_type = SelectField('Typ', choices = [(choice, choice) for choice in config['booze_gen']['types']])
    booze_shop = SelectField('Shop', choices = [(choice, choice) for choice in config['booze_gen']['shops']])
    smoothness = IntegerRangeField('Smoothness')
    party_link = TextField('Pártoška')


class BoozeGenForm(Form):
    article_name = TextField('Název článku', [validators.Length(min=1)])
    article_text = TextAreaField('', [validators.Length(min=10)])

class Booze(object):

    def __init__(self, form, smooth_levels):
        self.name = form['booze_name']
        self.origin = form['booze_origin']
        self.shop = form['booze_shop']
        self.smoothness = int(form['smoothness'])
        self.smoothness_level = smooth_levels[self.smoothness]
        self.booze_type = form['booze_type']
        self.party_link = form['party_link']

        query = '%27{}+{}%27'.format(self.name.replace(' ', '+'), self.booze_type)

        #tady pak asi predat celej ten 'bing_api' tag z toho configu protoze
        #tam mozna bude naky dalsi nastaveni toho vyhledavace
        self.img_link = get_image_url(query, config['bing_api']['key']) 

    def generate_text(self):
        text = "{} {} byla pořízena v oblíbeném obchodě {}.\n".format(
            self.booze_type, self.name, self.shop)
        text = text + "Země původu je {}.\n".format(self.origin)
        text = text + \
            "Chuťově je to docela {}.\n".format(self.smoothness_level)

        if(len(self.party_link) > 0):
            text = text + "Lahvinka byla zkonzumována na kalbě [[{}]].".format(self.party_link)

        text = text + "Obrázek: {}".format(self.img_link)
        return text

class Gin(Booze):
    pass

class Vodka(Booze):
    pass
