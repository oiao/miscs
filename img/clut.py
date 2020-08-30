#!/usr/bin/env python

descr ="""
Use ImageMagick to apply a batch of HaldCLUT matrices to a target file.

Usage
-----
./clut TARGET_IMG.jpg


Optional arguments
------------------
-o, --outdir: PATH
    Specify the output directory for the converted images.
    By default, the TARGET_IMG base name is used.
-r --resize: STR
    Resize argument to be passed to imagemagick.
    Recommended if applying a large number of
    cluts to the target file.
-d, --depth: INT
    The color depth of the output images. 8bit by default.
-w, --workers: INT
    Speed up the conversion by converting `workers` images at once.
    Defaults to the number of physical cores
--cluts: PATH
    This path and it's sub-directories
    will be used to look for suitable CLUT image files
    (.png format).
    A path to a single clut file can also be provided.
    Defaults to the `CLUTPATH` in this script.
"""

CLUTPATH = 'YOUR_PATH_HERE'

import os
from os.path import join as opj
from subprocess import Popen
from argparse import ArgumentParser, RawTextHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from time import time


parser = ArgumentParser(description=descr, formatter_class=RawTextHelpFormatter)
parser.add_argument('targetfile')
parser.add_argument('-o', '--outdir')
parser.add_argument('-r', '--resize')
parser.add_argument('-d', '--depth',   default='8')
parser.add_argument('-w', '--workers', default=os.cpu_count()//2)
parser.add_argument('--cluts',         default=CLUTPATH)
args = parser.parse_args()
t0 = time()

# Check the clut path
if os.path.isdir(args.cluts):
    # List all possible clut images in `args.cluts` and all subdirs
    cluts = [[opj(dir,file) for file in files if file.endswith('.png')] for dir,_,files in os.walk(args.cluts)]
    cluts = [j for i in cluts for j in i] # Flatten
elif os.path.isfile(args.cluts):
    # Single clut file
    cluts = [args.cluts]
else:
    print(f"The CLUT path '{args.cluts}' does not seem to exist. Check your inputs and adjust with the '--cluts' argument")
    exit(1)


# If no outdir provided, use the target files' base name as default
if not args.outdir:
    args.outdir = os.path.basename(os.path.splitext(args.targetfile)[0])

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
elif os.path.isfile(args.outdir):
    print(f"Out dir {args.outdir} exists!")
    exit(1)


def convert(clut):
    cmd = ['convert', args.targetfile, '-depth', args.depth, clut, '-hald-clut', opj(args.outdir, os.path.basename(clut))]
    if args.resize:
        cmd.insert(2, f"-resize")
        cmd.insert(3, args.resize)
    p = Popen(cmd)
    p.communicate()

with ThreadPoolExecutor(max_workers=args.workers) as e:
    e.map(convert, cluts)

t = time()-t0
print(f"Saved {len(cluts)} modifications of {args.targetfile} to {args.outdir} in {t/60 if t>60 else t:.1f} {'seconds' if t <= 60 else 'minutes'}")





# Helper
def remove_spaces(dir, filetypes=['.png'], replacer='_'):
    """
    Remove spaces from all file names with a file ending
    in `filetypes` and replace them with `replacer` in the
    `dir` directory and recursive sub-dirs.
    """
    for basedir,dirs,files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1] in filetypes:
                name = replacer.join(file.split())
                os.rename(opj(basedir, file), opj(basedir,name))
