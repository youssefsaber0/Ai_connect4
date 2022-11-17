from flask import Flask
from flask_cors import CORS
import json
from time import time_ns

from server.endpoints.Bot import Bot
from endpoints.ResponseExceptions import *

def micros() -> int:
  return int(time_ns() / 1000)

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def botDecision():
  try:
    endpoint = Bot()
  
  except BadRequest:
    return "Invalid Parameters", 400

  except Exception:
    return "Fail", 500

  state, scores = endpoint.handle()

  return json.dumps({
    'state': state,
    'scores': scores,
    ''
  })

app.run()