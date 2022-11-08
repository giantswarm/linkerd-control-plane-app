##@ Chart

YQ=docker run --rm -u $$(id -u) -v $${PWD}:/workdir mikefarah/yq:4.29.2
HELM_DOCS=docker run --rm -u $$(id -u) -v $${PWD}:/helm-docs jnorwood/helm-docs:v1.11.0

MAIN_CHART=helm/linkerd-control-plane
DEPS := $(shell ls $(MAIN_CHART)/charts)

.PHONY: update-chart helm-docs update-deps $(DEPS)

update-chart: ## Sync chat with upstream repo.
	@echo "====> $@"
	vendir sync
	$(MAKE) update-deps

update-deps: $(DEPS) ## Update Helm dependencies.
	cd $(MAIN_CHART) && helm dependency update

$(DEPS): ## Update main Chart.yaml with new local dep versions.
	new_version=`$(YQ) .version $(MAIN_CHART)/charts/$@/Chart.yaml` && \
	$(YQ) -i e "with(.dependencies[]; select(.name == \"$@\") | .version = \"$$new_version\")" $(MAIN_CHART)/Chart.yaml

helm-docs: ## Update $(MAIN_CHART) README.
	$(HELM_DOCS) -c $(MAIN_CHART) -g $(MAIN_CHART)
