from ftplib import FTP
import tar_progress as tar
from sort import file_extensionsort as c2
from tqdm import tqdm
import os, configparser


def storfile(user, passwd, host, port, filenames, transferdir='.'):
  c2c = c2(filenames) # sort
  tmpdir = "tmp"
  if c2c=="TAR":
    tmpfile = "tmp/storfiles.tar"
  elif c2c=="TGZ":
    tmpfile = "tmp/storfiles.tar.gz"
  tmpmeta = "tmp/tmpmeta"
  ### File names tmp
  tmpfilename = tmpfile.replace("tmp/", "")
  tmpmetaname = "tmpmeta"
  ### Compress data
  tar.compress(tmpfile, filenames, c2c)
  
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