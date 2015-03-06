#! /usr/bin/env python

import sys
from xml.etree.ElementTree import iterparse

class Parser():
    def __init__(self, filename):
        sentences = []
        nes = {}
        corefs = []
        context = iterparse(filename, events=('start', 'end'))
        event, root = context.next()
        sentence = -1
        token = -1
        prev_ne_type = None
        ne_tokens = []

        def maybe_add_ne(sentence, tokens, type):
            if len(tokens) > 0:
                entities = nes.get(sentence, [])
                entities.append({
                    'start': tokens[0][0],
                    'end': tokens[-1][0] + 1,
                    'ne': ' '.join(t[1] for t in tokens),
                    'type': type })
                nes[sentence] = entities
                tokens[:] = [] # clear

        for event, elem in context:

            if event == 'start':

                if elem.tag == 'sentence':
                    if 'id' in elem.attrib:
                        sentence = int(elem.get('id'))

                if elem.tag == 'token':
                    token = int(elem.get('id'))

            if event == 'end':

                if elem.tag == 'sentence':
                    if 'id' in elem.attrib:
                        sentences.append(' '.join(
                            [ o.text for o in 
                              elem.findall('./tokens/token/word') ]))
                        maybe_add_ne(sentence, ne_tokens, prev_ne_type)

                if elem.tag == 'token':
                    ne_type = elem.find('NER').text
                    if ne_type != prev_ne_type:
                        maybe_add_ne(sentence, ne_tokens, prev_ne_type)
                    if ne_type in ('PERSON', 'LOCATION', 'ORGANIZATION'):
                        ne_tokens.append (
                            (token, elem.find('word').text))
                    prev_ne_type = ne_type

                if elem.tag == 'sentences':
                    maybe_add_ne(sentence, ne_tokens, prev_ne_type)

                if elem.tag == 'coreference' and elem[0].tag == 'mention':
                    assert elem[0].get('representative') == 'true'
                    corefs.append({
                        'representative': {
                            'text': elem[0].find('text').text,
                            'location': (int(elem[0].find('sentence').text),
                                         int(elem[0].find('start').text),
                                         int(elem[0].find('end').text)) },
                        'mentions': frozenset(
                            [ (int(m.find('sentence').text),
                               m.find('text').text) for m in
                              elem.findall('./mention') ])
                    })

            root.clear()
           
        self.sentences = sentences
        self.nes = nes
        self.corefs = corefs

    def named_entities(self, sentence, start, end):
        return tuple([ ne for ne in self.nes.get(sentence, []) 
                       if ne['start'] >= start and ne['end'] <= end ])

    def coreferences(self):
        for c in self.corefs:
            #if len(c['mentions']) < 2: continue
            nes = self.named_entities(*c['representative']['location'])
            if len(nes) == 0: continue
            yield (c['representative']['text'], nes, 
                   [ (i, text, self.sentences[i-1]) 
                     for i, text in sorted(c['mentions']) ])

if __name__ == '__main__':
    p = Parser(sys.argv[1])
    for representative, entities, mentions in p.coreferences():
        print
        print '"%s"' % representative
        print ', '.join([ '%s [%s]' % (o['ne'], o['type']) for o in entities ])
        for i, text, sentence in mentions:
            print '%s: [%s] %s' % (str(i).rjust(3), text, sentence)
