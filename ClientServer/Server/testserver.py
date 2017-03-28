import select
import socket
import sys
import threading
global counter

class Server:
    def __init__(self):
        self.host = ''
        self.port = 50001
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        counter = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept(),counter)
                    c.start()
                    counter = counter + 1
                    self.threads.append(c)


                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        # self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self,(client,address),id):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.ides = id

    def run(self):
        running = 1
        while running:
            filename = self.client.recv(self.size)
            filesize = self.client.recv(self.size)
            if filesize == '':
                sys.stdout.write('Koneksi Client-'+ str(self.ides) +' ditutup\n')
                break
            else:
                filesize = int(filesize)

            self.client.send(str(self.ides))
            header = self.client.recv(self.size)
            sys.stdout.write(header)
            with open(filename,'wb+') as writingFile:
                while filesize > 0:
                    data = self.client.recv(self.size)
                    writingFile.write(data)
                    filesize -= len(data)
            message = 'Isi file sudah diterima\n'
            self.client.send(message)
        self.client.close()


if __name__ == "__main__":
    s = Server()
    s.run()