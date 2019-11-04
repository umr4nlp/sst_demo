#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Jayeol Chun'


# Meta Node(Root) + Edges
ROOT = 'ROOT'
DCT  = 'DCT'
AUT  = 'AUTHOR'
SNT  = 'SNT'

# Chain Nodes
COREF = 'coref'
TEMP  = 'temporal'
MODAL = 'modal'

# Coref Triple Relation
SAME = 'same'

# Temporal Triple Relations
AFTER   = 'after'
BEFORE  = 'before'
OVERLAP = 'overlap'

# Modality Triple Relations
POS   = 'pos' # positive
POSP  = 'posp' # partial positive
NEUT  = 'neut' # positive neutral
NEUTN = 'neutn' # negative neutral
NEG   = 'neg' # negative
NEGP  = 'negp' # partial negative