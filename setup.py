from setuptools import setup, find_packages

setup(
      name = "log4py",
      version = "alpha-1.0",
      author = "Jason Gao",
      author_email = "gaojian01735@pwrd.com",
      description = "This is a moudle of log server.",
      license = "MIT",
      keywords = "log4py",
      url = "https://10.14.0.102/gaojian01735/log4py",
      package_dir = {'log4py':'lib/log4py'},
      packages = find_packages(where = 'lib', exclude = ['*.tmp', 'tmp*', '*tmp*', '.git']),
      zip_safe = True,
     )
