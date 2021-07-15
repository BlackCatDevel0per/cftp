from ftplib import FTP
import tar_progress as tar
from tqdm import tqdm
import os

def storfile(user, passwd, host, port, filenames, transferdir='.'):
  tmpfile = "storfiles.tar.gz"
  tmpmeta = "tmpmeta"
  tar.compress(tmpfile, filenames)
  
  ftp = FTP()
  ftp.connect(host, port)
  ftp.login(user, passwd)
  ftp.cwd(transferdir)
  ###
  f1 = open(tmpfile, "rb")
  f2 = open(tmpmeta, "rb")
  ###
  filesize = os.path.getsize(tmpfile)
  tqdm_instance = tqdm(desc = "Uploading..", total = filesize, unit = 'b')
  ###
  ftp.storbinary("STOR "+ tmpfile, f1, callback = lambda sent: tqdm_instance.update(len(sent)))
  ftp.storbinary("STOR "+ tmpmeta, f2)
  ###
  ftp.close()
  f1.close()
  f2.close()
  os.remove(tmpfile) # Remove tmpfile from client device
  #os.remove(tmpmeta)