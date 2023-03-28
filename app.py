from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, string, random




app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
Migrate(app, db)

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=5)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short = rand_letters).first()
        if not short_url:
            return rand_letters

class Urls(db.Model):
    __tablename__ ="URLs"
    id = db.Column(db.Integer, primary_key = True)
    long = db.Column(db.String)
    short = db.Column(db.String)

    def __init__(self, long, short):
        self.long = long 
        self.short = short

    '''def __repr__(self):
        return "Short URl-> [{}] for url [{}] ".format(self.short, self.long)'''





@app.route('/', methods=['GET','POST'])
def home():
    if request.method== 'POST':
        url_received =request.form['in_1']
        short_url = Urls.query.filter_by(long = url_received).first()
        if short_url:
            return render_template('home.html', short_url= short_url.short)
       
        else:
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
        return render_template('home.html', short_url= short_url)
    else:
        return render_template('home.html')
@app.route('/history')
def history():
    URLs = Urls.query.all()
    return render_template("history.html", URLs = URLs)

@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f"<h2>URL does not exist</h2>"




if __name__ == '__main__':
    app.run(debug=True)