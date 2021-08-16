import threading
from collections import namedtuple

import sha256
from reporter import Reporter

HashResult = namedtuple("HashResult", ("type", "hash"))

class HashThread(threading.Thread):
  def __init__(self, queue, name='hash-thread'):
    super().__init__(name=name)
    self.queue = queue
    self.hash_string = None
    self.hash_file = None
    self.hash_algorithm = None
    self.running = True
    self.start()

  def run(self):
    print("Hashing thread started...")
    while self.running:
      if self.hash_algorithm != None and (self.hash_file != None or self.hash_string != None):
        if self.hash_algorithm == "SHA256":
          self.sha256()
        elif self.hash_algorithm == "SHA3":
          self.sha3()
        else:
          print("Unrecoginized hash algorithm " + self.hash_algorithm + ".")
        
        # Clean up after hashing
        self.hash_algorithm = None
        self.hash_file = None
        self.hash_string = None

  def close(self):
    self.running = False
    print("Thread stop has been requested. Please wait for current hashing to finish.")

  """
    Calculate sha256 of the value in the string field 
  """
  def sha256(self):
    if self.hash_string != None:
      to_hash = self.hash_string
      hash_result = HashResult("String", sha256.hash_string(to_hash))
      self.queue.put(hash_result)
    elif self.hash_file != None:
      reporter = Reporter(self.queue)
      to_hash = self.hash_file
      hash_result = HashResult("File", sha256.hash_file(to_hash, reporter))
      self.queue.put(hash_result)
    else:
      print("SHA256 called without a hash target. Should not happen.")

  def sha3(self):
    print("TODO implement sha3 hashing")