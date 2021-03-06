import argparse


class Parser(argparse.ArgumentParser):
    @staticmethod
    def _check_destination(ip: str):
        parts = ip.split('.')
        if len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts):
            return ip
        raise argparse.ArgumentTypeError(f'Неверное IP адрес: {ip}')

    @staticmethod
    def _check_port(port):
        _port = int(port)

        if 1 <= _port <= 65535:
            return _port
        raise argparse.ArgumentTypeError(f'Неверный порт: {port}')

    def do_settings(self):
        self.description = 'Утилита для сканирования TCP и UDP портов. ' \
                           'Автор: Шимаев Дмитрий, КН203(МЕН280208)'

        self.add_argument('-d', '--destination', type=self._check_destination,
                          help='IP адрес для сканирования', default='127.0.0.1')
        self.add_argument("-t", "--tcp", help="Сканирование TCP портов", action='store_true', default=False)
        self.add_argument("-u", "--udp", help="Сканирование UDP портов", action='store_true', default=False)
        self.add_argument('-p', '--ports', help='Порты для сканирования', nargs='+', type=self._check_port)
