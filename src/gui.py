import tkinter as tk
import tkinter.filedialog
import tkinter.ttk
from tkinter import *
import sys
import queue

from hash_thread import HashThread
from hash_thread import HashResult
from reporter import HashUpdate

class GUI:
  """
    Constructor which initialises the gui environment and creates and configures all contained objects 
  """
  def __init__(self):
    # Init the hashing listener queue and thread
    self.queue = queue.Queue()
    self.hash_thread = HashThread(self.queue)

    # Create gui environment
    self.gui = tk.Tk()
    self.frame = tk.Frame(self.gui)
    self.frame.pack()
    self.frame.columnconfigure(3, minsize=600)

    HASH_TYPES = [
      "SHA256",
      "SHA3"
    ]

    # Create GUI elements
    self.str_selected_hash = StringVar(self.frame)
    self.str_selected_hash.set(HASH_TYPES[0])
    self.hash_type = tk.OptionMenu(self.frame, self.str_selected_hash, *HASH_TYPES)
    # String hashing section
    self.lbl_string_hash = tk.Label(self.frame, text="String:")
    self.in_string_hash = tk.Entry(self.frame, width=50)
    self.btn_hash_string = tk.Button(self.frame, text='Hash', command=self.hash_string)
    self.str_hash_string_result = StringVar(self.frame)
    self.str_hash_string_result.set("---")
    self.lbl_hash_string_result = tk.Label(self.frame, textvariable=self.str_hash_string_result)
    #File hashing section
    self.lbl_file_hash = tk.Label(self.frame, text="File:")
    self.btn_select_hash_file = tk.Button(self.frame, text='Select file', command=self.select_file)
    self.btn_hash_file = tk.Button(self.frame, text='Hash', command=self.hash_file)
    self.str_hash_filename = StringVar(self.frame)
    self.str_hash_filename.set("---")
    self.lbl_hash_filename = tk.Label(self.frame, textvariable=self.str_hash_filename)
    self.str_hash_file_result = StringVar(self.frame)
    self.str_hash_file_result.set("---")
    self.lbl_hash_file_result = tk.Label(self.frame, textvariable=self.str_hash_file_result)
    self.prg_hash_file = tk.ttk.Progressbar(self.frame, length=400)

    # Position GUI elements
    self.hash_type.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    #String hashing section
    self.lbl_string_hash.grid(row=1,column=0, padx=5, pady=5)
    self.in_string_hash.grid(row=1,column=1, columnspan=2, padx=5, pady=5)
    self.lbl_hash_string_result.grid(row=1, column=3, padx=5, pady=5)
    self.btn_hash_string.grid(row=1, column=4, padx=5, pady=5)
    #File hashing section
    self.lbl_file_hash.grid(row=3,column=0, padx=5, pady=5)
    self.show_file_input()
    self.lbl_hash_file_result.grid(row=3, column=3, padx=5, pady=5)
    self.btn_hash_file.grid(row=3, column=4, padx=5, pady=5)

    # Set other gui handlers
    self.gui.protocol("WM_DELETE_WINDOW", self.close)

  """
    Monitor the queue of results from button clicks and when response received handle
  """
  def process_queue(self):
    try:
      msg = self.queue.get(0)
      if type(msg) is HashResult: 
        # Updated the correct label based on result type
        if msg.type == "String":
          self.str_hash_string_result.set(msg.hash)
        elif msg.type == "File":
          self.str_hash_file_result.set(msg.hash)
          self.hide_file_progress()
          self.show_file_input()

        else:
          print("Unrecoginized response type " + msg.type + ".")
      elif type(msg) is HashUpdate:
        if msg.type == "Progress":
          self.prg_hash_file["value"] = (float(msg.value) * 100)
        else:
          print("Unrecoginized update type " + msg.type + ".")
        # Updated message therefore redo queue listener for next update
        self.gui.after(100, self.process_queue)
      else:
        print("Fetched type " + type(msg).__name__ + " from queue. Can't handle.")
    except queue.Empty:
      self.gui.after(100, self.process_queue)

  def hide_file_input(self):
    self.btn_select_hash_file.grid_forget()
    self.lbl_hash_filename.grid_forget()

  def show_file_input(self):
    self.lbl_hash_filename.grid(row=3,column=1, padx=5, pady=5)
    self.btn_select_hash_file.grid(row=3,column=2, padx=5, pady=5)

  def show_file_progress(self):
    self.prg_hash_file.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

  def hide_file_progress(self):
    self.prg_hash_file.grid_forget()

  """
    Select a file and update the StringVar that stores the selected file
  """
  def select_file(self):
    filename = tk.filedialog.askopenfile()
    if filename is not None:
      self.str_hash_filename.set(filename.name)

  """
    Start the gui main loop
  """
  def start(self):
    self.gui.mainloop()

  """
    Function run when hash button clicked. Runs apropriate hash function 
    depending on the choice made by the end user
  """
  def hash_string(self):
    self.hash_thread.hash_algorithm = self.str_selected_hash.get()
    self.hash_thread.hash_string = self.in_string_hash.get()
    self.gui.after(100, self.process_queue)

  def hash_file(self):
    self.hide_file_input()
    self.show_file_progress()
    self.hash_thread.hash_algorithm = self.str_selected_hash.get()
    self.hash_thread.hash_file = self.str_hash_filename.get()
    self.gui.after(100, self.process_queue)

  """
    Exit the program
  """
  def close(self):
    self.hash_thread.close()
    sys.exit()