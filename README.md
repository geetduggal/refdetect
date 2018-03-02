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

## Examples

From command line within module directory:

```
refdetect <bam file on platform>
```

In a python script:

```python
import refdetect

ref_file_id = refdetect.get_reference_id("<bam file on platform>")
```

If a reference is not found a Python exception will be thrown.

## Adding a new reference to the module

```
$ refdetect <BAM file on platform> --refname=b37 --refid=file-XXX
```

In a python script:

```python
import refdetect

ref_file_id = refdetect.write_ref_metadata("<bam file on platform>", "b37", "file-XXX")
```

## Contributors

* Alpha Diallo
* Geet Duggal
* Marcus Kinsella
* Maria Simbirsky
