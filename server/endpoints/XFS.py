from flask import request

from endpoints.IEndpoint import IEndpoint
from endpoints.ResponseExceptions import *

from Node import Node, solution
from xfs import xfs

class XFS(IEndpoint):
  def __init__(self):
    self.validate()
    self.type = ""

  def validate(self):
    if request.args.get('state') == None:
      raise BadRequest

  def handle(self):
    start = Node(state=int(request.args.get('state')))
    final_node, explored, depth = xfs(self.type, start)
    if not final_node:
      return False, None, None, None, None
    _, states, actions = solution(final_node)

    return True, states, actions, explored, depth

class DFS(XFS):
  def __init__(self):
    super().__init__()
    self.type = "dfs"

class BFS(XFS):
  def __init__(self):
    super().__init__()
    self.type = "bfs"