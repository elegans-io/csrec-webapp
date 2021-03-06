from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path
import csrec_webapp
here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
long_description = open('README.md').read()


def setup_package():

    build_requires = ['csrec>=0.4.1', 'tornado>=4.5.2', 'locustio>=0.7.3']

    metadata = dict(
        name='csrec-webapp',

        # Versions should comply with PEP440.  For a discussion on single-sourcing
        # the version across setup.py and the project code, see
        # https://packaging.python.org/en/latest/single_source_version.html
        version=csrec_webapp.__version__,
        description="Webapp for the cold start recommender",
        long_description=long_description,

        # The project's main homepage.
        url='https://github.com/elegans-io/csrec-webapp',

        # Author details
        author='elegans.io Ltd',
        author_email='info@elegans.io',

        # Choose your license
        license='GPL v2',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Information Technology',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2.7',
        ],

        # What does your project relate to?
        keywords='recommendations, recommender,recommendation engine',

        # You can just specify the packages manually here if your project is
        # simple. Or you can use find_packages().
        #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
        packages=["csrec_webapp"],

        # List run-time dependencies here.  These will be installed by pip when your
        # project is installed. For an analysis of "install_requires" vs pip's
        # requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        # See also https://github.com/scipy/scipy/blob/master/setup.py (malemi)
        setup_requires=build_requires,
        install_requires=build_requires,

        # List additional groups of dependencies here (e.g. development dependencies).
        # You can install these using the following syntax, for example:
        # $ pip install -e .[dev,test]
        # extras_require={
        #     'dev': ['check-manifest'],
        #     'test': ['coverage'],
        # },

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then these
        # have to be included in MANIFEST.in as well.
        package_data={
            'csrec_webapp': ['*.cl', '*.py']
        },

        include_package_data=True,

        scripts=['bin/csrec_webapp.py'],


        # To provide executable scripts, use entry points in preference to the
        # "scripts" keyword. Entry points provide cross-platform support and allow
        # pip to create the appropriate form of executable for the target platform.
        # entry_points={
        #     'console_scripts': [
        #         'sample=sample:main',
        #     ],
        # },
    )

    setup(**metadata)

if __name__ == '__main__':
    setup_package()
