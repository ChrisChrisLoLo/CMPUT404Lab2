#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

HOST = 'localhost'
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
  try:
    remote_ip = socket.gethostbyname(host)
    return remote_ip
  except socket.gaierror:
    print('Hostname could not be resolved')
    sys.exit()

def send_data(serversocket, payload):
  try:
    serversocket.sendall(payload.encode())
  except socket.error:
    sys.exit()
  print("payload sent successfully")

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #QUESTION 3
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #bind socket to address
    s.bind((HOST, PORT))
    #listen mode
    s.listen(2)

    host2 = 'www.google.com'
    port2 = 80

    while True:
      conn, addr = s.accept()

      p = Process(target=handle_request, args=(addr,conn,host2,port2))
      p.daemon = True
      p.start()
      print(f'started process {p}')

def handle_request(addr,conn,host2,port2):
  print("Connected by", addr)

  #Recieve data, wait a bit, then send it back
  full_data = conn.recv(BUFFER_SIZE)

  # time.sleep(0.5)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    remote_ip = get_remote_ip(host2)

    s2.connect((remote_ip, port2))
    print(f'Socket Connected to {host2} on ip {remote_ip}')

    print(f'FULL DATA {full_data.decode()}')
    # Send fulldata as payload and shutdow
    send_data(s2, full_data.decode())
    s2.shutdown(socket.SHUT_WR)

    # Accept data
    full_data_2 = b""
    while True:
      data = s2.recv(BUFFER_SIZE)
      if not data:
        break
      full_data_2 += data
    print(full_data_2)

  conn.sendall(full_data_2)
  conn.shutdown(socket.SHUT_WR)
  conn.close()
      
if __name__ == "__main__":
  main()