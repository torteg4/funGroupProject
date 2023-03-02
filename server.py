from flask_app import app
from flask_app.controllers import users, cards
from distutils.log import debug

if __name__=="__main__":
    app.run(debug=True)