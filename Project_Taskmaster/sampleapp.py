from flask import Flask

#defining an application. 
#make sure that you use the name clearly
revathi_app = Flask(__name__)

# defining the URL route
@revathi_app.route('/revathi/')
#creating a function for the respective URL
def show_hello():
    return "Hello World, My name is Revathi"

@revathi_app.route('/')
def say_hi_to_dinesh():
    return "hello Dinesh"

# making sure that the program is 
# the main program and not imported
if __name__ == "__main__":
    revathi_app.run(debug=True)





