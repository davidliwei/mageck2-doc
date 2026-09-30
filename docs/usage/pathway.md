# pathway

Given a gene ranking from the [`test`](test.md) command, test whether gene sets
or pathways (in GMT format) are enriched. Enrichment is evaluated in both the
negative- and positive-selection directions unless `--single-ranking` is given.

```{eval-rst}
.. argparse::
   :module: mageck2.argsParser
   :func: build_parser
   :prog: mageck2
   :path: pathway
```

## See also

- [Tutorial 3 — end-to-end analysis of a public dataset](../TUTORIAL.md#3-end-to-end-analyzing-a-public-screening-dataset)
- [GMT pathway file format](../FILE_FORMATS.md)
