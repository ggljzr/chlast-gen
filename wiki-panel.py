
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash

app = Flask(__name__)

@app.route("/")
def home_page():
    
    return render_template('show_entries.html', text='Tady se vygeneruje text...')

@app.route("/add", methods=['POST'])
def add_entry():
    print(request.form['title'])
    print(request.form['text'])

    return redirect(url_for('home_page'))

@app.route("/generate", methods=['POST'])
def generate_entry():

    booze_name = request.form['booze_name']
    booze_origin = request.form['booze_origin']

    text = "Jde o chlast {} z {}".format(booze_name, booze_origin)

    #return redirect(url_for('home_page'))
    return render_template('show_entries.html', text=text, title=booze_name)

if __name__ == "__main__":
    app.run(debug=True)


