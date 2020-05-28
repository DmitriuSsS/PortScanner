import sys

from Parsers.parser import Parser
from Scanners.scanner import TCPScanner


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
        scanner = TCPScanner(args.destination)
        print(f'Начало сканирования с ip = {args.destination}:')
        for port in args.ports:
            print('-' * 30)
            print(f'Сканирование порта {port}:')
            if scanner.scan(port):
                print(f'Порт {port} открыт')
            else:
                print(f'Порт {port} закрыт')


if __name__ == '__main__':
    main()
