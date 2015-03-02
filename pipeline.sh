#! /bin/sh

java -cp "build/install/corenlp/lib/*" \
     -Xmx8g \
     edu.stanford.nlp.pipeline.StanfordCoreNLP \
     -props "config.props"
