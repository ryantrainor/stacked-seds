test:
	cd tests && pytest

lint:
	cd src && pylint image.py | pylint plot.py