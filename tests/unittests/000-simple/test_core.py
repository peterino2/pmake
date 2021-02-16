import os
import sys

orig_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join(orig_dir, '../../')))

import pogmake

args_raw = ['pog']

def test_parse_args():
    args = pogmake.parser.parse_args(args_raw)
    assert args.verbose == False

def test_pogfile_simple():
    args = pogmake.parser.parse_args(args_raw)
    args.start_dir = orig_dir 

    manager = create_manager(args)
    jobs = manager.jobs
    
    assert "job1" in jobs 
    assert "job2" in jobs
    
    
