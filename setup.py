# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='PDFutils',
    version='1.0.4',
    description='Django PDF utils',
    author='Maxime Haineault',
    author_email='max@motion-m.ca',
    url='https://github.com/h3/django-pdfutils',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
#   package_data={'seoutils': [
#       'templates/*',
#       ]},
    install_requires = [
        'django>=1.4',
        'decorator==3.4.0,<=3.9.9',
        'reportlab==2.5',
        'html5lib==0.90',
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
