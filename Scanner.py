import socket
import threading
import argparse

def TryConnect(ip, port, delay, result):
    socketToConnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketToConnect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketToConnect.settimeout(delay)
    try:
        socketToConnect.connect((ip, port))
        result[port] = True
    except:
        result[port] = False



def scan_ports(host_ip, delay, f, t):
    threads = []        
    threadsResults = {}
    r = range(f, t)
    for i in range(2**16):
        threads.append(None)
        threadsResults[i] = False

    for i in r:
        t = threading.Thread(target=TryConnect, args=(host_ip, i, delay, threadsResults))
        threads[i] = t
        t.start()

    for i in r:
        threads[i].join()

    for i in r:
        if threadsResults[i]:
            print(str(i))



def main():
    parser = argparse.ArgumentParser(description='Scans for open TCP ports and prints numbers of open ports')
    parser.add_argument('-ip', type=str, default='213.180.193.1', help='Ip adress that you want to scan')
    parser.add_argument('-d', type=int, default=2, help='Time delay for waiting answer from port')
    parser.add_argument('-f', type=int, default=0, help='Start of range of scanning ports')
    parser.add_argument('-t', type=int, default=2**16, help='End of range of scanning ports')
    args = parser.parse_args()

    scan_ports(args.ip, args.d, args.f, args.t)

if __name__ == "__main__":
    main()