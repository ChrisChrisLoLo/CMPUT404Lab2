import socket, sys

def create_tcp_socket():
  print('Creating socket')
  try:
    # SOCKSTREAM TELLS US WE WANT A TCP SOCKET
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except (socket.error):
    print('failed to create message')
    print(socket.error)
    sys.exit()
  return s

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
  try:
    host = 'localhost'
    end_host = 'www.google.com'
    port = 8001
    payload = f'GET / HTTP/1.0\r\nHost: {end_host}\r\n\r\n'
    buffer_size = 4096

    s = create_tcp_socket()

    remote_ip = get_remote_ip(host)

    s.connect((remote_ip, port))
    print(f'Socket Connected to {host} on ip {remote_ip}')

    # Send and shutdown
    send_data(s, payload)
    s.shutdown(socket.SHUT_WR)

    # Accept data
    full_data = b""
    while True:
      data = s.recv(buffer_size)
      if not data:
        break
      full_data += data
    print(full_data)
  except Exception as e:
    print(e)
  finally:
    # Always close
    s.close()

main()