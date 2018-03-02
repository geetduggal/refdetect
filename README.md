# refdetect module

Given an input bam file path or file ID, this module allows a DNAnexus user to obtain the reference file ID on the platform.

## Currently supported genomes

This list is intended to expand, but for our MVP of the compression utility, we will focus on these human genomes:

* GRCh37 (b37)
* GRCh37 (hs37d5)
* hg18
* hg19 (UCSC)
* GRCh38

Please see https://wiki.dnanexus.com/Scientific-Notes/human-genome for more information on the distinctions between the GRCh37s.

## Installation

```
python setup.py install
```

## Using refdetect in a Python DNAnexus applet

You can simply include this source code, but as an alternative, you can also include this asset and you should be able to `import refdetect` immediately:

```
record-F2BQ6yQ0BF9zPJ7P7P0g4Bxg
```

## Examples

From command line within module directory:

```
refdetect bams-compressable/b37/SRR100022_chrom21_mapped_to_b37.bam
```

In a python script:

```python
import refdetect

ref_file_id = refdetect.get_reference_id("bams-compressable/b37/SRR100022_chrom21_mapped_to_b37.bam")
```

If a reference is not found a Python exception will be thrown.

## Adding a new reference to the module

```
$ refdetect bams-compressable/b37/SRR100022_chrom21_mapped_to_b37.bam --refname=b37 --refid=file-XXX
```

In a python script:

```python
import refdetect

ref_file_id = refdetect.write_ref_metadata("bams-compressable/b37/SRR100022_chrom21_mapped_to_b37.bam", "b37", "file-XXX")
```

## Contributors

* Alpha Diallo
* Geet Duggal
* Marcus Kinsella
* Maria Simbirsky
