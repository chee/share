import setuptools

with open("readme.org", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="share-snootclub",
	version="0.0.0",
	author="chee",
	author_email="chee@snoot.club",
	description="share to share.snoot.club",
	long_description=long_description,
	long_description_content_type="text/org",
	url="https://git.snoot.club/chee/share",
	packages=setuptools.find_packages(),
	python_requires=">= 3.6",
	entry_points={
		'console_scripts': [
			"share = share.__main__:main"
		]
	}
)
