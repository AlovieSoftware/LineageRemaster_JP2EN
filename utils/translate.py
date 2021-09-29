# -*- coding: utf-8 -*-
"""
The utility translates the text file line by line using the Google Translate service.
param 1 - source file
param 2 - destination file
param 3 - number of lines to send to the translate service (optional, default = 100)
"""
import sys
from googletrans import Translator

src_lang = 'ja'
dest_lang = 'en'
decoding = 'Shift-JIS'
encoding = 'UTF-8'
group = 100
max_translate_length = 4500 # + length of current line 

if len(sys.argv) < 3:
    print('Please, set 2 arguments: src file and dest file')
    sys.exit(1)
elif len(sys.argv) > 3:
    group = int(sys.argv[3])

with open(sys.argv[1], 'r', encoding = decoding) as f:
    translator = Translator()
    i = 0
    lines = ''
    start_group = 1
    while True:
        i += 1
        line = f.readline()
        print("{}: {}".format(i, line))
        lines += line
        if not line or i%group == 0 or len(lines) > max_translate_length:
            if lines:
                print('[Src: {0}]\n{1}[Src: {0}]'.format(start_group, lines))
                translation = translator.translate(lines, src = src_lang, dest = dest_lang)
                print('[Dest: {0}]\n{1}\n[Dest: {0}]\n'.format(start_group, translation.text))
                with open(sys.argv[2], 'a', encoding = encoding) as fw:
                    fw.write(translation.text + '\n')
                lines = ''
            start_group = i
            if not line:
                break
