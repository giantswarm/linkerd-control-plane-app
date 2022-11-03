##@ Chart

MAIN_CHART=helm/linkerd-control-plane
VENDOR_CHART_LINKERD=vendor/linkerd/charts/linkerd-control-plane
VENDOR_CHART_PARTIALS=vendor/linkerd/charts/partials
VENDOR_CHART_CRDS=vendor/linkerd/charts/linkerd-crds


.PHONY: update-chart helm-docs apply-vendor update-deps
update-chart: ## Run vendir sync
	@echo "====> $@"
	vendir sync
	$(MAKE) apply-vendor
	$(MAKE) update-deps

update-deps:
	new_version=`docker run --rm -u $$(id -u) -v "$${PWD}":/workdir mikefarah/yq .version $(MAIN_CHART)/charts/linkerd-crds/Chart.yaml` && \
	docker run --rm -u $$(id -u) -v "$${PWD}":/workdir mikefarah/yq -i e "with(.dependencies[]; select(.name == \"linkerd-crds\") | .version = \"$$new_version\")" $(MAIN_CHART)/Chart.yaml
	cd $(MAIN_CHART) && helm dependency update

helm-docs:
	docker run --rm --volume "`pwd`:/helm-docs" -u `id -u` jnorwood/helm-docs:latest -c $(MAIN_CHART) -g $(MAIN_CHART)

apply-vendor:
	mkdir -p $(MAIN_CHART)/charts
	rm -rf $(MAIN_CHART)/templates
	rm -rf $(MAIN_CHART)/charts/partials
	rm -rf $(MAIN_CHART)/charts/linkerd-crds
	cp -r $(VENDOR_CHART_LINKERD)/templates $(MAIN_CHART)
	cp -r $(VENDOR_CHART_PARTIALS) $(MAIN_CHART)/charts/
	cp -r $(VENDOR_CHART_CRDS) $(MAIN_CHART)/charts/
