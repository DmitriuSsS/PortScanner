import socket

from Protocols.protocols import Protocols


class TCPScanner:
    def __init__(self, destination: str):
        self._destination = destination
        self._timeout_response = 1e-1
        self.connect_protocol = 'TCP'

    def scan(self, port: int) -> (bool, str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self._timeout_response)

            try:
                sock.connect((self._destination, port))
            except socket.error:
                return False, ""
            else:
                for name in Protocols.queries["TCP"].keys():
                    try:
                        sock.sendall(Protocols.queries["TCP"][name])
                        data = sock.recv(1024)
                        protocol = Protocols.get_protocol(data)
                        if protocol == name:
                            return True, protocol
                    except Exception:
                        continue

        return True, ''


class UDPScanner:
    def __init__(self, destination: str):
        self._destination = destination
        self._timeout_response = 1e-1
        self.connect_protocol = 'UDP'

    def scan(self, port: int) -> (bool, str):

        # проверка доступности
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(self._timeout_response)
            try:
                sock.sendto(bytearray([0, 0, port // 256, port % 256, 0, 64, 0, 0]), (self._destination, port))
                data, _ = sock.recvfrom(1024)
                if data.startswith(bytes([3, 3])):
                    return False, ''
            except socket.timeout:
                pass
            except socket.error:
                return False, ''

        # выяснение протокола
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(self._timeout_response)
            try:
                sock.connect((self._destination, port))
            except socket.error:
                return False, ""
            else:
                for name in Protocols.queries["UDP"].keys():
                    try:
                        sock.sendall(Protocols.queries["UDP"][name])
                        data = sock.recv(1024)
                        protocol = Protocols.get_protocol(data)
                        if protocol == name:
                            return True, protocol
                    except Exception:
                        continue

        return True, ''


class NotSupportedScanProtocol(Exception):
    def __init__(self, protocol):
        self.protocol = protocol

    def __str__(self):
        return f'Встречен неподдерживаемый для сканирования протокол - {self.protocol}'
