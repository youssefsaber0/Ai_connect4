from flask import request

from endpoints.IEndpoint import IEndpoint
from endpoints.ResponseExceptions import *

from Node import Node, solution

class AStar(IEndpoint):
  def __init__(self):
    self.validate()

  def validate(self):
    if request.args.get('state') == None or request.args.get('heueristic') not in ['manhattan_distance', 'euclidean_distance']:
      raise BadRequest

  def handle(self):
    start = Node(state=int(request.args.get('state')))
    final_node, explored, depth = A_star(start, request.args.get('heueristic'))

    if not final_node:
      return False, None, None, None, None

    _, states, actions = solution(final_node)

    return True, states, actions, explored, depth