from DomainName import DomainName
import socket
import sys


class Server ():

    domainNameList = []
    SubLevelDomainName = None

    #Below function creates a socket for server
    def createSocket(self, portno):
        print("Creating a socket\n")
        try:
            global host
            global port
            global serverSocket
            host = ''
            port = portno

            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error as err:
            print('socket could not be opened: {}\n'.format(err))
            exit()

    #Below function binds socket to port
    def socketBind(self):
        try:
            global host
            global port
            global serverSocket
            print("Binding socket to port: " + str(port))

            serverSocket.bind((host, port))
            serverSocket.listen(1)

        except socket.error as err:
            print("Server could not bind: error " + str(err))
            Server.socketBind(self) #trying to include recursion --> idk about syntax

    #Below function accepts connection from client --> SOCKET SHOULD NOT BE ENDED If connection is dropped
    def socketAccept(self):
        conn, address = serverSocket.accept()
        print("Connection has been establish: @ IP: " + str(address[0]) + " | " + "port: " + str(address[1]))
        try:
            while True:
                #is the following correct
                client_response = conn.recv(1024).decode('utf-8') # Following does not work in python 2.7!!
                #print(client_response)
                conn.send(Server.searchDNL(self, client_response).encode('utf-8'))

        except:
            print("Connection Disconnecting!")
            conn.close()

    def readDataFromFile(self, fileName="PROJI-DNSRS.txt"):
        File = open(fileName, "r")
        for line in File:

            tokens = line.split()  # This splits line into tokens to be put into domain info
            domainInfo = DomainName(tokens[0], tokens[1], tokens[2])  # This is the domain information
            #print("Domain Info:", domainInfo.hostname, domainInfo.IP, domainInfo.flag)

            if domainInfo.flag == "A":
                self.domainNameList.append(domainInfo)
            elif domainInfo.flag == "NS":
                self.SubLevelDomainName = domainInfo


    def searchDNL(self, client_response):
            for domainInfo in self.domainNameList:
                if (client_response == domainInfo.hostname):
                    output = "{} {} {}".format(domainInfo.hostname, domainInfo.IP, domainInfo.flag)
                    return output

            if self.SubLevelDomainName == None:
                return "{} - ERROR:HOST NOT FOUND".format(client_response)
            else:
                TSHostResponse = "{} {} {}".format(self.SubLevelDomainName.hostname, self.SubLevelDomainName.IP, self.SubLevelDomainName.flag)
                return TSHostResponse





#First try to create new server, connect with client, and send basic messages back and forth
if __name__ == "__main__":

    newServer = Server() #Not sure why I can't access for input
    newServer.readDataFromFile("PROJI-DNSRS.txt")

    print(newServer.SubLevelDomainName.hostname)

    newServer.createSocket(5018) #random port filled
    newServer.socketBind()
    while True:
        newServer.socketAccept()








#TODO
'''
X 1) Need to keep server running for as many clients I create --> right now server ends when I create a client
X 2) be able to search for client queries and send back to client 
X 3) Root and TS should be connected 

X If RS --> Need to find way to pass hostname of TS to RS
X Server should not end when connection is closed 
Accept multiple client connections? --> could use threads???? 

Connection is ending automatically in terminal --> Fix bug!! 
Case Insensitive



CONVERT TO PYTHON 2.7   
'''
