from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pdfsplit",
    version="0.1",
    install_requires=requirements,
    entry_points=f"""
        [console_scripts]
        pdfsplit=split.main:split_pdf
    """,
)
