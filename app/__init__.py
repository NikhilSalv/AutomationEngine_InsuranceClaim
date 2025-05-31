from flask import Flask

app = Flask(__name__)

from app import models  # or routes if you create one
