import base64
import hashlib

from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import sqlite3 as sql
import os

app = Flask(__name__)
app.secret_key = 'development key'

con = sql.connect("database.db")
c = con.cursor()


## PAGES
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/report')
def report():
    return render_template("report.html")
@app.route('/loginPage')
def loginPage():
    return render_template("login.html")
@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/MyHedgehogs')
def myHedgehogs():
    return render_template("myhedgehogs.html")
@app.route('/WatchMeGrow')
def meGrowing():
    return render_template("megrowing.html")
@app.route('/ForSale')
def forSale():
    con = sql.connect("database.db")
    c = con.cursor()
    rows = getForSale(con, c)

    return render_template("forsale.html", rows=rows)
@app.route('/Sold')
def sold():
    con = sql.connect("database.db")
    c = con.cursor()
    rows = getSold(con, c)

    return render_template("sold.html", rows=rows)
@app.route('/Care')
def care():
    return render_template("care.html")
@app.route('/Q&A')
def questionsAndAnswers():
    con = sql.connect("database.db")
    c = con.cursor()
    rows = getQA(con, c)

    return render_template("questionsandanswers.html", rows=rows)
@app.route('/FunFacts')
def funFacts():
    con = sql.connect("database.db")
    c = con.cursor()
    rows = getFacts(con, c)

    return render_template("funfacts.html", rows=rows)
@app.route('/Contact')
def contact():
    return render_template("contact.html")
@app.route('/Reviews')
def reviews():
    con = sql.connect("database.db")
    c = con.cursor()
    rows = getReviews(con, c)

    return render_template("reviews.html", rows=rows)
@app.route('/submitReview', methods=['POST'])
def submitReview():
    review = request.form.get('review')
    name = request.form.get('name')
    today = date.today()
    con = sql.connect("database.db")
    c = con.cursor()

    c.execute("""INSERT INTO Reviews (name, review, date) VALUES (?, ?, ?)""", (name, review, today.strftime("%m/%d/%y")))
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from Reviews"
    c.execute(stmt)
    con.commit()
    rows=c.fetchall()

    return render_template('reviews.html', rows=rows)

@app.route('/submitRegistration', methods=['POST'])
def submitRegistration():
    password = request.form.get('password')
    email = request.form.get('email')
    con = sql.connect("database.db")
    c = con.cursor()

    c.execute("""INSERT INTO Login (email, password) VALUES (?, ?)""", (email, password))
    con.commit()

    return render_template('login.html')

@app.route('/submitlogin', methods=['GET', 'POST'])
def submitLogin():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        validation = validate(email, password)
        if validation == False:
            error = 'Invalid Credentials. Please try again.'
            print("Error")
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

def validate(email, password):
    con = sql.connect("database.db")
    validation = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Login")
                rows = cur.fetchall()
                for row in rows:
                    dbEmail = row[1]
                    dbPass = row[2]
                    if dbEmail==email:
                        if dbPass==password:
                            validation = True
    return validation


@app.route('/submitFact', methods=['POST'])
def submitFact():
    fact = request.form.get('fact')
    name = request.form.get('name')
    today = date.today()
    con = sql.connect("database.db")
    c = con.cursor()

    c.execute("""INSERT INTO FunFacts (name, fact, date) VALUES (?, ?, ?)""",
              (name, fact, today.strftime("%m/%d/%y")))
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from FunFacts"
    c.execute(stmt)
    con.commit()
    rows = c.fetchall()

    return render_template('funfacts.html', rows=rows)
@app.route('/submitQuestion', methods=['POST'])
def submitQuestion():
    question = request.form.get('question')
    name = request.form.get('name')
    today = date.today()
    con = sql.connect("database.db")
    c = con.cursor()

    c.execute("""INSERT INTO QA (name, question, answer) VALUES (?, ?, ?)""", (name, question, "Not yet answered! if you have an answer, please email it to us!"))

    # return table results
    con.row_factory = sql.Row
    stmt = "select * from QA"
    c.execute(stmt)
    con.commit()
    rows = c.fetchall()

    return render_template('questionsandanswers.html', rows=rows)
