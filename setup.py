from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='beaverpy',
      version='0.0.1',
      description='Estimate water storage created by beaver dams',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering :: Hydrology',
          'Programming Language :: Python :: 3',
      ],
      keywords='hydrology, beaver, ecology, water storage',
      url='https://github.com/konradhafen/beaverpy',
      author='Konrad Hafen',
      author_email='khafen74@gmail.com',
      license='GPLv3',
      packages=['beaverpy'],
      install_requires=[
          'gdal',
          'numpy',
      ],
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.7',)
