from collections import namedtuple

HashUpdate = namedtuple("HashUpdate", ("type", "value"))

class Reporter:
  def __init__(self, queue):
    self.queue = queue

  def report(self, progress):
    self.queue.put(HashUpdate("Progress", progress))
