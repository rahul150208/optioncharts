from flask import Flask, render_template, jsonify,redirect,redirect,url_for,request

from flask_sqlalchemy import SQLAlchemy
from function import fetch_yahoo_data,get_authenticate,option_data
from supportfunc import expiryofmonth

from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime





app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class User(db.Model):
    sno: Mapped[int] = mapped_column(unique=True,nullable=False,primary_key=True)
    access_code: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"{self.access_code}"





@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        code = str(request.form['access_code'])
        resp = {'code':code}
        accesscode = User(access_code=code)
        db.session.add(accesscode)
        db.session.commit()
        get_authenticate(resp)
        # print(option_data())
        return render_template('index.html')
    return render_template('login.html')

@app.route('/redirect')
def your_redirect_route():
    return redirect("https://api.icicidirect.com/apiuser/login?api_key=D9v6t5804%409%26M32610~c%28025522248%5E%26")  # You can replace this with any URL you want



@app.route('/charts')
def index():
    return render_template('index.html')

@app.route('/api/data/<from_date>/<to_date>/<expiry_date>/<strike_price>/<option>/<timeframe>/<script_code>')
def get_data(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code):
    try:
        # print(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code,'in flaskapp')
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
        date = datetime.strptime(expiry_date, '%Y-%m-%d')
        expiry_date = date
        # expiry_date = expiryofmonth(date.year,date.month,date.day)
        strike_price = int(strike_price)

        # print('checkdatees',date,expiry_date)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    

    candlestick_data,vol_data= fetch_yahoo_data(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code)
    # print(jsonify({'candlestick': candlestick_data,'volume':vol_data}))
    return jsonify({'candlestick': candlestick_data,'volume':vol_data})

@app.route('/api/symbols')
def get_symbols():
    with open('symbols.txt') as f:
        symbols = [line.strip() for line in f]
    return jsonify(symbols)

if __name__ == '__main__':
    app.run(debug=True)