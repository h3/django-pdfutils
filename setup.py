# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='PDFutils',
    version='1.1.3',
    description='Django PDFutils',
    long_description=(read('README.rst')),
    author='Maxime Haineault',
    author_email='haineault@gmail.com',
    license='BSD',
    url='https://github.com/h3/django-pdfutils',
    packages=find_packages(),
    include_package_data=True,
    package_data={'pdfutils': [
        'README.rst',
        'changelog',
        ]},
    install_requires = [
        'django>=1.4',
        'decorator==3.4.0,<=4.0.2',
        'reportlab==2.5',
        'html5lib==0.999999999',
        'httplib2==0.9',
        'pyPdf==1.13',
        'xhtml2pdf==0.0.4',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
