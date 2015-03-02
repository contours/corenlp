package in.aesh.nlp.pipeline;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.Annotator;
import edu.stanford.nlp.util.ArraySet;
import edu.stanford.nlp.util.CoreMap;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.Properties;
import java.util.Set;
import java.util.Spliterator;
import java.util.Spliterators;
import java.util.function.BiConsumer;
import java.util.stream.Stream;

public class SpeakerAnnotator implements Annotator {

    public SpeakerAnnotator(String name, Properties props) {}

    @Override
    public void annotate(Annotation annotation) {
        if (! annotation.containsKey(CoreAnnotations.DocIDAnnotation.class)) {
            throw new RuntimeException("No document ID");
        }
        if (! annotation.containsKey(CoreAnnotations.SentencesAnnotation.class)) {
            throw new RuntimeException("No sentences");
        }
        String docID = annotation.get(CoreAnnotations.DocIDAnnotation.class);
        List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);

        try (Stream<String> speakers = Files.lines(Paths.get("data/in/" + docID + ".speakers")).map(String::trim)) {
            forEach(sentences.stream(), speakers, (sentence, speaker) -> {
                if (speaker.length() > 0) {
                    sentence.get(CoreAnnotations.TokensAnnotation.class).forEach(token -> {
                        token.set(CoreAnnotations.SpeakerAnnotation.class, speaker);
                    });
                }
            });
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Set<Requirement> requirementsSatisfied() {
        return Collections.emptySet();
    }

    @Override
    public Set<Requirement> requires() {
        return Collections.unmodifiableSet(new ArraySet<Requirement>(
                TOKENIZE_REQUIREMENT,
                CLEAN_XML_REQUIREMENT,
                SSPLIT_REQUIREMENT));
    }

    private static<A,B> void forEach(Stream<A> a, Stream<B> b, BiConsumer<A,B> consumer) {
        Objects.requireNonNull(consumer);
        Spliterator<A> aSpliterator = Objects.requireNonNull(a).spliterator();
        Spliterator<B> bSpliterator = Objects.requireNonNull(b).spliterator();
        Iterator<A> aIterator = Spliterators.iterator(aSpliterator);
        Iterator<B> bIterator = Spliterators.iterator(bSpliterator);
        while (aIterator.hasNext() && bIterator.hasNext()) {
            consumer.accept(aIterator.next(), bIterator.next());
        }
    }

}
