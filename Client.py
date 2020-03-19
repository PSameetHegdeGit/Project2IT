
import socket


'''
Only output if received A tag

'''

class Client:

    #need to pass command line arguments in

    def __init__(self, rsHostname, rsPort, tsPort, tsHostname=None,  request=None):
        self.rsHostname = rsHostname
        self.tsHostname = tsHostname
        self.rsPort = rsPort
        self.tsPort = tsPort
        self.request = request


    #Below function creates a client socket
    def createClientSocket(self, port, hostname):
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM means "use TCP protocol"
            #print("\n[C]: client socket created")
        except socket.error as err:
            print('socket open error: {}\n'.format(err))
            exit()

        host_addr = socket.gethostbyname(hostname) #gethostbyname translates hostname given by socket.gethostname() ~ or is passed in into IPV4 format

        clientSocket.connect((host_addr, port)) #since both client and server r on same host, localhost_addr should be fine
        #print("Client has successfully connected!\n")

        return clientSocket

       # Client.client_requests(self, clientSocket)


    #Below Function handles a Client request
    saveFile = open('RESOLVED.txt', 'w')
    saveFile.write("RESULTS\n")
    saveFile.close()
    def client_request(self, clientSocket, serverType="RS"):


        if serverType == "RS":
            self.request = raw_input("What would you like to request: ") #Raw_Input for python 2.7 and input for python 3 and above
            if self.request == "quit":
                exit()

        self.request = self.request.lower() #make it lower case
        clientSocket.send(self.request.encode('utf-8'))
        server_response = clientSocket.recv(1024).decode('utf-8')

        hostname, IP, flag= server_response.split(' ', 2)
        if flag == "A":
            print(server_response + "\n")
            saveFile = open('RESOLVED.txt', 'a')
            saveFile.write("\n" + server_response)
            saveFile.close()
            return "In Server"

        elif flag== "NS":
            self.tsHostname = hostname
            return "Check TS"

        elif flag == "ERROR:HOST NOT FOUND":
            print(hostname + " ERROR:HOST NOT FOUND\n")
            saveFile = open('RESOLVED.txt', 'a')
            saveFile.write("\n" + hostname + " ERROR:HOST NOT FOUND")
            saveFile.close()






if __name__ == "__main__":

    import sys

    #rshostname, rsPort, tsPort = input("Enter rsHostname, rsPort, tsPort:").split()
    rshostname = sys.argv[1]
    rsPort = sys.argv[2]
    tsPort = sys.argv[3]

    #print "{} {} {}".format(rshostname, rsPort, tsPort) #Just to check

    newClient = Client(rshostname, int(rsPort), int(tsPort))

    clientSocketRS = None
    clientSocketTS = None

    while True:
        #print("Attempting to Connect with RS... ")
        clientSocketRS = newClient.createClientSocket(newClient.rsPort, newClient.rsHostname)

        while True:
            retVal = newClient.client_request(clientSocketRS)

            if retVal == "Check TS":
                clientSocketRS.close()
                #print("Not in RS. Checking TS...")
                clientSocketTS = newClient.createClientSocket(newClient.tsPort, newClient.tsHostname)
                newClient.client_request(clientSocketTS, "TS")
                clientSocketTS.close()
                break











'''
 #Do we need way to end client program (or do we just ctrl + C it?
'''

