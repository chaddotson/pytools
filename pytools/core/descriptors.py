
class Attribute(object):
    def __init__(self, name="", types=None, default=None, *args, **kwargs):
        self._valid_types = types if type(types) is list or types is None else [types]

        print("name", name,"-", default, "-",types, "-", args, "-",kwargs)
        self._name = "__" + name

        if default is not None:
            self._assert_valid(default)

        self._default = default

    def __set__(self, instance, value):

        self._assert_valid(value)

        setattr(instance, self._name, value)

    def __get__(self, instance, owner):

        if self._default is None:
            return getattr(instance, self._name)
        else:
            return getattr(instance, self._name, self._default)

    def __delete__(self, instance):
        delattr(instance, self._name)

    def _assert_valid(self, value):
        if type(value) not in self._valid_types:
            raise TypeError("{value} is not a valid type.  Must be {valid_types}".format(value=value, valid_types=self._valid_types))


class IntAttribute(Attribute):
    def __init__(self, *args, **kwargs):
        super(IntAttribute, self).__init__(*args, types=int, **kwargs)


class FloatAttribute(Attribute):
    def __init__(self, *args, **kwargs):
        super(FloatAttribute, self).__init__(*args, types=float, **kwargs)


class NumberAttribute(Attribute):
    def __init__(self, *args, **kwargs):
        super(NumberAttribute, self).__init__(*args, types=[int, float], **kwargs)



class StringAttribute(Attribute):
    def __init__(self, max_length=None, *args, **kwargs):
        self._max_length = max_length
        super(StringAttribute, self).__init__(*args, types=str, **kwargs)

    def _assert_valid(self, val):
        super(StringAttribute, self)._assert_valid(val)

        if self._max_length is not None and len(val) > self._max_length:
            raise TypeError("length must be <={0}".format(self._max_length))
