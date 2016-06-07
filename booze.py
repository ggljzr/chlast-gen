from api_access import get_image_url

class Booze(object):

    def __init__(self, form, config):
        self.name = form['booze_name']
        self.origin = form['booze_origin']
        self.shop = form['booze_shop']
        self.smoothness = int(form['smoothness'])
        self.smoothness_level = config['booze_gen']['smoothness_levels'][self.smoothness]
        self.booze_type = form['booze_type']
        self.party_link = form['party_link']

        query = '%27{}+{}%27'.format(self.name.replace(' ',
            '+'), self.booze_type)

        # tady pak asi predat celej ten 'bing_api' tag z toho configu protoze
        # tam mozna bude naky dalsi nastaveni toho vyhledavace
        if form.get('include_img_link') != None:
            self.img_link = get_image_url(query, config['bing_api']['key'])
        else:
            self.img_link = None;

    def generate_text(self):
        text = "{} {} byla pořízena v oblíbeném obchodě {}.\n".format(
                self.booze_type, self.name, self.shop)
        text = text + "Země původu je {}.\n".format(self.origin)
        text = text + \
                "Chuťově je to docela {}.\n".format(self.smoothness_level)

        if(len(self.party_link) > 0):
            text = text + \
                    "Lahvinka byla zkonzumována na kalbě [[{}]].".format(self.party_link)

        if self.img_link != None:
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
