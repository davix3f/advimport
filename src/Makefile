CURRENT_VERSION := $(shell cat setup.py | grep version | egrep -o '([0-9]\.*)+')
PY = 3
UPLOAD_URL = "https://upload.pypi.org/legacy/"
PKGNAME = $(shell cat setup.py | grep name | egrep -o '\"\w+\"')
getversion:
	@echo "Current version of $(PKGNAME) is $(CURRENT_VERSION)"

%:
# Create setup.py for a new version
# e.g 'make 2.3'
	@echo "From version $(CURRENT_VERSION) to $@"
	@sed -i 's/version.*=.*/version = \"$@\",/g' setup.py
	@echo "New version is: $@"

pack_py:
# generate directories for upload
# do 'make pack_py PY=[py version you want to use] to use a different python version
	@python$(PY) setup.py sdist

upload_twine:
# upload packages to pypi.
# do 'make upload_twine UPLOAD_URL=[custom url]' to upload to another pypi url
	@echo "Trying to upload package to $(UPLOAD_URL)\n" 
	@twine upload --repository-url $(UPLOAD_URL) dist/* && echo "\nUpload successful"
	clean

upload:
# upload packages to pypi using the configuration
# in ~/.pypirc
# do 'make upload PY=[python version you want to use]
# if you want to use a different version from 3
	@python$(PY) setup.py sdist upload && echo "\nUpload successful"

clean:
# remove generated directories
	@rm -rf build dist *.egg-info
	@echo "Generated directories deleted"

