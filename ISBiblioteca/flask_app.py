from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from CreareSiAdministrareBazaDeDate import AdministrareBazaDate
import random
import AdministrareMail as mail
from openpyxl import load_workbook
import re

email_sender = 'zorbogdan2001@gmail.com'
email_password = 'attfdvpkuodyxkol'
email_receiver =''

cale = "D:/flask tutorial files/database.xlsx"
caleCarti = "D:/flask tutorial files/booksDatabase.xlsx"
book = AdministrareBazaDate(caleCarti)

bd = AdministrareBazaDate(cale)
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():

    return render_template("index.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        if bd.CautareAtribut(username) != -1 and bd.CautareAtribut(password) != -1:
            
            return redirect(url_for('home'))
  
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        number = random.randint(0,2000)
     
        if bd.CautareAtribut(email) != -1:
            msg = 'Account already exists !'
   
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            email_receiver = request.form['email']
            mail.Trimitere_Email(email_sender, email_password, 'Bun venit pe site', email_receiver)
            inreg1 = [number, request.form['username'], request.form['password'], request.form['email']]
            bd.Adaugare_Inregistrare_Noua(inreg1)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)

    return render_template("base.html")

@app.route("/books", methods =['GET', 'POST'])
def books():
    msg = ''
    if request.method == 'POST' and 'buy' in request.form  :

        buy = request.form['buy']
        if buy == 'Price: 90':
            buy = 'All the Light We Cannot See'
            email_receiver = 'chintescu.bogdan@yahoo.com'
      
        if book.CautareAtribut(buy) != -1:
            carte = book.CautareAtribut(buy)
            valoare = book.Citire_Din_Baza_Date(carte, 3)
            if valoare != 0 :
                
                if email_receiver != '':
                    mail.Trimitere_Email(email_sender, email_password, 'Va multumim pentru achizite ', email_receiver)
                book.Modificare_Valoare_In_Baza_Date(valoare, valoare-1)
            else:
                
                msg = 'Out of Stock !'
        else:
            msg = 'Not found'
  

    return render_template("books.html", msg = msg)
@app.route("/purchase")
def purchase():
    return render_template("purchase.html")
    
@app.route("/articles")
def articles():
    book = load_workbook("D:/flask tutorial files/articles.xlsx")
    sheet = book.active
    return render_template("articles.html", sheet=sheet)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

