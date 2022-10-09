# For details on Makefiles, see the section notes.

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: run-service-development

# start up Flask API service
run-service-development:
	@echo "+ $@"
	python ml_api/run.py

run-service-wsgi:
	@echo "+ $@"
	gunicorn --workers=1 --bind 0.0.0.0:5000 --chdir ml_api run:application