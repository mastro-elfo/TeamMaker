from uuid import uuid1

def uid():
    """
    @see: https://docs.python.org/3.8/library/uuid.html?highlight=uuid#module-uuid
    """
    return str(uuid1())

class Uid(object):
    """Defines and set a unique id as property
    """

    @property
    def id(self):
        """`id` property, read-only"""
        return self.__id

    def __init__(self, *args, **kwargs):
        self.__id = uid()
        super(Uid, self).__init__(*args,  **kwargs)

    def __eq__(self, other):
        """Implements the `==` operator"""
        return self.id == other.id

    # `!=` is implicit

    def __hash__(self):
        """Implements the `hash` built-in function"""
        return hash(self.id)

if __name__ == '__main__':
    a = Uid()
    b = Uid()
    c = Uid()

    assert isinstance(a, Uid)

    # Force `c` to have the same id as `a`
    c._Uid__id = a.id

    assert a != b
    assert a == c
