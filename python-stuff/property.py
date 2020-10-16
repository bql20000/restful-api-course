class Person:
    def __init__(self, name='Long'):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def del_name(self):
        del self._name

    name = property(get_name, set_name, del_name)


class Person2:
    def __init__(self, new_name='Long'):
        self._name = new_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        self._name = new

    @name.deleter
    def name(self):
        del self._name


me = Person()
me.name = 'hi'
print(me.name)


me = Person2()
me.name = 'hi'
print(me.name)
print(me._name)

