import pytest
from linked_list import linked_list


class Test:

    def test_add(self):
        l_list = linked_list([0, 100])
        linked_list.add(0, 50)
        print(l_list)
        linked_list.add(1, 51)
        print(l_list)
        linked_list.add(50, 50)
        print(l_list)
        linked_list.add(103, 50)
        print(l_list)
        try:
            linked_list.add(105, 50)
            assert False
        except Exception:
            assert True

    def test_rm(self):
        l_list = linked_list([0, 100])
        linked_list.remove(50)
        linked_list.remove(60)
        linked_list.remove(2)
        linked_list.remove(1)


if __name__ == '__main__':
    t = Test()
    t.test_add()
    t.test_rm()
    # pytest.main()
