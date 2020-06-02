from setuptools import setup

setup(name="nds",
      version="0.3.0",
      description="Non-dominated sorting algorithm.",
      author="Alexander Kryuchkov",
      author_email="KernelA@users.noreply.github.com",
      url="https://github.com/KernelA/nds-py",
      license="MIT",
      long_description="See Buzdalov M., Shalyto A. "
                       "A Provably Asymptotically Fast Version of the Generalized Jensen Algorithm for Non-dominated Sorting //"
                       " Parallel Problem Solving from Nature XIII.- 2015. - P. 528-537. - (Lecture Notes on Computer Science ; 8672).",
      packages=["nds"],
      python_requires=">=3.6",
      classifiers=[
          "Development Status :: 4 - Beta"
      ]
      )
