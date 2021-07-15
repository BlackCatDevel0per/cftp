from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import os
import tar_progress as tar
from threading import Thread
from time import sleep

APP_DIR = 'testftp'
# The port the FTP server will listen on.
# This must be greater than 1023 unless you run this script as root.
FTP_HOST = "0.0.0.0"
FTP_PORT = 2221

# The name of the FTP user that can log in.
FTP_USER = "android"

# The FTP user's password.
FTP_PASSWORD = "android"

# The directory the FTP user will have full read/write access to.
FTP_DIRECTORY = "."

os.chdir(APP_DIR)

def extract_on_stor():
  while True:
    sleep(5)
    
    if os.path.isfile('tmpmeta'):
      print ("PASS!")
      tar.extract("storfiles.tar.gz")
      os.remove("tmpmeta")
      os.remove("storfiles.tar.gz")
    else:
      pass
      #print ("Waiting..")

def main():
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    #handler.banner = "pyftpdlib based ftpd ready."

    # Optionally specify range of ports to use for passive connections.
    #handler.passive_ports = range(60000, 65535)

    address = (FTP_HOST, FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()

if __name__ == '__main__':
  Thread(target = main).start()
  Thread(target = extract_on_stor).start()