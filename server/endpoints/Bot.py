from flask import request

from endpoints.IEndpoint import IEndpoint
from endpoints.ResponseExceptions import *

from src.runner import input

class Bot(IEndpoint):
  def __init__(self):
    self.validate()

  def validate(self):
    if request.args.get('state') == None or request.args.get('col') == None:
      raise BadRequest

  def handle(self):
    return input(request.args.get('col'),
      request.args.get('state'),
      5
    )