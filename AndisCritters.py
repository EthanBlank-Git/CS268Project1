import base64

from flask import Flask, render_template, request, flash
import sqlite3 as sql
import os
import unicodecsv
import sys

app = Flask(__name__)
app.secret_key = 'development key'




@app.route('/')
def home():
    return render_template("index.html")


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

    #for row in rows:
    #    print(row)

    return render_template("forsale.html", rows=rows)


@app.route('/Sold')
def sold():
    return render_template("sold.html")


@app.route('/Care')
def care():
    return render_template("care.html")


@app.route('/Q&A')
def questionsAndAnswers():
    return render_template("questionsandanswers.html")


@app.route('/FunFacts')
def funFacts():
    return render_template("funfacts.html")


@app.route('/Contact')
def contact():
    return render_template("contact.html")


@app.route('/Reviews')
def reviews():
    return render_template("reviews.html")


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

def getForSale(con, c):
    # drop table
    try:
        stmt = "DROP TABLE ForSale"
        c.execute(stmt)
    except Exception as e:
        print(e)
    # create table
    try:
        stmt = "CREATE TABLE ForSale (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price TEXT NOT NULL, dob TEXT NOT NULL, color TEXT NOT NULL, gender TEXT NOT NULL, ready TEXT NOT NULL, img TEXT NOT NULL);"
        c.execute(stmt)
        con.commit()
    except Exception as e:
        print(e)

    # populate table
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
                except :
                    print("Incomplete Listing:  {}".format(x))

        except Exception as e:
            print(e)
            print("{} Not added to database ".format(x))

    # return table results
    con.row_factory = sql.Row
    stmt = "select * from ForSale"
    c.execute(stmt)

    return c.fetchall()

def get_value(item):
    info = item.strip().split(':')
    val = info[1].strip().split(',')
    return val[0].strip()

if __name__ == '__main__':
    app.run(debug=True)
