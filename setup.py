from setuptools import setup, find_packages
import os

setup(
    name="mini_flask_serializer",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=1.0",
        "Flask-SQLAlchemy>=2.0",
    ],
    author="John Stares",
    author_email="wisdom.achor@ust.edu.ng",
    description="A lightweight serializer for Flask-SQLAlchemy models",
    long_description=open("README.md").read()  if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/JohnStares/mini-flask-serializer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)