#!/usr/bin/env python3

# See: https://eg.readthedocs.io/en/latest/datahub.html
def hub_entry(url, name, type="bigwig", color="black"):
    return ({"type": type,
             "name": name,
             "url": url,
             "options": {"color": color}})

aws_base = "https://{0}.s3.{1}.amazonaws.com/{2}"

import os
import sys
import json
import random
import shutil
import string
import pprint
import argparse

pp = pprint.PrettyPrinter(compact=True)

parser = argparse.ArgumentParser()
parser.version = '1.0'
parser.add_argument('-f', '--files', action='store', nargs='+', type=str, required=True)
parser.add_argument('-b', '--bucket', action='store', type=str, required=True)
parser.add_argument('-r', '--region', action='store', type=str, required=True)
parser.add_argument('-n', '--names', action='store', nargs='+', type=str)
parser.add_argument('-o', '--outdir', action='store', type=str, default="")
args = parser.parse_args()

def get_file_name(file_path):
    return(os.path.basename(file_path))

def get_file_pre(file_name):
    return(os.path.splitext(file_name)[0])

def del_file_ext(file_name):
    return(os.path.splitext(file_name)[1])

def random_key(length=64):
    choices = string.ascii_letters+string.digits
    return ''.join(random.choice(choices) for i in range(length))

if __name__ == "__main__": 

    # Arguments
    files = vars(args)['files']
    bucket = vars(args)['bucket']
    region = vars(args)['region']
    names = vars(args)['names']
    outdir = vars(args)['outdir']

    # Check names
    if names is not None:
        if len(names) != len(files):
            raise ValueError("The number of names must equal the number of files.")
    else:
        names = [get_file_pre(get_file_name(i)) for i in files]

    # Check if out directory exists
    if outdir != "" and os.path.isdir(outdir) is False:
        raise ValueError("Output directory does not exist.")

    datahub = []
    for n,f in zip(names, files):
        
        # Generate random key file
        key = random_key(64)
        pre = get_file_pre(get_file_name(f))
        ext = del_file_ext(f)
        file_key = "{0}-{1}{2}".format(pre, key, ext)

        # Format into hosted path
        file_aws = aws_base.format(bucket, region, file_key)

        # Copy file with key name
        shutil.copyfile(f, os.path.join(outdir, file_key))

        entry = hub_entry(file_aws, n, type="bigwig", color="black")
        datahub.append(entry)

    # Show config
    pp.pprint(datahub)

    # Save config
    with open(os.path.join(outdir, "datahub.json"), 'w') as outfile:
        json.dump(datahub, outfile, indent=4)
