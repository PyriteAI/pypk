from setuptools import find_packages, setup

setup(
    name="pypk",
    author="Miller Wilt",
    author_email="miller@pyriteai.com",
    description="An opinionated Python package template generator",
    packages=find_packages("src"),
    package_dir={"": "src"},
    use_scm_version={"write_to": "src/pypk/version.py"},
    setup_requires=["setuptools_scm"],
    python_requires=">=3.6.0",
)
