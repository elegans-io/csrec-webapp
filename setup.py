
from setuptools import setup

setup(
    # Application name:
    name="csrec-webapp",

    # Version number (initial):
    version="0.1.0",

    # description
    description="Webapp for the cold start recommender",

    # long_description
    long_description="Web application which provide an API for the cold start recommender",

    # Application author details:
    author="elegans.io Ltd",
    author_email="info@elegans.io",

    # Choose your license
    license='LICENSE.txt',

    # Include additional files into the package
    include_package_data=False,

    scripts=['csrec_webapp.py'],

	url='https://github.com/elegans-io/csrec-webapp',

    # Dependent packages (distributions)
    install_requires=["cold-start-recommender>=0.4.0",
                      "tornado>=4.2.1",
                      "locustio>=0.7.3"]
)
