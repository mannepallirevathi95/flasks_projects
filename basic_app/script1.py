# the IMPORTANT '7 - LINES OF CODE'
# everything will be started after importing 'flask'
from flask import Flask, render_template
# we have to create a variable to store inside a flask application
# app = obj
# Flask() = classname
# __name__ = variable
r_app = Flask(__name__)
# decorator to route  it to a URL either to home page or not
@r_app.route('/')
def home():
    return render_template("home_page.html")

@r_app.route('/about/')
def about():
    return render_template("about.html")

# if particular name of the app is 'main', then it has to run the code 
if __name__ == "__main__":
    r_app.run(debug = True)

# we can add additional pages like about, contact etc...
# but if condition should be executed at the END OF THE LINE
