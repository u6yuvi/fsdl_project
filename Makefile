# Arcane incantation to print all the other targets, from https://stackoverflow.com/a/26339924
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Install exact Python and CUDA versions
conda-update:
	conda env update --prune -f environment.yml
	echo "!!!RUN THE conda activate COMMAND ABOVE RIGHT NOW!!!"

# Install exact pip packages
pip-tools:
	pip install pip-tools==6.3.1 setuptools==59.5.0
	pip-sync semantic_search/fsdl_project.txt
	python -m build semantic_search
	pip install -e semantic_search

# Bump versions of transitive dependencies, compile
pip-tools-upgrade:
	pip install pip-tools==6.3.1 setuptools==59.5.0
	pip-compile -o semantic_search/fsdl_project.txt semantic_search/requirements/prod.in semantic_search/requirements/dev.in
	echo "!!!Run pip-tools command to actually update the environment"
	echo "!!! make pip-tools !!!"

# Fix lint as much as possible, give messages on the rest
# not running back as it makes too many changes, run it when needed
# python -m black .
lint:
	isort .
	flake8 .