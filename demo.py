#! /usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys

from consts import *
from structure import Node, Triple

__author__ = 'Jayeol Chun'


def read( file):
  lines = []
  with open(file, 'r') as f:
    for line in f.readlines():
      # remove comments, assuming `#` doesn't appear in amr itself
      line = line.strip().split('#')[0]
      if line:
        lines.append(line.strip())
  print(lines)
  return lines

def add_to_tree(tree, triple):
  tree.append(triple)

  # update parent/child links
  triple.src.children.append(triple.tgt)
  triple.tgt.parent = triple.src

def build_tree(lines):
  # list of Triples
  tree = []

  stack = []
  for line in lines:
    if line.startswith("("):
      # node
      line = line[1:]
      node = Node(line)
      stack.append((node, None, []))
    elif line.startswith(":"):
      # edge
      line = line[1:].split()

      rel = line[0]
      if '(' in rel:
        rel = rel[:rel.index('(')]
      parent, _, _ = stack[-1]

      if line[-1].endswith(")"):
        triple = Triple(rel, parent, Node(value=[]))  # empty node
        add_to_tree(tree, triple)
        continue

      if len(line) == 1:
        last = stack[-1]
        stack.append((last[0], rel, []))
      else:
        value = line[1]

        if value.startswith("("):
          node = Node(value[1:])
          stack.append((node, None, []))
        else:
          node = Node(value)

        triple = Triple(rel=rel, src=parent, tgt=node)
        add_to_tree(tree, triple)

    elif line.startswith(")"):
      node, rel, val = stack.pop()
      if val:
        triple = Triple(rel=rel, src=node, tgt=Node(val))
        add_to_tree(tree, triple)
    else:
      # triple cases
      if line.endswith(','):
        line = line[:-1]

      fidx = line.index('(')
      lidx = line.rindex(')')
      rel = line[:fidx]
      src_tgt = line[fidx+1:lidx].split(',')
      src = src_tgt[0].strip()
      tgt = src_tgt[1].strip()
      # line = re.split(r"[(,)]+", line)
      # rel = line[0]
      # src = line[1].strip()
      # tgt = line[2].strip()
      chain_triple = Triple(rel=rel, src=src, tgt=tgt)
      stack[-1][-1].append(chain_triple)

  print(tree)
  return tree

def split_var(line):
  return line.split('/')[0]

def convert(tree):
  """tree as triples"""
  corefs, temps, modals = [], [], []
  modal_vars = []
  for tree_triple in tree:
    rel = tree_triple.rel
    chain_triples = tree_triple.tgt

    if rel == COREF:
      for chain_triple in chain_triples.value:
        src_var = split_var(chain_triple.src)
        tgt_var = split_var(chain_triple.tgt)

        found_chain = None
        for coref_chain in corefs:
          if src_var in coref_chain or tgt_var in coref_chain:
            found_chain = coref_chain
            break

        if not found_chain:
          corefs.append([src_var, tgt_var])
        else:
          if src_var not in found_chain:
            found_chain.append(src_var)
          if tgt_var not in found_chain:
            found_chain.append(tgt_var)

    elif rel == TEMP:
      """TODO (Nov 3, 2019)"""
      pass
    elif rel == MODAL:
      for chain_triple in chain_triples.value:
        chain_rel = chain_triple.rel
        src_var = Node(split_var(chain_triple.src))
        tgt_var = Node(split_var(chain_triple.tgt))

        if src_var not in modal_vars:
          modal_vars.append(src_var)
        else:
          src_var = [v for v in modal_vars if src_var == v][0]

        if tgt_var not in modal_vars:
          modal_vars.append(tgt_var)
        else:
          tgt_var = [v for v in modal_vars if tgt_var == v][0]

        new_chain_triple = Triple(chain_rel, src_var, tgt_var)
        add_to_tree(modals, new_chain_triple)

  root = tree[0].src
  assert root.is_root()
  new_tree = [
    Triple(rel=COREF, src=root, tgt=Node(corefs)),
    Triple(rel=TEMP, src=root, tgt=Node(temps)),
    Triple(rel=MODAL, src=root, tgt=Node(modals))
  ]

  return new_tree

def visualize(chains):
  """TODO (Nov 3, 2019)"""
  print(chains)

if __name__ == '__main__':
  file = sys.argv[1]
  print("* processing", file)
  lines = read(file)
  tree = build_tree(lines)
  chains = convert(tree)
  visualize(chains)
