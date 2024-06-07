"""
Prunes the pages file by removing pages which are marked as redirects but have no corresponding
redirect in the redirects file.

Output is written to stdout.
"""

from __future__ import print_function

import io
import sys
import gzip

# Validate input arguments.
if len(sys.argv) < 3:
  print('[ERROR] Not enough arguments provided!')
  print('[INFO] Usage: {0} <pages_file> <redirects_file>'.format(sys.argv[0]))
  sys.exit()

PAGES_FILE = sys.argv[1]
REDIRECTS_FILE = sys.argv[2]

if not PAGES_FILE.endswith('.gz'):
  print('[ERROR] Pages file must be gzipped.')
  sys.exit()

if not REDIRECTS_FILE.endswith('.gz'):
  print('[ERROR] Redirects file must be gzipped.')
  sys.exit()

# Create a dictionary of redirects.
REDIRECTS = {}
for line in io.BufferedReader(gzip.open(REDIRECTS_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  source_page_id = line_item[0]
  REDIRECTS[source_page_id] = True

# Loop through the pages file, ignoring pages which are marked as redirects but which do not have a
# corresponding redirect in the redirects dictionary, printing the remaining pages to stdout.
for line in io.BufferedReader(gzip.open(PAGES_FILE, 'r')):
  line_item = line.decode().rstrip('\n').split('\t')
  # if a page does not have enough items for some reason, just leave it
  if len(line_item) < 3:
    continue
  page_id = line_item[0]
  page_title = line_item[1]
  is_redirect = line_item[2]

  if is_redirect == '0' or page_id in REDIRECTS:
    print('\t'.join([page_id, page_title, is_redirect]))
