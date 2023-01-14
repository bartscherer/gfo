SHELL := /bin/bash
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#+                                                                           +#
#+       THIS MAKEFILE WILL HELP YOU START WORKING WITH THE UNDERLYING       +#
#+     REPOSITORY. SHOW HELP VIA 'make' OR 'make help' IN YOUR TERMINAL.     +#
#+                                                                           +#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

.ONESHELL:

##@ HELPERS

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

##@ TASKS

requirements_local_syntax_highlighting: ## Install the requirements into the actual environment to get VS Code autocompletion
	@echo "[*] Installing requirements.txt into the non-virtual environment..."
	@pip3 install -r gfo/requirements.txt
	@echo "[*] Successfully installed requirements"

pyenv: ## Setup a python virtual environment
	@echo "[*] Creating the python virtual environment..."
	@sudo apt install python3.10-venv -y
	@/bin/env python3 -m venv ./.python-virtual-environment
	@echo "[*] Done!"

requirements: pyenv ## Install the requirements into the virtual environment
	@source .python-virtual-environment/bin/activate
	@echo "[*] Installing requirements.txt into the virtual environment..."
	@pip3 install -r gfo/requirements.txt
	@echo "[*] Successfully installed requirements"

run: requirements ## Run the server
	@source .python-virtual-environment/bin/activate
	@echo "[*] Running the FastAPI application via gunicorn now..."
	@cd gfo
	@/bin/bash process_wrapper.sh -p false
	@echo "[*] Server exited"

run-docker: ## Run the server dockerized
	@docker build --no-cache -t gfo:latest .
	@docker run --publish 80:80 gfo