@app.route('/inquireHoglet', methods=['POST'])
def inquireHoglet():
    email = request.form.get('email')
    hoglet = request.form.get('hoglet')
    today = date.today()
    con = sql.connect("database.db")
    c = con.cursor()

    try:
        cur2 = con.execute("SELECT name, requests FROM ForSale")
        for row1 in cur2.fetchall():
            hogletTmp = row1[0]

            if hoglet == hogletTmp:
                print
                "yes"  # as a test for me to see the loop worked
                con.execute("UPDATE ForSale SET requests=requests+1 WHERE name=?", (hoglet,))
                c.execute("""INSERT INTO Inquiries (email, hoglet, date) VALUES (?, ?, ?)""", (email, hoglet, today.strftime("%m/%d/%y")))
                con.commit()
    except Exception as err:
        print(err)

    rows = con.execute("SELECT * FROM ForSale")
    rows = rows.fetchall()
    return render_template('forsale.html', rows=rows)

class ForSaleListing(object):
    def __init__(self):
        self.image_name = []

    def load_directory(self, path):
        """
        :param path: Provide Path of File Directory
        :return: List of image Names
        """
        for x in os.listdir(path):
            self.image_name.append(x)

        return self.image_name

    def create_database(self, name, price, dob, color, gender, ready, image, c):
        """
        :param name: String
        :param image:  BLOP Data
        :return: None
        """
        # Insert data into A
        try:
            c.execute("""INSERT INTO ForSale 
            (name, price, dob, color, gender, ready, img) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (name, price, dob, color, gender, ready, image))
        except Exception as e:
            print(e)

## GETTERS FOR DATABASE STUFF
def getForSale(con, c):
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from ForSale"
    c.execute(stmt)

    return c.fetchall()
def getSold(con, c):
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from Sold"
    c.execute(stmt)

    return c.fetchall()
def getFacts(con, c):
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from FunFacts"
    c.execute(stmt)

    return c.fetchall()
def getReviews(con, c):
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from Reviews"
    c.execute(stmt)

    return c.fetchall()
def getQA(con, c):
    # return table results
    con.row_factory = sql.Row
    stmt = "select * from QA"
    c.execute(stmt)

    return c.fetchall()
def get_value(item):
    info = item.strip().split(':')
    val = info[1].strip().split(',')
    return val[0].strip()

## POPULATE DATABASE
def popDatabase():
    # create tables
    try:
        stmt = "CREATE TABLE IF NOT EXISTS ForSale (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price TEXT NOT NULL, dob TEXT NOT NULL, color TEXT NOT NULL, gender TEXT NOT NULL, ready TEXT NOT NULL, img TEXT NOT NULL, requests INTEGER);"
        c.execute(stmt)
        stmt = "CREATE TABLE IF NOT EXISTS Sold (id INTEGER PRIMARY KEY, name TEXT NOT NULL, img TEXT NOT NULL);"
        c.execute(stmt)
        stmt = "CREATE TABLE IF NOT EXISTS Reviews (id INTEGER PRIMARY KEY, name TEXT NOT NULL, review TEXT NOT NULL, date TEXT NOT NULL);"
        c.execute(stmt)
        stmt = "CREATE TABLE If NOT EXISTS QA (id INTEGER PRIMARY KEY, name TEXT NOT NULL, question TEXT NOT NULL, answer TEXT);"
        c.execute(stmt)
        stmt = "CREATE TABLE If NOT EXISTS FunFacts (id INTEGER PRIMARY KEY, name TEXT NOT NULL, fact TEXT NOT NULL, date TEXT NOT NULL);"
        c.execute(stmt)
        stmt = "CREATE TABLE If NOT EXISTS Inquiries (id INTEGER PRIMARY KEY, email TEXT NOT NULL, hoglet TEXT NOT NULL, date TEXT NOT NULL);"
        c.execute(stmt)
        stmt = "CREATE TABLE IF NOT EXISTS Login (id INTEGER PRIMARY KEY, email TEXT NOT NULL, password TEXT NOT NULL);"
        c.execute(stmt)
        con.commit()
    except Exception as e:
        print(e)

    # populate tables
    try:
        # for sale
        obj = ForSaleListing()
        forSalePath = os.getcwd() + "\\static\\images\\ForSale"
        forSalePath = forSalePath.replace("\\", "/")
        for x in obj.load_directory(path=forSalePath):
            try:
                if ".jpg" in x:
                    txtFile = x.replace(".jpg", ".txt")
                    price = dob = color = gender = ready = ''
                    name = x.replace(".jpg", "")
                    try:
                        with open(forSalePath + "/" + txtFile, "r") as f:
                            file_data = f.readlines()
                            for item in file_data:
                                if 'Price' in item:
                                    price = get_value(item)
                                elif 'DOB' in item:
                                    dob = get_value(item)
                                elif 'Color' in item:
                                    color = get_value(item)
                                elif 'Gender' in item:
                                    gender = get_value(item)
                                elif 'Ready' in item:
                                    ready = get_value(item)
                        with open(forSalePath + "/" + x, "rb") as f:
                            data = base64.b64encode(f.read())
                            obj.create_database(name=name, price=price, dob=dob, color=color,
                                                gender=gender, ready=ready, image=data, c=c)
                        print("Added listing for {}".format(name))
                    except:
                        print("Incomplete Listing:  {}".format(x))

            except Exception as e:
                print(e)
                print("{} Not added to database ".format(x))

        # reviews
        obj = ForSaleListing()
        forSalePath = os.getcwd() + "\\static\\Reviews"
        forSalePath = forSalePath.replace("\\", "/")
        for x in obj.load_directory(path=forSalePath):
            try:
                Name = x.replace(".txt", "")
                Review = Date = ''
                with open(forSalePath + "/" + x, "r") as f:
                    file_data = f.readlines()
                    for item in file_data:
                        if 'Review' in item:
                            Review = get_value(item)
                        elif 'Date' in item:
                            Date = get_value(item)
                with open(forSalePath + "/" + x, "rb") as f:
                    data = base64.b64encode(f.read())
                    c.execute("""INSERT INTO Reviews (name, review, date) VALUES (?, ?, ?)""", (Name, Review, Date))
                print("Added review from {}".format(Name))
            except Exception as e:
                print(e)
                print("{} Not added to database ".format(x))

        # sold
        obj = ForSaleListing()
        soldPath = os.getcwd() + "\\static\\images\\Sold"
        soldPath = soldPath.replace("\\", "/")
        for x in obj.load_directory(path=soldPath):
            try:
                if ".jpg" in x:
                    name = x.replace(".jpg", "")
                    with open(soldPath + "/" + x, "rb") as f:
                        data = base64.b64encode(f.read())
                        c.execute("""INSERT INTO Sold (name, img) VALUES (?, ?)""", (name, data))
                        print("Sold {} added to database ".format(x))
            except Exception as e:
                print(e)
                print("{} Not added to database ".format(x))

        # QA
        obj = ForSaleListing()
        qaPath = os.getcwd() + "\\static\\QA"
        qaPath = qaPath.replace("\\", "/")
        for x in obj.load_directory(path=qaPath):
            try:
                Name = x.replace(".txt", "")
                Question = Answer = ''
                with open(qaPath + "/" + x, "r") as f:
                    file_data = f.readlines()
                    for item in file_data:
                        if 'Question' in item:
                            Question = get_value(item)
                        elif 'Answer' in item:
                            Answer = get_value(item)
                c.execute("""INSERT INTO QA (name, question, answer) VALUES (?, ?, ?)""", (Name, Question, Answer))
                print("Added review from {}".format(Name))
            except Exception as e:
                print(e)
                print("{} Not added to database ".format(x))
        con.commit()
    except Exception as e:
        print(e)

    # remove duplicates
    stmt = "DELETE FROM ForSale WHERE rowid NOT IN (SELECT min(rowid) FROM ForSale GROUP BY name, dob);"
    c.execute(stmt)
    stmt = "DELETE FROM Sold WHERE rowid NOT IN (SELECT min(rowid) FROM Sold GROUP BY name);"
    c.execute(stmt)
    stmt = "DELETE FROM Reviews WHERE rowid NOT IN (SELECT min(rowid) FROM Reviews GROUP BY name);"
    c.execute(stmt)
    stmt = "DELETE FROM QA WHERE rowid NOT IN (SELECT min(rowid) FROM QA GROUP BY name);"
    c.execute(stmt)
    stmt = "DELETE FROM FunFacts WHERE rowid NOT IN (SELECT min(rowid) FROM FunFacts GROUP BY fact);"
    c.execute(stmt)
    stmt = "DELETE FROM Inquiries WHERE rowid NOT IN (SELECT min(rowid) FROM Inquiries GROUP BY email);"
    c.execute(stmt)

    # set default values
    cur2 = con.execute("SELECT name, requests FROM ForSale")
    for row1 in cur2.fetchall():
        hogletTmp = row1[0]

        tmp = con.execute("UPDATE ForSale SET requests=0 ")


    con.commit()

## START FUNCTION
if __name__ == '__main__':
    popDatabase()
    app.run(debug=True)

