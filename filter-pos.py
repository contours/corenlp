#! /usr/bin/env python3

import sys
from xml.etree.ElementTree import iterparse

POS_TAGS = ['CC',
            'CD',
            'DT',
            'EX',
            'FW',
            'IN',
            'JJ','JJR','JJS',
            'LS',
            'MD',
            'NN','NNS','NNP','NNPS',
            'PDT',
            'POS',
            'PRP','PRP$',
            'RB','RBR','RBS',
            'RP',
            'SYM',
            'TO',
            'UH',
            'VB','VBD','VBG','VBN','VBP','VBZ',
            'WDT',
            'WP','WP$',
            'WRB']

def filter(filename, acceptToken):
    space = False
    for _, elem in iterparse(filename):
        if elem.tag == 'token':
            if acceptToken(elem):
                if space: print(' ', end='')
                print(elem.find('word').text, end='')
                space = True
        if elem.tag == 'sentence':
            print()
            space = False
        if elem.tag == 'sentences':
            break

def parse_input(s):
    s = s.strip()
    if not s: return []
    tags = [ t.strip() for t in s.split(',') ]
    for t in tags:
        if t.strip(['*']) not in POS_TAGS:
            raise Exception('Unknown tag: %s' % t)
    return tags
            
if __name__ == '__main__':
    tags = (parse_input(input('POS tags to accept [NN*,VB*,JJ*]: '))
            or ['NN*','VB*','JJ*'])

    def acceptToken(token):
        pos = token.find('POS').text
        for t in tags:
            if t.endswith('*') and pos.startswith(t[:-1]):
                return True
            if t == pos:
                return True
            return False

    filter(sys.argv[1], acceptToken)
