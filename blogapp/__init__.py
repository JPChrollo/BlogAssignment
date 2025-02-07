from flask import Flask, config

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

