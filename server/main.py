from flask import Flask
from flask_cors import CORS
import json
from time import time_ns

from endpoints.AStar import AStar
from endpoints.ResponseExceptions import *
from endpoints.XFS import DFS, BFS

def micros() -> int:
  return int(time_ns() / 1000)

app = Flask(__name__)
CORS(app)

@app.route("/dfs", methods=['GET'])
def dfs_endpoint():
  try:
    start = micros()
    endpoint = DFS()
    time_taken = micros() - start
  
  except BadRequest:
    return "Invalid Parameters", 400

  except Exception:
    return "Fail", 500

  success, states, actions, explored, depth = endpoint.handle()

  if success:
    return json.dumps({
      'time_taken': time_taken,
      'states': states,
      'actions': actions,
      'explored': explored,
      'depth': depth
    })
  else:
    return "No Solution"

@app.route("/bfs", methods=['GET'])
def bfs_endpoint():
  try:
    start = micros()
    endpoint = BFS()
    time_taken = micros() - start

  except BadRequest:
    return "Invalid Parameters", 400

  except Exception:
    return "Fail", 500

  success, states, actions, explored, depth = endpoint.handle()

  if success:
    return json.dumps({
      'time_taken': time_taken,
      'states': states,
      'actions': actions,
      'explored': explored,
      'depth': depth
    })
  else:
    return "No Solution"

@app.route("/a-star", methods=['GET'])
def a_star():
  try:
    start = micros()
    endpoint = AStar()
    time_taken = micros() - start
  
  except BadRequest:
    return "Invalid Parameters", 400

  except Exception:
    return "Fail", 500

  success, states, actions, explored, depth = endpoint.handle()

  if success:
    return json.dumps({
      'time_taken': time_taken,
      'states': states,
      'actions': actions,
      'explored': explored,
      'depth': depth
    })
  else:
    return "No Solution"

@app.errorhandler(404)
def pageNotFound(e):
  return "Invalid path<br><br>Available paths:<br>&nbsp;&nbsp;/a-star => requires 9-digit \"state\" of different numbers and a \"heueristic\" method (euclidean_distance, manhattan_distance)<br>&nbsp;&nbsp;/dfs => requires 9-digit \"state\" of different numbers<br>&nbsp;&nbsp;/bfs => requires 9-digit \"state\" of different numbers"

app.run()