shell = ${SHELL}

# Text Formatting
NO_FORMAT	= \033[0m
BOLD		= \033[1m
RED 		= \033[31m
GREEN		= \033[32m

# Meta-Goals
.PHONY: help
.DEFAULT_GOAL := help
project := app
entrypoint := btc_ui.py

default:
	echo 'Makefile default target!'

##@ Section 1: Local Build Commands
.PHONY: build
build: ## Start the Crypto Coin Trading UI server
	$(info ******** Installing the Crypto Coin Trading UI ********)
	@bash -c "python -m pip install --upgrade pip && python -m pip install -r requirements.txt"
	@bash -c "python -m poetry install"

##@ Section 2: Local Run Commands
.PHONY: run
run: ## Start the Crypto Coin Trading UI server
	$(info ******** Running the Crypto Coin Trading UI ********)
	@bash -c "python -m poetry run streamlit run ${project}/${entrypoint}"

##@ Section 3: Kubernetes Environment Commands

##@ Section 4: Dockerfile Build Commands

##@ Section 5: Documentation

### Help Section
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
