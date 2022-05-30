import os
import setuptools 

def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()

setuptools.setup(name='music-composition-api',
      version='0.0',
      description='Python harmony package for hand-made chord progressions maker',
      author='Carlos Hernandez Olivan',
      author_email='carloshero@unizar.es',
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          ],
      
      )
