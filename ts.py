from Server import Server

if __name__ == "__main__":
    import sys
    tsListenPort = int(sys.argv[1])


    TS = Server()  # Not sure why I can't access for input
    TS.readDataFromFile("PROJI-DNSTS.txt")

    TS.createSocket(tsListenPort)  # random port filled
    TS.socketBind()

    while True:
        TS.socketAccept()
