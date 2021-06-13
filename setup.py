from setuptools import setup

with open("version.txt", encoding="utf-8") as file:
    version = file.readlines()[0].strip()

if not version:
    raise ValueError("Found empty version")

setup(name="nds",
      version=version,
      license="MIT",
      packages=["nds"],
      keywords=["nds", "multiobjective-optimization", "non-dominated-sorting"],
      python_requires=">=3.6"
      )
