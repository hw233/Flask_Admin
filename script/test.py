#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_test
Filename: test.py
Author: ronnyzh
Date: 2020-03-05 14:53
Revision: $Revision$
Description: $Description$
"""

from collections import namedtuple
from math import hypot


class Vector(object):
    # 基本定制型
    def __new__(cls, *args, **kwargs):
        """构造器"""
        return super(Vector, cls).__new__(cls)

    def __init__(self, x=0, y=0):
        """构造器：通常用在设置不可变数据类型的子类"""
        self.x = x
        self.y = y
        self.z = list(range(1, 11))

    def __del__(self):
        """解构器"""
        pass

    def __str__(self):
        """可打印的字符串输出： 内建str()及print语句"""
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def __repr__(self):
        """运行时的字符串输出： 内建repr()及 ' ' 操作符"""
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def __unicode__(self):
        """Unicode字符串输出： 内建unicode()"""
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def __call__(self, *args, **kwargs):
        """表示可调用的实例"""
        pass

    def __nonzero__(self):
        """为object定义False值： 内建bool()"""
        pass

    def __len__(self):
        """长度（可用于类）： 内建len()"""
        return len(self.z)

    # 对象（值）比较
    def __cmp__(self, other):
        """对象比较： 内建cmp()"""
        pass

    def __lt__(self, other):
        """小于/小于或等于： 对应<及<=操作符"""
        pass

    def __gt__(self, other):
        """大于/大于或等于： 对应>及>=操作符"""
        pass

    def __eq__(self, other):
        """等于/不等于： 对应==, != 及 <>操作符"""
        pass

    # 属性
    def __getattr__(self, item):
        """获取属性： 内建getattr()： 仅当属性没有找到时调用"""
        return getattr(self.z, item)

    def __setattr__(self, key, value):
        """设置属性"""
        return setattr(self.z, key, value)

    def __delattr__(self, item):
        """删除属性"""
        return delattr(self.z, item)

    def __getattribute__(self, item):
        """获取属性： 内建getattr(): 总是被调用"""
        return getattr(self.z, item)

    def __get__(self):
        """描述符： 获取属性"""
        pass

    def __set__(self, instance, value):
        """描述符： 设置属性"""
        pass

    def __delete__(self, instance):
        """描述符： 删除属性"""
        pass

    # 定制类/模拟类型
    # 数值类型： 二进制操作符
    def __add__(self, other):
        """加： + 操作符"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """减： - 操作符"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """乘： * 操作符"""
        return Vector(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        """True 除： / 操作符"""
        return Vector(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        """Floor 除： // 操作符"""
        return Vector(self.x // other.x, self.y // other.y)

    def __mod__(self, other):
        """取模/取余： % 操作符"""
        return Vector(self.x % other.x, self.y % other.y)

    def __divmod__(self, other):
        """除和取模： 内建divmod()"""
        return divmod(self.x, other.x), divmod(self.y, other.y)

    def __pow__(self, power, modulo=None):
        """乘幂： 内建pow()： **操作符"""
        return Vector(pow(self.x, power), pow(self.y, power))

    def __lshift__(self, other):
        """左位移： << 操作符"""
        pass

    def __rshift__(self, other):
        """右位移： >> 操作符"""
        pass

    def __and__(self, other):
        """按位与： & 操作符"""
        return Vector(self.x, self.y) & Vector(other.x, other.y)

    def __or__(self, other):
        """按位或： | 操作符"""
        return Vector(self.x, self.y) | Vector(other.x, other.y)

    def __xor__(self, other):
        """按位与或： ^ 操作符"""
        return Vector(self.x, self.y) ^ Vector(other.x, other.y)

    # 数值类型： 一元操作符
    def __neg__(self):
        """一元负"""
        pass

    def __pos__(self):
        """一元正"""
        pass

    def __abs__(self):
        """绝对值： 内建abs()"""
        return hypot(self.x, self.y)

    def __invert__(self):
        """按位求反： ~ 操作符"""
        pass

    # 数值类型： 数值转换
    def __complex__(self):
        """转为complex（复数）： 内建complex()"""
        return compile(self.x)

    def __int__(self):
        """转为int： 内建int()"""
        return int(self.x)

    def __long__(self):
        """转为long： 内建long()"""
        pass

    def __float__(self):
        """转为float： 内建float()"""
        return float(self.x)

    # 数值类型：基本表示法（String)
    def __oct__(self):
        """八进制表示： 内建oct()"""
        return oct(self.x)

    def __hex__(self):
        """十六进制表示： 内建hex()"""
        return hex(self.x)

    # 数值类型： 数值压缩
    def __coerce__(self, other):
        """压缩成同样的数值类型： 内建coerce()"""
        pass

    def __index__(self):
        """在有必要时，压缩可选的数值类型为整型（比如：用于切片索引等）"""
        pass

    # 序列类型
    def __len__(self):
        """序列中项的项目"""
        return len(self.z)

    def __getitem__(self, item):
        """得到单个序列元素"""
        return self.z[item]

    def __setitem__(self, key, value):
        """设置单个序列元素"""
        self.z[key] = value

    def __delitem__(self, key):
        """删除单个序列元素"""
        return self.z.pop(key)

    def __setslice__(self, i, j, sequence):
        """设置序列片段"""
        self.z[i:j] = sequence

    def __delslice__(self, i, j):
        """删除序列片段"""
        del self.z[i:j]

    def __contains__(self, item):
        """测试序列成员： 内建in关键字"""
        return item in self.z

    def __add__(self, other):
        """串连： + 操作符"""
        return self.z + other.z

    def __mul__(self, other):
        """重复： * 操作符"""
        return self.z * other.z

    def __iter__(self):
        """创建迭代类： 内建iter()"""
        return iter(self.z)

    # 映射类型
    def __len__(self):
        """mapping中的项的数目"""
        return len(self.z)

    def __hash__(self):
        """散列（hash）函数值"""
        pass

    def __getitem__(self, item):
        """得到给定键（key）的值"""
        pass

    def __setitem__(self, key, value):
        """设置给定键（key）的值"""
        pass

    def __delitem__(self, item):
        """删除给定键（key）的值"""
        pass

    def __missing__(self, key):
        """给定键如果不存在字典中，则提供一个默认值"""
        pass


from math import hypot
from collections import namedtuple, deque
from collections import defaultdict
from collections import OrderedDict
from collections import ChainMap
from collections import Counter
from collections import UserDict
from functools import reduce
from functools import partial
from operator import add
from operator import itemgetter
from operator import attrgetter
from operator import methodcaller
import inspect
import numpy
import traceback
import bisect
import sys
import array
import random
import weakref


class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.z = list(range(1, 11))

    def __repr__(self):
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def __str__(self):
        return 'Vector({0}, {1})'.format(self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)


from collections import namedtuple
from operator import mul

Customer = namedtuple('Customer', 'name fidelity')


class LineItem(object):
    def __init__(self, product, price, quantity):
        self.product = product
        self.price = price
        self.quantity = quantity

    def total(self):
        return mul(self.price, self.quantity)


class Order(object):
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def que(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount


def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def deco(func):
    def inner():
        print('running inner()')
        return func()

    return inner


@deco
def target():
    print('running target()')


from itertools import chain
from array import array
import math


class Vector(object):
    typecode = 'd'
    shortcut_name = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        print('type(self) = {}'.format(cls))
        print('index = {}'.format(index))
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __getattr__(self, item):
        cls = type(self)
        if len(item) == 1:
            pos = cls.shortcut_name.find(item)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        return AttributeError(msg.format(cls, item))

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_name:
                error = 'readonly atribute {attr_name!r}'
            elif name.islower():
                error = 'can"t set attributes "a" to "z" in {cls_name!r}'
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return reduce(xor, hashes, 0)

    def angel(self, n):
        r = math.sqrt(sum(x * x for x in self[:]))
        a = math.atan2(r, self[n - 1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angels(self):
        return (self.angel(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # 超球面坐标
            fmt_spec = fmt_spec[:-1]
            coords = chain([abs(self)],
                           self.angels())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

