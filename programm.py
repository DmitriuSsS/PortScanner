import sys
import threading
from typing import List

from Parsers.parser import Parser
from Scanners.scanner import TCPScanner, UDPScanner


def _scan_port(scanner, port: int) -> None:
    (can_connect, protocol) = scanner.scan(port)
    if can_connect:
        if protocol:
            print(f'{scanner.connect_protocol}: порт {port} работает с {protocol} протоколом')
        else:
            print(f'{scanner.connect_protocol}: порт {port} открыт и работает с нераспознанным протоколом')
    else:
        print(f'{scanner.connect_protocol}: порт {port} закрыт')


def scan(ports: List[int], protocol: str, destination: str):
    if protocol == 'TCP':
        scanner = TCPScanner(destination)
    elif protocol == 'UDP':
        scanner = UDPScanner(destination)
    else:
        print('Неопознанный протокол для сканирования')
        return
    print(f'Начало сканирования портов протокола {protocol} с ip = {destination}:')

    threads = []
    for port in ports:
        threads.append(threading.Thread(target=_scan_port, args=(scanner, port)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def main():
    parser = Parser()
    parser.do_settings()
    if len(sys.argv) == 1:
        parser.parse_args(['-h']).function()
    else:
        args = parser.parse_args()
        if not args.ports:
            print('Необходимо ввести порты для сканирования')
            return

        tcp = args.tcp
        udp = args.udp
        if not (tcp or udp):
            tcp, udp = True, True

        if tcp:
            scan(args.ports, 'TCP', args.destination)
        if udp:
            scan(args.ports, 'UDP', args.destination)


if __name__ == '__main__':
    main()
