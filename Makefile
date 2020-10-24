test:
	pipenv run pytest -sx

lint:
	pipenv run pre-commit run -a -v

update-precommit:
	pipenv run pre-commit autoupdate
