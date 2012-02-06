from setuptools import setup, find_packages
import os

CLASSIFIERS = []

setup(
    author="Jacob Rief",
    author_email="jacob.rief@gmail.com",
    name='django-shop-wishlists',
    version='0.0.1',
    description='Provide wishlists to Django SHOP, so that customers can remember items together with their variation',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='http://www.django-shop.org/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.2',
        'django-shop>=0.0.9',
    ],
    packages=find_packages(exclude=["example", "example.*"]),
    zip_safe = False
)

