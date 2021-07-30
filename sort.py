import os, configparser

def get_filenames(dirname): # Get filenames in dirs, only dirs
  dn = os.walk(dirname)
  for root, dirs, files in dn:
    pass
  return files

def get_filelist(dirname): # Get file path list
  filelist =[]
  dn = os.walk(dirname)
  for root, dirs, files in dn:
    for file in files:
      filelist.append(os.path.join(root,file))
  return filelist
      
def get_dirsize(dirname): # Get dir size
  totalsize = 0
  dn = os.walk(dirname)
  for root, dirs, files in dn:
    for f in files:
      fp = os.path.join(root, f)
      fs = os.path.getsize(fp)/1024
      fsi = round(fs)
      totalsize+=fsi
  return totalsize

def config_parse(arch, ext): # Parse settings.ini
  config = configparser.ConfigParser()
  config.read("settings.ini")
  if arch == "tar":
    a = "TAR"
  elif arch == "tgz" or "tar.gz":
    a = "TGZ"
  ex1 = config[a + "_COMPRESS_EXTENSIONS"][ext]
  extname = ex1.split(sep=None, maxsplit=-1)
  return extname
  
def file_sizesort():
  pass
def file_extensionsort(fn):
  #filenames = fn
  ###
  TAR = "TAR"
  TGZ = "TGZ"
  ###
  config = configparser.ConfigParser()
  config.read("settings.ini")
  ###
  tmpsize = config["TMP_SIZE"]["tmpsize"]
  audio = config_parse(arch="tar", ext="audio")
  photo = config_parse(arch="tgz", ext="photo")
  video = config_parse(arch="tar", ext="video")
  text = config_parse(arch="tgz", ext="text")
  ###
  tarcom = video + audio
  tgzcom = text + photo
  ###
  totalsize = 0 # total data size
  totalcount = 0 # total files count
  total2tar = 0 # total files to tar compressing
  total2tgz = 0 # total files to tar with gzip compressing
  totalunextfiles = 0 # unextension files
  
  for n in fn:
    if os.path.isdir(n): # add subdirs files to fn list
      nf = get_filenames(n)
      fn = nf+fn
  
  for n in fn: # Check files extensions
    file_name = n.split('.')
    file_ext = file_name[1::]
    file_ext = "".join(file_ext)
    ###
    # Get total data size in kb
    if os.path.isdir(n):
      totalsize += get_dirsize(n)
      totalcount += len(get_filelist(n)) # total files count in dir 
      
    if os.path.isfile(n):
      fs = os.path.getsize(n)/1024
      fsi = round(fs)
      totalsize += fsi
      totalcount+=1
      if file_ext == "": # if no file extension
        totalunextfiles+=1
    ###
    # Sort to tar & tgz
    for e in tarcom:
      if file_ext == e:
        total2tar+=1
    for e in tgzcom:
      if file_ext == e:
        total2tgz+=1
    ###
  ###
  #print("totalsize: ", totalsize, "kb\ntotalcount", totalcount, " \ntotal2tar: ", total2tar, " \ntotal2tgz: ", total2tgz, " \ntotalunextfiles: ", totalunextfiles)
  #print(fn)
  ###
  if totalsize <= int(tmpsize) and totalcount >= 10 and total2tar >= 10: # if files size <= tmp size in kb and files count >= 10 and file extensions for tar compressing >= 10
    print(TAR)
    return TAR
  
  elif totalsize > int(tmpsize):
    print("Warning! tmp size may not be enough!", " datasize: ", totalsize, ", tmpsize: ", tmpsize)
  
  elif total2tgz >= 10:
    print(TGZ)
    return TGZ
  
  elif totalunextfiles >= 10:
    print("Please sort by size")
  
  elif total2tar == total2tgz:
    print(TGZ)
    return TGZ
  
  elif total2tar > total2tgz:
    print(TAR)
    return TAR
  
  elif total2tar < total2tgz:
    print(TGZ)
    return TGZ
  ###



fn = ['testdata', 'testdata2', 'LICENSE', 'settings.ini']
#fn = ['file', 'file.txt', 'file.mp3', 'file.mp4', 'file.avi', 'file.html', 'file.css', 'file.js', 'file.py', 'file.mkv', ]
file_extensionsort(fn)