from abc import ABCMeta, abstractmethod

class IEndpoint(metaclass=ABCMeta):
  @abstractmethod
  def validate():
    """
      Method validates and sanitizes the request parameters
    """
    pass
    
  @abstractmethod
  def handle():
    """
      Method handles the request and returns response
    """
    pass