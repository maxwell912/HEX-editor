import argparse
from linked_list import linked_list


class hex_red:
    def __init__(self, directory='some_text.txt', line_am=5):
        self.line_am = line_am
        self.dir = directory
        if not os.path.exists(directory):
            open(directory, 'bw').close()

        self.data = linked_list([0, os.path.getsize(directory)])
        self.page_b = list()
        self.page_s = list()
        self.current_page = 0
        self._load()

    def add_string(self, position, s: str):
        for i in range(len(s)):
            self.add_symbol(position + i, s[i])

    def add_symbol(self, position, symbol: str):
        symbol_h = symbol.encode('utf-8')
        with open(self.dir, 'ab') as file:
            file_pos = file.tell()
            linked_list.add(position, file_pos)
            file.write(symbol_h)
        self._load()

    def add_h_symbol(self, position, h_symbol):
        byte = bytes.fromhex(h_symbol)
        self.add_symbol(position, byte.decode('utf-8'))

    def change_string(self, position, string: str):
        for i in range(len(string)):
            self.change_symbol(position + i, string[i])

    def change_symbol(self, position, symbol: str):
        symbol_h = symbol.encode('utf-8')
        with open(self.dir, 'ab') as file:
            file_pos = file.tell()
            linked_list.change(position, file_pos)
            file.write(symbol_h)
        self._load()

    def change_h_symbol(self, position, h_symbol):
        byte = bytes.fromhex(h_symbol)
        self.change_symbol(position, byte.decode('utf-8'))

    def remove_symbol(self, position):
        linked_list.remove(position)
        self._load()

    def remove_string(self, position, length):
        for i in range(length):
            self.remove_symbol(position)

    def show(self):
        print(self)

    def save(self):
        with open(self.dir, 'rb') as old:
            with open('new.txt', 'wb') as new:
                for r in linked_list.range(0, float('inf')):
                    old.seek(r[0], 0)
                    new.write(old.read(r[1] - r[0]))
        os.remove(self.dir)
        os.renames('new.txt', self.dir)
        linked_list.head = None
        self.data = linked_list([0, os.path.getsize(self.dir)])
        self._load()

    def _load(self):
        self.page_s = list()
        self.page_b = list()
        s = self.read_symbols(16 * self.line_am * self.current_page)
        for sym in s:
            self.page_s.append(sym)
            self.page_b.append(bytes(sym, encoding='utf-8').hex())

    def read_symbols(self, start, length=None):
        if length is None:
            length = self.line_am * 16
        s = ''
        with open(self.dir, 'rb') as file:
            for r in linked_list.range(start, length):
                file.seek(r[0], 0)
                for _ in range(r[0], r[1]):
                    sym = file.read(1)
                    if sym[0] > 127:
                        s += '#'
                    else:
                        s += sym.decode('ascii')
        return s

    def next_page(self):
        if len(self.page_s) < self.line_am * 16:
            return
        self.current_page += 1
        self._load()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        self._load()

    def __str__(self):
        s_s = '    ' +\
            '  ' + '  '.join(map(str, range(10))) +\
            '  ' + '  '.join('ABCDEF') + '\n'
        s_b = s_s
        for i in range(self.line_am):
            shift = 16 * (self.current_page * self.line_am + i)
            shift = hex(shift)[2:].rjust(4, '0')
            s_b += '  '.join([shift] + self.page_s[16*i:16*(i+1)]) + '\n'
            s_s += ' '.join([shift] +
                            self.page_b[16 * i:16 * (i + 1)]) + '\n'
        return s_b + '\n' + s_s

    def __del__(self):
        self.data = None


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-doc', '--d', nargs='?',
                        help='Document directory.')
    return parser


if __name__ == '__main__':
    import os

    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.d is not None:
        h = hex_red(namespace.d)
    else:
        h = hex_red()
    print('\n'.join(['exit', 'next', 'prev',
                     'save', 'add pos value', 'rm pos', 'ch pos value',
                     'chH pos value', 'addH pos value']))
    com = input()
    while com != 'exit':
        if com == 'next':
            h.next_page()
        elif com == 'prev':
            h.prev_page()
        elif com == 'save':
            h.save()
        com = com.split(' ')
        if len(com) > 1:
            if len(com[1]) % 2 == 1:
                com[1] = '0' + com[1]
            b = bytes.fromhex(com[1])
            com[1] = int.from_bytes(b, byteorder='little') + 1
        if com[0] == 'add':
            if len(com[2]) == 1:
                h.add_symbol(com[1], com[2])
            elif len(com[2]) > 1:
                h.add_string(com[1], com[2])
        elif com[0] == 'addH':
            h.add_h_symbol(com[1], com[2])
        elif com[0] == 'rm':
            if len(com) == 2:
                h.remove_symbol(com[1])
            elif len(com) > 2:
                h.remove_string(com[1], int(com[2]))
        elif com[0] == 'ch':
            if len(com[2]) == 1:
                h.change_symbol(com[1], com[2])
            elif len(com[2]) > 1:
                h.change_string(com[1], com[2])
        elif com[0] == 'chH':
            h.change_h_symbol(com[1], com[2])
        h.show()
        com = input()

    h.save()
