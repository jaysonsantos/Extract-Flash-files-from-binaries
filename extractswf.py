#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @todo: Make a better code translation, I did it too fast.
# @todo: Instead loading the hole file to memory, read chunks.

__author__ = 'Jayson Reis'
__version__ = '0.1'

import sys
import os
import optparse
import struct

def _e(str):
    sys.stderr.write(str)
    sys.stderr.flush()
    
options_parser = optparse.OptionParser()
options_parser.add_option("-f", "--file_path", dest="file_path")

options_parser.add_option("-d", "--destionation_dir", dest="destionation_dir")

(options, arguments_options) = options_parser.parse_args(sys.argv)

if options.file_path is None:
    _e('The file to be analysed is required.\n')
    sys.exit(1)
else:
    if os.path.exists(options.file_path):
        file_path = open(options.file_path, 'rb').read()
        file_size = len(file_path)
    else:
        _e('File does not exists: "%s"\n' % options.file_path)
    
if options.destionation_dir is None:
    destionation_dir = os.path.abspath(os.path.dirname(__file__))
    file_path_base = os.path.basename(os.path.splitext(options.file_path)[0])
    file_path_swf = os.path.join(destionation_dir, '%s-%d.swf')
else:
    destionation_dir = os.path.abspath(os.path.dirname(options.destionation_dir))
    file_path_base = os.path.basename(os.path.splitext(options.file_path)[0])
    file_path_swf = os.path.join(destionation_dir, '%s-%d.swf')
    
i = 0
extracted_files = 0
print('Wait. File analyzes can take a while.')
while i < file_size:
    try:
        tmp = struct.unpack('3s', file_path[i:i+3])[0]
    except struct.error:
        # EOF
        break
    if tmp == 'CWS' or tmp == 'FWS' :
        extracted_files += 1
        if tmp == 'CWS':
            compressed_file = True
            _e('Extracting a compressed file\n')
        else:
            compressed_file = False
        extracted_file_name = file_path_swf % (file_path_base, extracted_files)
        print 'Found a flash file.'
        file_size = struct.unpack("<I", file_path[i+4:i+8])[0]
        extracted_file = open(extracted_file_name, 'wb')
        extracted_file.write(file_path[i:i+511+file_size])
        extracted_file.close()
        print "Extracted to: %s" % extracted_file_name
        i += 511 + file_size
    else:    
        i += 1
if extracted_files > 0:
    if extracted_files == 1:
        print '%s Flash file extracted to %s.' % (extracted_files, destionation_dir)
    else:
        print '%s Flash files extracted to %s.' % (extracted_files, destionation_dir)
else:
    print 'The are not Flash files inside specified file.'
