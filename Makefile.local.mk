##@ Chart

YQ=docker run --rm -u $$(id -u) -v $${PWD}:/workdir mikefarah/yq
HELM_DOCS=docker run --rm -u $$(id -u) -v $${PWD}:/helm-docs jnorwood/helm-docs:latest

MAIN_CHART=helm/linkerd-control-plane
DEPS := $(shell ls $(MAIN_CHART)/charts)

.PHONY: update-chart helm-docs update-deps $(DEPS)
update-chart: ## Run vendir sync
	@echo "====> $@"
	vendir sync
	$(MAKE) update-deps

update-deps: $(DEPS)
	cd $(MAIN_CHART) && helm dependency update

$(DEPS):
	new_version=`$(YQ) .version $(MAIN_CHART)/charts/$@/Chart.yaml` && \
	$(YQ) -i e "with(.dependencies[]; select(.name == \"$@\") | .version = \"$$new_version\")" $(MAIN_CHART)/Chart.yaml

helm-docs:
	$(HELM_DOCS) -c $(MAIN_CHART) -g $(MAIN_CHART)
