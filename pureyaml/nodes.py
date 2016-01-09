#!/usr/bin/env python
# coding=utf-8
"""
nodes
"""
from __future__ import absolute_import

import re
from base64 import standard_b64decode
from functools import partial
from math import isnan

from pureyaml.exceptions import YAMLCastTypeError
from ._compat import collections_abc as abc


class Node(object):
    def __init__(self, value, **kwargs):
        self.raw_value = value
        self.value = self.init_value(self, value, **kwargs)

    def init_value(self, *values, **kwargs):
        return values[0]

    def __eq__(self, other):
        try:
            return self.value == other.value and type(self) == type(other)
        except AttributeError:
            return False

    def repr_value(self):
        try:
            return repr(self.value)[1:-1]
        except AttributeError:
            return repr(self.raw_value)[1:-1]

    def __repr__(self):
        cls_name = self.__class__.__name__
        return '<%s:%s>' % (cls_name, self.repr_value())


class SequenceMixin(abc.Sequence):
    value = NotImplemented

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)

    def __contains__(self, x):
        return x in self.value

    def __iter__(self):
        return iter(self.value)


class Collection(SequenceMixin, Node):
    def __init__(self, *values, **kwargs):
        self.raw_value = values
        self.value = self.init_value(*values, **kwargs)

    def init_value(self, *value, **kwargs):
        return value

    def __add__(self, other):
        _Collection = self.__class__

        if not isinstance(other, _Collection):
            self_cls_name, other_cls_name = self.__class__.__name__, other.__class__.__name__
            raise TypeError('%s + %s :: %s + %s' % (self_cls_name, other_cls_name, self, other))

        value = self.value + other.value
        return _Collection(*value)


class Docs(Collection):
    pass


class Doc(Collection):
    pass


class Sequence(Collection):
    pass


class MappingMixin(abc.Mapping):
    value = NotImplemented

    def __getitem__(self, key):
        for k, v in self.value:
            if k == key:
                return v

        raise KeyError('key %s not found in %r' % (key, self))

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        for key, _ in self.value:
            yield key

    def __eq__(self, other):
        return Node.__eq__(self, other)


class Map(MappingMixin, Collection):
    def init_value(self, *values, **kwargs):
        for value in values:
            if len(value) == 2:
                continue

            msg = 'Unexpected Value: %s :: %s values must come in pairs'
            cls_name = self.__class__.__name__
            raise ValueError(msg % (value, cls_name))

        return values


class Scalar(Node):
    type = NotImplemented

    def __init__(self, value, *args, **kwargs):
        self.raw_value = value
        self.value = self.init_value(value, *args, **kwargs)

    def init_value(self, value, *args, **kwargs):
        return self.type(value)


class Null(Scalar):
    type = None

    def init_value(self, *values, **kwargs):
        return None


class Str(Scalar):
    type = str

    def init_value(self, value, *args, **kwargs):
        if value is None:
            return ''
        return super(Str, self).init_value(value, *args, **kwargs)


class Int(Scalar):
    type = int

    def init_value(self, value, base=None, *args, **kwargs):
        if base is not None:
            return self.type(value, base=base)

        return self.type(value)


class Float(Scalar):
    type = float

    def init_value(self, value, *args, **kwargs):
        # Guard, inf and nan
        if isinstance(value, str):
            value_lower = value.lower().replace('.', '')
            if value_lower.endswith('inf'):
                return self.type(value_lower)
            if value_lower.endswith('nan'):
                return self.type(value_lower)

        return self.type(value)

    def __eq__(self, other):
        # Guard, we're not doing math.
        if isnan(self.value) and isnan(other.value):
            return True

        return super(Float, self).__eq__(other)


class Bool(Scalar):
    type = bool
    TRUE_VALUES = ['TRUE', 'YES', '1']
    FALSE_VALUES = ['FALSE', 'NO', '0']

    def init_value(self, value, *args, **kwargs):
        str_value = str(value).upper()
        possible_values = self.TRUE_VALUES + self.FALSE_VALUES
        if str_value not in possible_values:
            cls_name = self.__class__.__name__
            msg = 'Unknown %s value: %r not in %s'
            raise ValueError(msg % (cls_name, value, possible_values))
        return str_value in self.TRUE_VALUES


class Binary(Scalar):
    type = 'binary'

    def init_value(self, value, *args, **kwargs):
        return standard_b64decode(value)


class ScalarDispatch(object):
    map = {  # :off
        'null': Null,
        'bool': Bool,
        'int': Int,
        'int10': partial(Int, base=10),
        'int8': partial(Int, base=8),
        'int16': partial(Int, base=16),
        'float': Float,
        'infinity': Float,
        'nan': Float,
        'str': Str,
        'binary': Binary,
    }  # :on

    re_dispatch = re.compile(r"""
        ^ (?P<null> (?i) null $| ~ $)
        | (?P<bool> (?i) true $| false $| yes $| no $)
        | (?P<int10> [-+]? [0-9]+ $)
        | (?P<int8> 0o [0-7]+ $)
        | (?P<int16> 0x [0-9a-fA-F]+ $)
        | (?P<float>[-+]? (?:
            (?: [0-9]* \. [0-9]+ |  [0-9]+ \. [0-9]* )
                (?: [eE] [-+]? [0-9]+ )? $|
            [0-9]* \.? [0-9]* [eE] [-+]? [0-9]+ ) $
          )
        | (?P<infinity> [-+]? (?: \.inf | \.Inf | \.INF) $)
        | (?P<nan> [-+]? (?: \.nan | \.NaN | \.NAN) $)
        | (?P<str> .+ $)
    """, re.X)

    def __new__(cls, value, cast=None):  # noqa
        # Guard, explicit casting
        if cast is not None:
            try:
                return cls.map[cast](value)
            except KeyError:
                raise YAMLCastTypeError(cast=cast)

        # Guard, already casted
        type_name = type(value).__name__
        if not isinstance(value, str) and type_name in cls.map:
            return cls.map[type_name](value)

        # Guard, empty value
        value = value.strip()
        if value == '':
            return Null(value)

        match = cls.re_dispatch.match(value)
        return cls.map[match.lastgroup](value)
