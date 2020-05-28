import socket


class TCPScanner:
    def __init__(self, destination: str):
        self._destination = destination
        self._timeout_response = 1e-1

    def scan(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self._timeout_response)
            try:
                sock.connect((self._destination, port))
            except socket.error:
                return False
            else:
                return True
