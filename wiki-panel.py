
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash

from booze_gen import Booze, BoozeForm
import pytoml as toml

app = Flask(__name__)

config = []

@app.route("/")
def home_page():
    form = BoozeForm(None)
    #return render_template('show_entries.html', text='Tady se vygeneruje text...', config = config)
    return render_template('homepage.html', form = form, text = '', title = '')

@app.route("/add", methods=['POST'])
def add_entry():
    print(request.form['title'])
    print(request.form['text'])

    return redirect(url_for('home_page'))

@app.route("/generate", methods=['POST'])
def generate_entry():

    print(request.form['booze_name'])
    new_booze = Booze(request.form, config['booze_gen']['smoothness_levels'])

    text = new_booze.generate_text()
    form = BoozeForm(None)

    #return redirect(url_for('home_page'))
    return render_template('homepage.html', form=form, text=text, title=new_booze.name)

if __name__ == "__main__":
    with open('config.toml', 'rb') as config_file:
        config = toml.load(config_file)
    
    print(config)

    app.run(debug=True)


