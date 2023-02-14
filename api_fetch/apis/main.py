from db import get_user_data
from flask import Flask, render_template

app = Flask(__name__)
headings = ("first_name","last_name","state","country","email","user_name","password","age","cell")
data = get_user_data()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/table/")
def table_display():
    return render_template('table.html', headings = headings, data = data)

if __name__ == "__main__":
    app.run(debug=True)