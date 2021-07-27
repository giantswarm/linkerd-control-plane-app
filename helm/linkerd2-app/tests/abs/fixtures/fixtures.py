from typing import List

import pytest
import yaml
from pykube import ConfigMap
from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.giantswarm_app_platform.app import AppFactoryFunc, ConfiguredApp
from pytest_helm_charts.giantswarm_app_platform.app_catalog import AppCatalogFactoryFunc
from pytest_helm_charts.giantswarm_app_platform.custom_resources import AppCR, AppCatalogCR
from pytest_helm_charts.utils import wait_for_namespaced_objects_condition

cni_app_version = "0.3.1-beta-68af46a45a03e1cfc304fa40a0022fb163edb2d3"

timeout = 120

#@pytest.fixture(scope="module")
#def catalogs(app_catalog_factory: AppCatalogFactoryFunc) -> List[AppCatalogCR]:
#    res: List[AppCatalogCR] = []
#    for cat_name in ["giantswarm", "giantswarm-test"]:
#        res.append(app_catalog_factory(cat_name, f"https://giantswarm.github.io/{cat_name}-catalog/"))
#


@pytest.fixture(scope="module")
def cni_app_cr(app_factory: AppFactoryFunc) -> ConfiguredApp:
    res = app_factory("linkerd2-cni-app",
                      cni_app_version,
                      "giantswarm-test",
                      "https://giantswarm.github.io/giantswarm-test-catalog/",
                      namespace_config_annotations={"linkerd.io/inject": "disabled"},
                      namespace_config_labels={
                          "linkerd.io/cni-resource": "true",
                          "config.linkerd.io/admission-webhooks": "disabled"
                      }
                      )
    return res


def user_configmap(filepath):
    with open(filepath, 'r', encoding='utf-8') as valuesfile:
        values = valuesfile.read()

    yaml_config = yaml.safe_load(values)
    return yaml_config


@pytest.fixture(scope="module")
def linkerd_app_cr(kube_cluster: Cluster, app_factory: AppFactoryFunc, chart_version: str) -> ConfiguredApp:
    app_name = "linkerd2-app"
    namespace = "linkerd2-app"
    config_map = user_configmap("test-values.yaml")
    app_factory(app_name,
                      chart_version,
                      "chartmuseum-test-time",
                      "http://chartmuseum-chartmuseum:8080/charts/",
                      namespace=namespace,
                      config_values=config_map,
                      namespace_config_annotations={"linkerd.io/inject": "disabled"},
                      namespace_config_labels={
                          "linkerd.io/is-control-plane": "true",
                          "config.linkerd.io/admission-webhooks": "disabled",
                          "linkerd.io/control-plane-ns": namespace
                      })
    apps = wait_for_namespaced_objects_condition(
        kube_cluster.kube_client,
        AppCR,
        [app_name],
        namespace,
        _app_deployed,
        timeout,
        True
    )
    return apps[0]


@pytest.fixture(scope="module")
def linkerd_app_cr_old(kube_cluster, chart_version):
    app_name = "linkerd2-app"
    app_cm_name = f"{app_name}-user-config"

    app_cm = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": app_cm_name, "namespace": "giantswarm"},
        "data": {"values": user_configmap("test-values.yaml")}
    }
    app_cm_obj = ConfigMap(kube_cluster.kube_client, app_cm)
    app_cm_obj.create()

    app = app_cr_obj(
        app_name,
        "chartmuseum",
        chart_version,
        namespace_config_annotations={"linkerd.io/inject": "disabled"},
        namespace_config_labels={
            "linkerd.io/is-control-plane": "true",
            "config.linkerd.io/admission-webhooks": "disabled",
            "linkerd.io/control-plane-ns": app_name
        }
    )
    app["spec"]["userConfig"] = {
        "configMap": {"name": app_cm_name, "namespace": "giantswarm"}
    }

    app_obj = AppCR(kube_cluster.kube_client, app)
    app_obj.create()
    apps = wait_for_namespaced_objects_condition(
        kube_cluster.kube_client,
        AppCR,
        [app_name],
        "giantswarm",
        _app_deployed,
        timeout,
        True
    )

    return apps[0]


def _app_deployed(app: AppCR) -> bool:
    complete = (
            "status" in app.obj
            and "release" in app.obj["status"]
            and "appVersion" in app.obj["status"]
            and "status" in app.obj["status"]["release"]
            and app.obj["status"]["release"]["status"] == "deployed"
    )
    return complete
