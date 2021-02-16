exclude_paths = ["tests"]  # do not look for pogfiles in this directory
include_paths = ['pogmake/sample_pogfile.py']

path = os.path

docs_spec_folder = path.abspath(path.join("docs_src/_spec"))
usage_print_file = path.join(docs_spec_folder, "usage_print.txt")

# usage_print_example
@job(desc="Prints the 'usage' to the temporary directory under ", default=False)
def usage_print():
    os.makedirs("docs_src/_spec", exist_ok=True)
    output = subprocess.check_output([sys.executable, "pog", "--help"], cwd=orig_dir)
    with open(usage_print_file, "w") as f:
        f.write(output.decode())


@job("usage_print", desc="Builds the documentation for pogmake")
def docs():
    os.makedirs("build-html", exist_ok=True)
    subprocess.run(["sphinx-build", "docs_src", "build-html"], check=True, cwd=orig_dir)
    # /usage_print_example


@job(desc="Runs the tests for pogmake")
def tests():
    subprocess.run(
        ["python", "../pog", "--list"], check=True, cwd=os.path.join(orig_dir, "tests")
    )


@job(desc="installs the dependencies for building the docs", default=False)
def docs_deps():
    subprocess.run(
        ["python", "-m", "pip", "install", "-r", "requirements.txt"],
        check=True,
        cwd=os.path.join(orig_dir, "docs_src"),
    )


@job(desc="uploads to pypi", default=False)
def upload_to_pypi():
    cwd = os.getcwd()
    os.chdir(orig_dir)
    os.system("python setup.py sdist")
    os.system("twine upload dist/*")
    os.chdir(cwd)
