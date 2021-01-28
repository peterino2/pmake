# pogfile shared imports
import subprocess
import sys
import argparse
import os
import shutil
# /pogfile shared imports

from varname import nameof

from pogmake import *
import pogmake


def main_importer(root, cli_args, filename='pogfile'):
    print(root)
    print(filename)

    apath = os.path.abspath(os.path.join(root, filename))
    print(apath)
    if not os.path.exists(apath):
        print(apath)
        tapath = os.path.abspath(os.path.join(root, filename+'.py'))
        assert os.path.exists(apath), f" Neither {root + apath} or the .py version exists"
        apath = tapath

    orig_dir = os.path.dirname(apath)

    loader = importlib.machinery.SourceFileLoader(
        "tmpPackage", apath
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)

    # pogfile extra symbols
    mod.job = job           # job decorator
    mod.cli_args = cli_args # parsed command line arguments
    mod.pogmake = pogmake   # reference to pogmake library
    mod.orig_dir = orig_dir # absolute path to origin of this pogfile
    # /pogfile extra symbols

    # standard imports
    mod.sys = sys
    mod.subprocess = subprocess
    mod.shutil = shutil
    mod.os = os

    loader.exec_module(mod)

    gjobs = mod.pogmake.get_gjobs()

    if hasattr(mod, "subfiles"):
        for fname in mod.subfiles:
            if os.path.isdir(fname):
                gjobs.update( main_importer(fname, cli_args))
            else: 
                gjobs.update(main_importer(os.path.dirname(fname), cli_args, filename=os.path.basename(fname)))

    return gjobs

def print_hidden_debug():
    pass

def main():
    args = parser.parse_args()
    gjobs = main_importer(os.getcwd(), args)
    manager = JobManager(gjobs)

    if args.print_hidden_debug:
        print_debug()

    if args.list_jobs:
        manager.show_jobs()
        return

    manager.queue_jobs(args.jobs)
    manager.run_jobs()
