import pmake
from pmake import job


@job()
def myjob1():
    print("Hfhehfawe")

pmake.pmakemain()
