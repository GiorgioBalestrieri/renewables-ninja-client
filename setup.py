from setuptools import setup, find_packages

setup(
    name = "renewables_ninja_client",
    version = "0.1.0",
    description = ("Client for Renewables Ninja API."),
    author = ["Giorgio Balestrieri"],
    packages = find_packages(exclude=[
        "docs", "tests", "examples", 
        "sandbox", "scripts"]),
    install_requires=[
        "pandas",
        "numpy",
        "requests",
        'typing;python_version<"3.7"'],
    )