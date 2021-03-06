PACKAGE_NAME=psh

dist: clean
	test ! -z "${VIRTUAL_ENV}" && python3 setup.py sdist bdist_wheel

upload-test: dist
	test ! -z "${VIRTUAL_ENV}" && twine upload --repository-url https://test.pypi.org/legacy/ dist/*

install-test:
	test ! -z "${VIRTUAL_ENV}" && python3 -m pip install --index-url https://test.pypi.org/simple/ "${PACKAGE_NAME}"

upload-prod: dist
	test ! -z "${VIRTUAL_ENV}" && twine upload dist/*
	

clean:
	rm -rf dist/

.PHONY: clean dist upload-test install-test upload-prod
