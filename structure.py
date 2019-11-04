#! /usr/bin/python3
# -*- coding: utf-8 -*-
from consts import *

__author__ = 'Jayeol Chun'


class Triple(object):
  """a Triple in a chain within SST"""
  def __init__(self, rel, src, tgt):
    self._rel = rel
    self._src = src
    self._tgt = tgt

  @property
  def rel(self):
    return self._rel

  @property
  def src(self):
    return self._src

  @property
  def tgt(self):
    return self._tgt

  def __repr__(self):
    return f"\nTriple: {self.rel}(Parent -> {self.src}, Child -> {self.tgt})"

class Node(object):
  """a Node in SST"""
  def __init__(self, value=None):
    # data
    self._value = value

    # immediate relationship
    self.parent = None
    self.children = []

  @property
  def value(self):
    return self._value

  def is_root(self):
    return self.value == ROOT

  def is_terminal(self):
    # has no children
    return not self.children

  def __eq__(self, other):
    if isinstance(other, Node):
        return self.value == other.value
    return False

  def __repr__(self):
    return f"Node: {self.value}"
