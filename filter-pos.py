#! /usr/bin/env python3

import sys
from xml.etree.ElementTree import iterparse

# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# https://pinboard.in/cached/ebae1c3686a2/
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

def filter_tokens(filename, filter):
    if not filename.endswith('.xml'):
        raise Exception('%s does not end with .xml' % filename)
    with open(filename[:-3] + filter.name + '.txt', 'w') as outfile:
        space = False
        for _, elem in iterparse(filename):
            if elem.tag == 'token':
                if filter.accepts(elem):
                    if space: print(' ', end='', file=outfile)
                    print(elem.find('word').text, end='', file=outfile)
                    space = True
            if elem.tag == 'sentence':
                print(file=outfile)
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

class Filter:
    def __init__(self, tags):
        self.tags = tags
        self.name = '-'.join(tags)
    def accepts(self, token):
        pos = token.find('POS').text
        for t in self.tags:
            if t.endswith('*') and pos.startswith(t[:-1]):
                return True
            if t == pos:
                return True
            return False

if __name__ == '__main__':
    tags = (parse_input(input('POS tags to accept [NN*,VB*,JJ*]: '))
            or ['NN*','VB*','JJ*'])
    filter = Filter(tags)
    for filename in sys.argv[1:]:
        filter_tokens(filename, filter)
