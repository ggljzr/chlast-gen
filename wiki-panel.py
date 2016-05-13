
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash

from booze_gen import Booze, BoozeForm
import pytoml as toml

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY="dev_key",
    ))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

config = []

@app.route("/")
def home_page():
    form = BoozeForm()
    #return render_template('show_entries.html', text='Tady se vygeneruje text...', config = config)
    return render_template('homepage.html', form = form, text = '', title = '', img_link = '')

@app.route("/add", methods=['POST'])
def add_entry():
    text = request.form['text']
    title = request.form['title']

    if len(text) > 0 and len(title) > 0:
        flash("Článek přidán", 'flash')
    else:
        flash("Prázdný článek", 'error')
        form = BoozeForm()
        return render_template('homepage.html', form = form, text = text, title = title, img_link = '')

    return redirect(url_for('home_page'))

@app.route("/generate", methods=['POST'])
def generate_entry():

    print(request.form['booze_name'])
    new_booze = Booze(request.form, config['booze_gen']['smoothness_levels'])

    text = new_booze.generate_text()

    form = BoozeForm()
    form.booze_name.data = new_booze.name
    form.booze_shop.default = new_booze.shop
    form.smoothness.data = int(new_booze.smoothness)
    form.party_link.data = new_booze.party_link

    #return redirect(url_for('home_page'))
    return render_template('homepage.html', form=form, text=text, title=new_booze.name, img_link = new_booze.img_link)

if __name__ == "__main__":
    with open('config.toml', 'rb') as config_file:
        config = toml.load(config_file)
    
    print(config)

    app.run(debug=True)


