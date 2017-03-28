import socket
import sys
import os

host = 'localhost'
port = 50001
size = 1024
basedir = "Dataset/"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while 1:
    line = sys.stdin.readline()
    if line == '\n':
        break
    linet = line.strip()
    namafile = linet.split()[1]
    fullpath = basedir+namafile
    if os.path.isfile(namafile) == 1:
        filesize = os.path.getsize(namafile)
        s.send(fullpath)
        s.send(str(filesize))
        ides = s.recv(size)
        header = 'client-id: klien-' + ides + '\n'+'file-size: ' + str(filesize) + '\n \n\n'
        s.send(header)

        with open(namafile, "rb") as f:
            while True:
                l = f.read(size)
                s.send(l)
                if not l:
                    break

        data = s.recv(size)
        sys.stdout.write(data)
    else:
        sys.stdout.write('File not exist\n')
    sys.stdout.write('Continue? Y/N \n')
    answer = sys.stdin.readline()
    if answer == 'N\n':
        break
s.close()