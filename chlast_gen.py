
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash

from booze import Booze, Gin
from booze_form import BoozeForm, BoozeGenForm

import pytoml as toml

FULL_CONFIG_PATH="/home/ubuntu"

app = Flask(__name__)

app.config.update(dict(
    DEBUG=False,
    SECRET_KEY="asdjfiafew155",
    ))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

config = []

with open('config.toml', 'rb') as config_file:
        config = toml.load(config_file)

@app.route("/")
def home_page():
    form = BoozeForm()
    gen_form = BoozeGenForm()
    
    return render_template('homepage.html', form = form, gen_form = gen_form, img_link = '')

@app.route("/add", methods=['POST'])
def add_entry():
    text = request.form['article_text']
    title = request.form['article_name']

    #tady asi pak udelat tu validaci pres form.validate()
    if len(text) > 0 and len(title) > 0:
        flash("Článek přidán", 'flash')
    else:
        flash("Prázdný článek", 'error')
        form = BoozeForm()
        gen_form = BoozeGenForm(request.form)
        return render_template('homepage.html', form = form, gen_form = gen_form, img_link = '')

    return redirect(url_for('home_page'))

@app.route("/generate", methods=['POST'])
def generate_entry():
    if request.form['booze_type'] == 'Gin':
        new_booze = Gin(request.form, config)
    else:
        new_booze = Booze(request.form, config)
    
    text = new_booze.generate_text()

    form = BoozeForm(request.form)
    gen_form = BoozeGenForm()

    gen_form.article_text.data = text
    gen_form.article_name.data = new_booze.name

    return render_template('homepage.html', form=form, gen_form = gen_form, img_link = new_booze.img_link)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8080)


