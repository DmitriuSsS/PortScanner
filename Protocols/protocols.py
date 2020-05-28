import binascii
import re


class Protocols:
    # https://habr.com/ru/post/346098/
    _dns_query = binascii.unhexlify(
        "AA AA 01 00 00 01 00 00 00 00 00 00 07 65 78 61 6d 70 6c 65 03 63 6f 6d 00 00 01 00 01".replace(" ", "")
    )

    queries = {
        "TCP": {
            "DNS": _dns_query,
            "SMTP": b"EHLO dima.example.org\r\n",
            "HTTP": b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n",
            "POP3": b"USER dima\r\n"
        },
        "UDP": {
            "DNS": _dns_query
        }
    }

    @staticmethod
    def get_protocol(data: bytes) -> str:
        if data.startswith(b"HTTP"):
            return "HTTP"
        elif re.match(br"[0-9]{3}", data[:3]):
            return "SMTP"
        elif data.startswith(binascii.unhexlify("AAAA")):
            return "DNS"
        elif data.startswith(b"+"):
            return "POP3"
        else:
            return ""
