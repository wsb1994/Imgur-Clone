from flask import Flask
from endpoints.auth import auth
from endpoints.public_user_info import user_info


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(user_info, url_prefix='/user')

@app.route('/')
def index():
    return "This is an example app"

app.run()