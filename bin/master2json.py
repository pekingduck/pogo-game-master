#!/usr/bin/env python3

# This script converts a decoded Game Master to JSON
# Usage master2json.py game_master.txt game_master.json

import os.path
import sys
import re
import pprint
import json

# Extract string, int , float or boolean from string
def extract_val(v):
  if v.startswith('"') and v.endswith('"'):
    return v[1:-1]
  elif v == 'true':
    return True
  elif v == 'false':
    return False

  try:
    i = int(v)
    return i
  except ValueError:
    try:
      f = float(v)
      return f
    except ValueError:
      return v

def debug(msg):
  pass
  #print("DEBUG:{0}".format(msg), file=sys.stderr)

block_regex = re.compile("^\s*(\w+) {$")   # e.g. item_template {
kv_regex = re.compile("^\s*(\w+): (.*)$")  # e.g. attack_scalar: 0.714

master = {} # the top level hash

# This stack keeps track of where data should be added to.
# when a block starts i.e. xxxx_yyyy {, a new hash is created and pushed
# to the stack.
# when a block ends, we pop the hash off the stack
hash_stack = [master]

with open(sys.argv[1], "r") as f:
  for line in f:
    line = line.strip()
    debug("LINE={0}".format(line))
    if len(line) == 0:
      continue
    elif line == "}":
      debug("end of block")
      hash_stack.pop()
    elif line.endswith("{"):
      debug("start of block")
      m = block_regex.search(line)
      h = {}
      k = m.group(1)
      t = hash_stack[-1]

      if k in t:
        old_v = t[k]
        if type(old_v) == list:
          # The same key exists and the value is a list
          old_v.append(h)
        else:
          # create list
          t[k] = [old_v, h]
      else:
        t[k] = h
      hash_stack.append(h)
    else:
      m = kv_regex.search(line)
      if m:
        k = m.group(1)
        v = extract_val(m.group(2))
        t = hash_stack[-1]

        if k in t:
          old_v = t[k]
          if type(old_v) == list:
            debug("add to existing list")
            old_v.append(v)
          else:
            debug("new list")
            t[k] = [old_v, v]
        else:
          debug("new pair")
          t[k] = v

assert(len(hash_stack) == 1) # master should always be there!

#basename_no_ext = os.path.splitext(os.path.basename(sys.argv[1]))[0]
#with open("{0}.json".format(basename_no_ext), "w") as f:
json.dump(master, sys.stdout)
