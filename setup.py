from setuptools import setup

setup(name='refdetect',
      version='0.1.0',
      packages=['refdetect'],
      entry_points={
          'console_scripts': [
              'refdetect = refdetect.__main__:main'
          ]
      },
     )
