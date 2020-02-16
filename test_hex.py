import os
import pytest
from hex import hex_red


class Test_hex:

    def test_add_s(self):
        h = hex_red('test.txt')
        h.add_symbol(1, 'a')
        h.add_string(2, 'mama mila ramu')
        h.save()
        with open('test.txt') as file:
            s = file.readline()
        assert s == 'amama mila ramu'
        h.remove_string(0, 15)
        h.save()

    def test_remove(self):
        h = hex_red('test.txt')
        h.add_symbol(1, 'a')
        h.add_string(2, 'mama mila ramu')
        h.remove_string(0, 15)
        h.save()
        with open('test.txt') as file:
            s = file.readline()
        assert s == ''

    def test_change(self):
        h = hex_red('test.txt')
        h.add_symbol(1, 'a')
        h.change_symbol(1, 'h')
        h.save()
        with open('test.txt') as file:
            s = file.readline()
        assert s == 'h'
        h.remove_symbol(1)
        h.save()

    def test_save(self):
        h = hex_red('test.txt')
        h.add_symbol(1, 'a')
        h.change_symbol(1, 'h')
        with open('test.txt') as file:
            s = file.readline()
        assert s == 'ah'
        h.save()
        with open('test.txt') as file:
            s = file.readline()
        assert s == 'h'
        h.remove_symbol(1)
        # h.save()
        os.remove('test.txt')


if __name__ == '__main__':
    pytest.main()
