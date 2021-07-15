from ftplib import FTP
import tar_progress as tar
from tqdm import tqdm
import os, configparser

def storfile(user, passwd, host, port, filenames, transferdir='.'):
  tmpdir = "tmp"
  tmpfile = "tmp/storfiles.tar.gz"
  tmpmeta = "tmp/tmpmeta"
  ### File names tmp
  tmpfilename = "storfiles.tar.gz"
  tmpmetaname = "tmpmeta"
  ###
  tar.compress(tmpfile, filenames)
  
  ftp = FTP()
  ftp.connect(host, port)
  ftp.login(user, passwd)
  ftp.cwd(tmpdir)
  tmpmetawrite(transferdir, tmpmeta) # write tmpmeta
  ### Open files in binary mode
  f1 = open(tmpfile, "rb")
  f2 = open(tmpmeta, "rb")
  ### Progress bar
  filesize = os.path.getsize(tmpfile)
  tqdm_instance = tqdm(desc = "Uploading..", total = filesize, unit = 'b')
  ###
  ftp.storbinary("STOR "+ tmpfilename, f1, callback = lambda sent: tqdm_instance.update(len(sent)))
  ftp.storbinary("STOR "+ tmpmetaname, f2)
  ###
  ftp.close()
  f1.close()
  f2.close()
  os.remove(tmpfile) # Remove tmpfile from client device
  os.remove(tmpmeta)
  
def tmpmetawrite(transferdir, tmpmeta):
  config = configparser.ConfigParser()
  config['TMPMETA'] = {'decdir': transferdir}
  tmpmetafile = open(tmpmeta, 'w')
  config.write(tmpmetafile)
  tmpmetafile.close()