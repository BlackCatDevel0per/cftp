import os, configparser

def file_extensionsort(fn):
  #filenames = fn
  config = configparser.ConfigParser()
  config.read("settings.ini")
  ext = config["TAR_COMPRESS_EXTENSION"]['video']
  for n in fn:
    total = 0
    file_name = n.split('.')
    file_ext = file_name[1::]
    if file_ext == ['mp4']:
      total = total+1
      print('TAR!')
    else:
      print('NOT TAR!')



  print(total)
  print(ext)
  print(fn)

fn = ['file.txt', 'file.mp4', 'file.avi', 'file.html', 'file.css', 'file.js', 'file.py', 'file.mkv', ]
file_extensionsort(fn)