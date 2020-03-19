from Server import Server

if __name__ == "__main__":

    import sys
    rsListenPort = int(sys.argv[1])


    RS = Server()  # Not sure why I can't access for input
    RS.readDataFromFile("PROJI-DNSRS.txt")

    print(RS.SubLevelDomainName.hostname)

    RS.createSocket(rsListenPort)  # random port filled
    RS.socketBind()

    while True:
        RS.socketAccept()

