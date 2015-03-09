#! /usr/bin/env python3

import sys
import re
from xml.etree.ElementTree import iterparse

def represent(text):
    return text.upper()

def parse_corefs(filename):
    if not filename.endswith('.xml'):
        raise Exception('%s does not end with .xml' % filename)
    corefs = {}
    representative = None
    for _, elem in iterparse(filename):
        if elem.tag == 'mention':
            if elem.get('representative') == 'true':
                representative = represent(elem.find('text').text)
            sentence, start, end = (int(elem.find(tag).text)
                                    for tag in ['sentence','start','end'])
            if (sentence, start) in corefs:
                current = corefs[(sentence, start)]
                if len(representative) >= len(current[0]):
                    continue # keep shortest representative
            corefs[(sentence, start)] = (representative, end)
    return corefs

def resolve_corefs(filename, corefs):
    if not filename.endswith('.xml'):
        raise Exception('%s does not end with .xml' % filename)
    with open(filename[:-3] + 'corefs-resolved.txt', 'w') as outfile:
        space = False
        sentence = 1
        skip_until = 0
        for _, elem in iterparse(filename):
            if elem.tag == 'token':
                token = int(elem.get('id'))
                if token < skip_until:
                    continue
                if space: print(' ', end='', file=outfile)
                if (sentence,token) in corefs:
                    representative, skip_until = corefs[(sentence,token)]
                    print(representative, end='', file=outfile)
                else:
                    print(elem.find('word').text, end='', file=outfile)
                space = True
            if elem.tag == 'sentence':
                print(file=outfile)
                space = False
                sentence += 1
                skip_until = 0
            if elem.tag == 'sentences':
                break
        

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        corefs = parse_corefs(filename)
        resolve_corefs(filename, corefs)
