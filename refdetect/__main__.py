import glob
import json
import os
import subprocess
import sys
import argparse


KNOWN_REFERENCES_DIR = os.path.dirname(os.path.abspath(__file__))


class KnownRef():

    def __init__(self):
        self.list_all = []
        self.import_all_refs()

    def import_all_refs(self):
        ref_files = glob.glob(os.path.join(KNOWN_REFERENCES_DIR, '*.json'))

        for json_file in ref_files:
            ref = self.import_ref(json_file)
            self.list_all.append(ref)

    def import_ref(self, json_file):
        ref = Ref()
        ref.filename = json_file

        json_load = json.load(open(json_file, "r"))
        ref.name = json_load['name']
        ref.file_id = json_load['file-id']
        ref.dict = json_load['chromosomes']

        return ref


class Ref():

    def __init__(self):
        self.filename = ''
        self.name = ''
        self.file_id = ''
        self.dict = {}


def _run_cmd(cmd, returnOutput=False):
    if returnOutput:
        output = subprocess.check_output(
            cmd, shell=True, executable='/bin/bash').strip()
        print output
        return output
    else:
        subprocess.check_call(cmd, shell=True, executable='/bin/bash')


def _inspect_header(bam_fname_or_id):
    cmd = 'dx cat {0} | samtools view -H - > header.txt'.format(bam_fname_or_id)
    _run_cmd(cmd)

    header_dict = {}
    with open('header.txt', "r") as f:
        for line in f.readlines():
            if '@SQ' not in line:
                continue

	    #Striping done 2 in passes, rather than one, which was removing more than expected
            #chr_name = line.split()[1].lstrip('SN:')
            #chr_length = line.split()[2].lstrip('LN:')
	    chr_name = line.split()[1].lstrip('SN')
            chr_name = chr_name.lstrip(':')
            chr_length = line.split()[2].lstrip('LN:')
            chr_length = chr_length.lstrip(':')
            header_dict.update({chr_name: chr_length})

    _run_cmd('rm header.txt')

    return header_dict


def _identify_reference(input_dict, known_refs):
    for ref in known_refs.list_all:
        if set(ref.dict.items()) == set(input_dict.items()):
            return ref.file_id

    raise Exception("No reference file on the DNAnexus platform could be found for this BAM file")

def get_reference_id(bam_fname_or_id):
    known_refs = KnownRef()
    header_dict = _inspect_header(bam_fname_or_id)
    return _identify_reference(header_dict, known_refs)

def write_ref_metadata(bam_fname_or_id, refname, refid):
    header_dict = _inspect_header(bam_fname_or_id)
    ref_metadata = {"name": refname, "file-id": refid, "chromosomes": header_dict}
    with open("{}/{}.json".format(KNOWN_REFERENCES_DIR, refname), "w") as f:
        f.write(json.dumps(ref_metadata))

def main(args=None):
    parser = argparse.ArgumentParser(description='BAM reference detection utility for the DNAnexus platform')
    parser.add_argument('bam_fname_or_id', help='BAM file name or ID on the DNAnexus platform')
    parser.add_argument('--refname',  help='Reference name for adding a new reference')
    parser.add_argument('--refid',  help='Reference File ID on the DNAnexus platform for adding a new reference')
    args = parser.parse_args()

    if args.refname and args.refid:
        write_ref_metadata(args.bam_fname_or_id, args.refname, args.refid)
    else:
        print get_reference_id(args.bam_fname_or_id)


if __name__ == "__main__":
    main()
