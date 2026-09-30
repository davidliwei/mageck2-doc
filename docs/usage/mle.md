# mle

Estimate gene essentiality (beta scores) by maximum likelihood under a
user-supplied experimental design matrix. This is the route for designs that a
single treatment-versus-control comparison cannot express: time series, several
conditions at once, or drug treatments.

Outputs `[prefix].gene_summary.txt` (beta scores) and
`[prefix].sgrna_summary.txt`; see [file formats](../FILE_FORMATS.md#mle-outputs).

Beta scores are on the natural-log scale, and the **first row of the design
matrix is the baseline sample** — see the
[design matrix format](../FILE_FORMATS.md#design-matrix) for the rules, which the
module enforces.

```{eval-rst}
.. argparse::
   :module: mageck2.argsParser
   :func: build_parser
   :prog: mageck2
   :path: mle
```

## See also

- [Tutorial 4 — multi-condition analysis with MAGeCK MLE](../TUTORIAL.md#4-multi-condition-analysis-with-mageck-mle)
- [Tutorial 9 — complex experimental designs](../TUTORIAL.md#9-complex-experimental-designs)
- [Tutorial 11 — incorporating sgRNA efficiency](../TUTORIAL.md#11-incorporating-sgrna-efficiency)
- [Design matrix file format](../FILE_FORMATS.md#design-matrix)
