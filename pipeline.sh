#! /bin/sh

ANNS="tokenize,cleanxml,ssplit,speaker,pos,lemma,ner,parse,dcoref"

java -cp "build/install/corenlp/lib/*" \
     -Xmx8g \
     edu.stanford.nlp.pipeline.StanfordCoreNLP \
     -props "config.props" \
     -annotators $ANNS \
     -filelist "filelist.txt" \
     -outputDirectory "data/out" \
     -replaceExtension

