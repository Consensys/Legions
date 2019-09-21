from setuptools import setup

setup(name='legion',
      version='0.3',
      description='Ethereum/EVM Node Security Toolkit',
      url='https://github.com/shayanb/Legion',
      author='Shayan Eskandari - ConsenSys Diligence',
      author_email='shayan.eskandari@consensys.net',
      license='MIT',
      packages=['legion'],
      package_data={
          'legion': ['commands/**'],
      },
      install_requires=[
          'python-nubia',
          'jellyfish',
          'prettytable',
          'prompt-toolkit',
          'Pygments',
          'pyparsing',
          'termcolor',
          'wcwidth',
          'web3>=5.1.0'
          #'requests',
      ],      
      entry_points='''
          [console_scripts]
          legion=legion.main:main
      ''',
      zip_safe=False)