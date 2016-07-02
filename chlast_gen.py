
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash

from booze import Booze, Gin
from booze_form import BoozeForm, BoozeGenForm

import pytoml as toml

DEBUG=True

app = Flask(__name__)

app.config.update(dict(
    DEBUG=DEBUG,
    SECRET_KEY="babababa1348",
    ))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

config = []

with open('config.toml', 'rb') as config_file:
        config = toml.load(config_file)

@app.route("/")
def home_page():
    form = BoozeForm()
    gen_form = BoozeGenForm()
    
    return render_template('homepage.html', form = form, gen_form = gen_form, img_link = None)

@app.route("/add", methods=['POST'])
def add_entry():
    gen_form = BoozeGenForm(request.form)

    if gen_form.validate():
        flash("Článek přidán", 'flash')
    else:
        #tady je blby ze se takhle ztrati ten vyplnenej BoozeForm
        #kdyz se to nepovede
        flash("Prázdný článek", 'error')
        form = BoozeForm()
        return render_template('homepage.html', form = form, gen_form = gen_form, img_link = None)

    return redirect(url_for('home_page'))

@app.route("/generate", methods=['POST'])
def generate_entry():

    form = BoozeForm(request.form)
    gen_form = BoozeGenForm()

    if not form.validate():
        #tady pak upravit tu error message
        #v tyhle je vsechno dulezity ale vypada divne
        flash("Chyba ve formuláři: {}".format(form.errors), 'error')
        return render_template('homepage.html', form=form, gen_form = gen_form, img_link = None)

    if request.form['booze_type'] == 'Gin':
        new_booze = Gin(request.form, config)
    else:
        new_booze = Booze(request.form, config)
    
    text = new_booze.generate_text()
    
    gen_form.article_text.data = text
    gen_form.article_name.data = new_booze.name

    return render_template('homepage.html', form=form, gen_form = gen_form, img_link = new_booze.img_link)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8080, debug=DEBUG)


