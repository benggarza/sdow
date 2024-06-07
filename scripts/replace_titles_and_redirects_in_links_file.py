"""
Replaces page names in the links file with their corresponding IDs, eliminates links containing
non-existing pages, and replaces redirects with the pages to which they redirect.

Output is written to stdout.
"""

from __future__ import print_function

import io
import sys
import gzip

# Validate inputs
if len(sys.argv) < 4:
  print('[ERROR] Not enough arguments provided!')
  print('[INFO] Usage: {0} <pages_file> <redirects_file> <links_file>'.format(sys.argv[0]))
  sys.exit()

PAGES_FILE = sys.argv[1]
REDIRECTS_FILE = sys.argv[2]
LINKS_FILE = sys.argv[3]

if not PAGES_FILE.endswith('.gz'):
  print('[ERROR] Pages file must be gzipped.')
  sys.exit()

if not REDIRECTS_FILE.endswith('.gz'):
  print('[ERROR] Redirects file must be gzipped.')
  sys.exit()

if not LINKS_FILE.endswith('.gz'):
  print('[ERROR] Links file must be gzipped.')
  sys.exit()

print(f'Parsing page file...',file=sys.stderr)
# Create a set of all page IDs and a dictionary of page titles to their corresponding IDs.
ALL_PAGE_IDS = {}
PAGE_TITLES_TO_IDS = {}
for line in io.BufferedReader(gzip.open(PAGES_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  page_id = line_item[0]
  page_title = line_item[1]
  #print(f'{page_id}: {page_title}',file=sys.stderr)
  ALL_PAGE_IDS[page_id] = 1
  PAGE_TITLES_TO_IDS[page_title] = page_id

print(f'Parsing redirect file...',file=sys.stderr)
# Create a dictionary of page IDs to the target page ID to which they redirect.
REDIRECTS = {}
for line in io.BufferedReader(gzip.open(REDIRECTS_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  source_page_id = line_item[0]
  target_page_id = line_item[1]
  REDIRECTS[source_page_id] = target_page_id

print(f'Parsing links file...')
# Loop through each line in the links file, replacing titles with IDs, applying redirects, and
# removing nonexistent pages, writing the result to stdout.
for line in io.BufferedReader(gzip.open(LINKS_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  source_page_id = line_item[0]
  target_page_title = line_item[1]

  source_page_exists = source_page_id in ALL_PAGE_IDS

  if source_page_exists:
    source_page_id = REDIRECTS.get(source_page_id, source_page_id)

    target_page_id = PAGE_TITLES_TO_IDS.get(target_page_title)

    if target_page_id is not None and source_page_id != target_page_id:
      target_page_id = REDIRECTS.get(target_page_id, target_page_id)
      #print(f'{source_page_id} -> {target_page_id}',file=sys.stderr)
      print('\t'.join([source_page_id, target_page_id]))
  else:
    print('',file=sys.stderr)
