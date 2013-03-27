#!/usr/bin/env python3

import math
import socket
import select
import struct
import sys
import threading
import time


class TinyControlServer:
    def __init__(self):
        self.host = ''
        self.port = 54321
        self.backlog = 5
        self.size = 16
        self.server = None
        self.threads = []
        
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind((self.host,self.port))
        except socket.error as e:
            if self.server:
                self.server.close()
            print("Could not open socket: ", e.strerror)
            sys.exit(1)
    
    def run(self):
        self.open_socket()
        inputs = [self.server, sys.stdin]
        running = True
        while running:
            inputready,outputready,exceptready = select.select(inputs, [], [])
            for x in inputready:
                if x == self.server:
                    f = open("a.mp3", "rb")
                    c = Client(self.server.accept(), f)
                    c.start()
                    self.threads.append(c)
                elif x == sys.stdin:
                    command = sys.stdin.readline()
                    running = False
        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, client_address, file):
        threading.Thread.__init__(self)
        self.client = client_address[0]
        self.address = clinet_address[1]
        self.file = file
        self.loss = 0
        self.recvset = {}
        self.lastset = 0
        self.tld = 0
        self.initial = -1
        self.size = 1000
        #as of now R is in nanoseconds
        self.R = -1
        self.X = self.size
        self.Xbps = -1
        self.Nofeedback = 2
        self.seq = 1
        
        
    def run(self):
        running = True
        while running:
            if (time.time() - self.lastset - self.Nofeedback) > 0:
                #self.timerExpired()
                pass
            inputs,outputs,excepts = select.select([self.client], [], [])
            for x in inputs:
                y = self.client.recv(16)
                self.feedback(y)
            begin = time.time()
            while (time.time() - begin) < 0.5:
                pps = self.X/1000
                wait = 0.5/pps/2
                pack = formPacket()
                if pack == None:
                    running = False
                else:
                    self.client.send(pack)
                    time.sleep(wait)
            pass
        
    def feedback(self, recv):
        timestamp = struct.unpack("<i", data[0:3])[0]
        elapse = struct.unpack("<i", data[4:7])[0]
        rate = struct.unpack("<i", data[8:11])[0]
        loss = struct.unpack("<i", data[12:15])[0]
        self.loss = loss
        
        #change R if you want it in seconds
        R = time.time()*1000000000 - timestamp*1000000000 - elapse
        if self.R == -1:
            self.R = R
            self.initial = 4000/(R/1000000000)
            self.tld = time.time()
        else:
            self.R = .9*self.R + .1*R
        
        self.Nofeedback = max(4*self.R, 2000/rate)
        
        self.recvset[rate] = time.time()
        keys = self.recvset.keys()
        for x in keys:
            if time.time() - self.recvset[x] > 2*self.R:
                del self.recvset[x]
        
        self.algorithm1()
        
        self.lastset = time.time()
        
        
        pass
    
    def timerExpired(self):
        
        X = max(self.recvset.keys())
        if self.R == -1:
            self.X = max(self.X/2,1000/64)
        elif self.loss == 0:
            self.X = max(self.X/2,1000/64)
        elif self.Xbps > (2*X):
            self.updateLimits(X)
        else:
            self.updateLimits(self.Xbps/2)
        
        self.lastset = time.time()
        pass
    
    def updateLimits(self, lim):
        if lim < 1000/64:
            lim = 1000/64
        self.recvset = {lim/2:time.time()}
        self.algorithm1()
        pass
    
    def algorithm1(self):
        recvlim = 2*max(self.recvset.keys())
        
        if self.loss > 0:
            self.Xbps = 1000/(self.R * math.sqrt(2*self.loss/3) + 12 * math.sqrt(3*self.loss/8) * self.loss * (1 + 32 * self.loss * self.loss))
            self.X = max(min(self.Xbps, recvlim), 1000/64)
        elif (time.time() - self.tld) >= self.R:
            self.X = max(min(2*self.X,recvlim),self.initial)
            self.tld = time.time()
    
    def formPacket(self):
        x = struct.pack("<i", int(self.seq))
        self.seq = self.seq + 1
        y = struct.pack("<i", int(time.time()))
        z = struct.pack("<i", int(self.R))
        p = self.file.read(1000)
        if p == None:
            return None
        else:
            return (x + y + z + p)
        
if __name__ == "__main__":
        tcs = TinyControlServer()
        tcs.run()