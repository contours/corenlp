## Compile the code

```
$ ./gradlew build
```

Compiles the custom SpeakerAnnotator.

## Create an installation image

```
$ ./gradlew installApp
```

This puts all the necessary JARs in `build/install/corenlp/lib/`.

## Process files

```
$ ./pipeline.sh
```

This script will run the pipeline on all the files listed in
`filelist.txt`.  Annotated files will be written to `data/out`.

## Pipeline configuration

The following options can be configured in `config.props`:

* `threads` number of cores to use
* `filelist` list of input files
* `customAnnotatorClass.speaker` name of the class implementing the `speaker` annotator
* `annotators` comma-separated list of annotators to include in the pipeline
* `ssplit.eolonly` expect input that is already sentence-tokenized
* `outputDirectory` directory to put annotated documents in
* `replaceExtension` name output files like `[document id].xml`

## Input files

Input files must be placed in the directory `data/in/` and added to
`filelist.txt`.  Your input files must be plain text files containing
one sentence per line, wrapped in a single `doc` XML element with an
`id` attribute identifying the document.

For example:

```
<doc id="U-0012">
In response to your first direction and then you can remind me of the others.
Okay.
[ many sentences snipped ... ]
And your help.
To you.
</doc>

```

[`splitta`](https://github.com/contours/node-splitta) can be used to
sentence-tokenize input files:

```
$ cat U0080_Transcript.txt | ./bin/splitta > U-0080.txt
```

The `add-doc-ids.sh` script can handle wrapping plain text files in `doc` elements:

```
./add-doc-ids.sh data/in/*.txt
```

The command above will create an XML file alongside each TXT file.

For the SpeakerAnnotator to work, there must be an additional input
file for each document, named `[document id].speakers`. So, for
example, for document with id `U-0012` shown above, the
SpeakerAnnotator will expect to find a file
`data/in/U-0012.speakers`. This file is a plain text file with one
speaker name per line. It should have exactly the same number of lines
as there are sentences in input document.

A speakers file can be created for one of the DocSouth interviews in
the Redis database by using the `dump-speakers.py` script in the
`evaluation` project:

```
$ ./dump-speakers.py U-0012 > U-0012.speakers
```

A speakers file can be created for a sentence-tokenized SOHP
transcript by using the `print-speakers.py` script in this project:

```
$ ./print-speakers.py U-0080.txt > U-0080.speakers
```

## Output files

Output files will appear in the `data/out` directory. To see a
human-readable view of the coreference resolution:

```
./parse-output.py data/out/U-0012.xml
```
