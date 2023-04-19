import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def make_folders(path):
  if not os.path.isdir(path):
    os.makedirs(path) 