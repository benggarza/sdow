"""
Combines the incoming and outgoing links (as well as their counts) for each page.

Output is written to stdout.
"""

from __future__ import print_function

import io
import sys
import gzip
from collections import defaultdict

# Validate input arguments.
if len(sys.argv) < 2:
  print('[ERROR] Not enough arguments provided!')
  print('[INFO] Usage: {0} <outgoing_links_file> <incoming_links_file>'.format(sys.argv[0]))
  sys.exit()

OUTGOING_LINKS_FILE = sys.argv[1]
INCOMING_LINKS_FILE = sys.argv[2]

if not OUTGOING_LINKS_FILE.endswith('.gz'):
  print('[ERROR] Outgoing links file must be gzipped.')
  sys.exit()

if not INCOMING_LINKS_FILE.endswith('.gz'):
  print('[ERROR] Incoming links file must be gzipped.')
  sys.exit()

# Create a dictionary of page IDs to their incoming and outgoing links.
LINKS = defaultdict(lambda: defaultdict(str))
for line in io.BufferedReader(gzip.open(OUTGOING_LINKS_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  source_page_id = line_item[0]
  target_page_ids = line_item[1]
  LINKS[source_page_id]['outgoing'] = target_page_ids

for line in io.BufferedReader(gzip.open(INCOMING_LINKS_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  if len(line_item) < 2:
    print(f'something wrong with this line item: {line_item}',file=sys.stderr)
    continue
  target_page_id = line_item[0]
  source_page_ids = line_item[1]
  LINKS[target_page_id]['incoming'] = source_page_ids

# For each page in the links dictionary, print out its incoming and outgoing links as well as their
# counts.
for page_id, links in iter(LINKS.items()):
  outgoing_links = links.get('outgoing', '')
  outgoing_links_count = 0 if outgoing_links == '' else len(
      outgoing_links.split('|'))

  incoming_links = links.get('incoming', '')
  incoming_links_count = 0 if incoming_links == '' else len(
      incoming_links.split('|'))

  columns = [page_id, str(outgoing_links_count), str(
      incoming_links_count), outgoing_links, incoming_links]

  print('\t'.join(columns))
