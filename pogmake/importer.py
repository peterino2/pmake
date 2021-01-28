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
import importlib

def find_all_subpogs(root):
    return subpogs

def inner_importer(root, cli_args, _filename=None):
    """
    Runs the importer for a target file and 
    directory, 

    :return: g_jobs, a glob of all the jbos in that file
    """

    filename = _filename
    if _filename == None:
        filename = "pogfile"


    apath = os.path.abspath(os.path.join(root, filename))
    if not os.path.exists(apath):
        tapath = os.path.abspath(os.path.join(root, filename+'.py'))
        assert os.path.exists(tapath), f" Neither {root + apath} or the .py version exists"
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
    mod.include_paths = []
    mod.exclude_paths = []

    loader.exec_module(mod)

    gjobs = mod.pogmake.get_gjobs()
    for path in mod.include_paths:
        jpath = os.path.join(root, path)

        if not os.path.exists(jpath):
            print(f"Include path in {apath} does not exist: {jpath}")
            continue
            
        if os.path.isdir(jpath):
            rjobs, modinfo = inner_importer(jpath, cli_args)
            gjobs.update(rjobs)
        else:
            rjobs, modinfo = inner_importer(os.path.dirname(jpath), cli_args, os.path.basename(jpath))
            gjobs.update(rjobs)

    return gjobs, mod

def main_importer(root, cli_args, filename='pogfile'):

    subpogs = []
    first = True
    gjobs = {}
    excluded = []
    for r, d, f in os.walk(root):
        should_skip = False
        for path in excluded:
            if r.startswith(os.path.abspath(path)+os.sep) or r == path:
                should_skip = True

        if not should_skip:
            for fname in f:
                if fname == "pogfile" or fname == "pogfile.py":
                    rjobs, modinfo = inner_importer(r, cli_args)
                    gjobs.update(rjobs)
                    for epath in modinfo.exclude_paths:
                        excluded.append(os.path.abspath(os.path.join(r, epath)))

    return gjobs

def print_hidden_debug():
    pass

def main():
    args = parser.parse_args()
    args.start_file = os.path.abspath(args.start_file)

    tpath = "pogfile"
    dirpath = args.start_file

    if not os.path.isdir(dirpath):
        dirpath = os.path.dirname(args.start_file)
        tpath = os.path.basename(tpath)
    
    gjobs = main_importer(dirpath, args, tpath)
    manager = JobManager(gjobs)

    if args.print_hidden_debug:
        print_debug()

    if args.list_jobs:
        manager.show_jobs()
        return

    manager.queue_jobs(args.jobs)
    manager.run_jobs()
