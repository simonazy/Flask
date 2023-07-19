from flask import Flask, render_template, session, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class SimpleForm(FlaskForm):
    submit = SubmitField("Submit")

@app.route('/', methods=['GET','POST'])
def index():
    form = SimpleForm()
    if form.validate_on_submit():
        flash("You just clicked the button!")
        return redirect(url_for('index'))
    return render_template('02-flash.html', form=form) 

app.run()

