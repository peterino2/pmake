import subprocess
import sys
import argparse
import os
import shutil
import inspect
import importlib 
from colorama import Fore, Style, init
init(autoreset=True)

parser = argparse.ArgumentParser(
    description = ("Registers and executes jobs")
)

parser.add_argument( 
        "--verbosity",
        default="INFO",
        choices=["DEBUG", "INFO"],
        help="Logging verbosity level"
)

parser.add_argument(
    "jobs", 
    nargs="*",
    default=["__ALL_JOBS__"],
    type=str,
    help="Jobs to run, defaults to all"
)

parser.add_argument("-l", "--list-jobs", action="store_true", help="List all jobs available")

gargs = None
g_jobs = {}

def get_gjobs():
    global g_jobs
    return g_jobs

def get_gargs():
    global gargs
    return gargs

class JobInfo:
    
    def __init__(self, func, desc, deps=None, default=False, name="Unknown"):
        self.func = func
        self.docs = desc
        self.name = name
        self.deps = [*deps]
        # print("deps : ",self.deps)
        self.default = default

    def get_deplist(self, deplist=None):
        global g_jobs

        if deplist is None:
            deplist = []
            
        for dep in self.deps:
            assert dep in g_jobs, f"{dep} is listed as a dep of {self.name}, but is not a valid target"
            if dep == self.name:
                print(f"warning: {self.name} has itself listed as a dependency")
                continue
            if dep not in deplist:
                deplist.append(dep)
                deplist += g_jobs[dep].get_deplist(deplist)

        odeplist = []

        for dep in deplist:
            if dep not in odeplist:
                odeplist.append(dep)
        return odeplist

def job(*deps, desc=None, default=True):
    def wrap(f):
        global g_jobs
        g_jobs[f.__name__] = JobInfo(f, desc, deps, default, f.__name__)
        def wrapped_f(*deps):
            f(*deps)
        return wrapped_f
    return wrap

class JobManager:

    def __init__(self, jobs):
        self.jobs = jobs
        self.defaults = []

        for name, info in self.jobs.items():
            if info.default: 
                self.defaults.append(name)

        self.dispatched_jobs = []
        self.queued_jobs = []
        self.n_jobs = 0
        self.completed_jobs = []
    
    def queue_jobs(self, joblist):
        queued_jobs = joblist

        if "__ALL_JOBS__" in joblist:
            queued_jobs = self.defaults

        for jobname in queued_jobs:
            jobinfo = self.jobs[jobname]
            deplist = jobinfo.get_deplist()
            for dep in deplist:
                if dep not in queued_jobs:
                    queued_jobs.append(dep)            

        self.queued_jobs = queued_jobs
        self.queued_count = len(queued_jobs)

        print("======================================================================")
        print("Queueing the following jobs:")
        for job in self.queued_jobs:
            print(f"    {Fore.CYAN}{job}")
        print(f"  TOTAL: {Fore.YELLOW}{self.queued_count}")
        print("======================================================================")
        return queued_jobs

    def show_jobs(self):
        word = 'are'
        s = 's'
        default_jobs = []
        nondefault_jobs = []
        for name, job in self.jobs.items():
            if job.default: default_jobs.append(job)
            else: nondefault_jobs.append(job)

        if len(self.jobs) == 1:
            word = "is"
            s = ""
        
        def print_job(job):
            name = job.name
            asterix = "* "
            if not job.default:
                asterix = "  "
            else:
                asterix = "* "

            if job.docs is not None:
                print(f"   {asterix}{Fore.MAGENTA + name} - {Fore.GREEN + job.docs}")
            else:
                print(f"   {asterix}{Fore.MAGENTA + name} - {Fore.YELLOW + 'no description available'}")

        print("\n======================================================================")
        print(f"There {word} {Fore.YELLOW}{len(self.jobs)}{Style.RESET_ALL} job{s} registered: (* means part of the default)")

        for job in default_jobs:
            print_job(job)

        for job in nondefault_jobs:
            print_job(job)
        print("======================================================================")
            
    def run_job(self, name):
        job = self.jobs[name]
        
        if name not in self.completed_jobs:
            for dep in job.deps:
                if name == dep:
                    continue
                if dep not in self.completed_jobs:
                    self.run_job(dep)
            print(Fore.MAGENTA + f"=========== {Fore.GREEN}Running Job: " + Fore.CYAN + name + Fore.MAGENTA + 
                    f" [{Fore.GREEN}{len(self.completed_jobs) + 1}{Fore.MAGENTA}/{self.queued_count}] ======== ")
            try:
                job.func()
                self.completed_jobs.append(name)
            except:
                print(f"{Fore.RED}Job {name} failed")
                raise
    
    def run_jobs(self):
        for job in self.queued_jobs:
            self.run_job(job)

def get_manager():
    return JobManager(g_jobs)

def petesmakemain():
    args = parser.parse_args()

    args.list_jobs = True

    manager = JobManager(g_jobs)

    if args.list_jobs:
        manager.show_jobs()
        return

    manager.queue_jobs(args.jobs)
    manager.run_jobs()


def main_importer(root, args, filename='pmakefile'):

    apath = os.path.abspath(os.path.join(root, filename))
    if not os.path.exists(apath):
        apath = os.path.abspath(os.path.join(root, filename+'.py'))
        assert os.path.exists(apath)
    orig_dir = os.path.dirname(apath)

    loader = importlib.machinery.SourceFileLoader(
        "tmpPackage", apath
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)

    # set up pmakefile's internal globals
    mod.job = job
    mod.cli_args = args
    mod.path = os.path
    mod.pmake = sys.modules[__name__]
    mod.orig_dir = orig_dir

    # standard imports
    mod.sys = sys
    mod.sp = subprocess
    mod.subprocess = subprocess
    mod.shutil = shutil
    mod.os = os

    loader.exec_module(mod)
    return mod.pmake.get_gjobs()
    
def main():
    args = parser.parse_args()
    gjobs = main_importer(os.getcwd(), args)
    manager = JobManager(gjobs)

    if args.list_jobs:
        manager.show_jobs()
        return

    manager.queue_jobs(args.jobs)
    manager.run_jobs()
    
