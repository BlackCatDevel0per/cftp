from cftp import storfile

user = 'user'
passwd = 'password'
host = '0.0.0.0'
port = 2221
filenames = ["testdata", "testdata2", "testdata.tar.gz"] # dir stor
transferdir = 'new' # to dir on ftp server

storfile(user, passwd, host, port, filenames, transferdir)