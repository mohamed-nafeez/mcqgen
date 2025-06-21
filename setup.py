from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='nafeez',
    author_email='mohamednafeez@gamil.com',
    install_requires=[
        "requests",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)
