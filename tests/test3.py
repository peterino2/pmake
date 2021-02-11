@job("job1", desc="Job 2 depends on job 1")
def job2():
    print("job2")


@job(desc="job1's generator function")
def job1_gen():
    print("job1_gen")


@job("job1_gen", desc="job1's main build")
def job1():
    print("job1")
