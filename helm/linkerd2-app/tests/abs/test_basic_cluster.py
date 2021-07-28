import json
import logging
import os
import shutil
import subprocess  # nosec
from typing import Dict

import pykube
import pytest
import pytest_helm_charts.giantswarm_app_platform.custom_resources
import requests
import yaml
from pytest_helm_charts.fixtures import Cluster
from pytest_helm_charts.giantswarm_app_platform.app import AppFactoryFunc
from pytest_helm_charts.giantswarm_app_platform.custom_resources import AppCR
from pytest_helm_charts.utils import wait_for_deployments_to_run, ensure_namespace_exists

logger = logging.getLogger(__name__)

timeout: int = 360
cni_app_version = "0.3.1-beta-68af46a45a03e1cfc304fa40a0022fb163edb2d3"


def get_linkerd_cli(version):
    url = f"https://github.com/linkerd/linkerd2/releases/download/{version}/linkerd2-cli-{version}-linux-amd64"
    logger.info(f"Downloading linkerd-cli from url '{url}'")
    local_filename = "linkerd-cli"
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    os.chmod(local_filename, 0o755)


def exec_linkerd_cli(kube_config_path, cni_namespace, namespace, app_namespace):
    result = subprocess.run([
        "./linkerd-cli",
        "check",
        "--kubeconfig", kube_config_path,
        "--cni-namespace", cni_namespace,
        "--linkerd-namespace", namespace,
        "--proxy",
        "--namespace", app_namespace,
        "--output", "json",
    ],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=None,
    ).stdout

    return json.loads(result)


@pytest.mark.smoke
def test_api_working(kube_cluster: Cluster) -> None:
    """
    Test if the kubernetes api works
    """
    assert kube_cluster.kube_client is not None
    assert len(pykube.Node.objects(kube_cluster.kube_client)) >= 1


@pytest.mark.smoke
def test_cluster_info(
        kube_cluster: Cluster, cluster_type: str, chart_extra_info: Dict[str, str]
) -> None:
    """Test if the culster_info is available"""
    logger.info(f"Running on cluster type {cluster_type}")
    key = "external_cluster_type"
    if key in chart_extra_info:
        logger.info(f"{key} is {chart_extra_info[key]}")
    assert kube_cluster.kube_client is not None
    assert cluster_type != ""


@pytest.mark.smoke
def test_linkerd_cni_deployed(kube_cluster: Cluster, app_factory: AppFactoryFunc):
    """Install using the linkerd cni"""
    app_name = "linkerd2-cni-app"
    app_factory(app_name,
                cni_app_version,
                "giantswarm-test",
                "https://giantswarm.github.io/giantswarm-test-catalog/",
                namespace_config_annotations={"linkerd.io/inject": "disabled"},
                namespace_config_labels={
                    "linkerd.io/cni-resource": "true",
                    "config.linkerd.io/admission-webhooks": "disabled"
                }
                )
    app_cr = AppCR.objects(kube_cluster.kube_client).get_by_name(app_name)
    app_version = app_cr.obj["status"]["version"]
    assert app_version == cni_app_version
    logger.info(f"cni App CR shows installed appVersion {app_version}")


def load_yaml_from_path(filepath):
    with open(filepath, 'r', encoding='utf-8') as values_file:
        values = values_file.read()

    yaml_config = yaml.safe_load(values)
    return yaml_config


@pytest.mark.smoke
def test_linkerd_deployed(kube_cluster: Cluster, app_factory: AppFactoryFunc, chart_version: str):
    """Test using the linkerd cli using 'check'"""
    app_name = "linkerd2-app"
    namespace = "linkerd"
    ensure_namespace_exists(kube_cluster.kube_client, namespace)
    res = app_factory(app_name,
                      chart_version,
                      "chartmuseum-test-time",
                      "http://chartmuseum-chartmuseum:8080/charts/",
                      timeout_sec=timeout,
                      namespace=namespace,
                      config_values=load_yaml_from_path("test-values.yaml"),
                      namespace_config_annotations={"linkerd.io/inject": "disabled"},
                      namespace_config_labels={
                          "linkerd.io/is-control-plane": "true",
                          "config.linkerd.io/admission-webhooks": "disabled",
                          "linkerd.io/control-plane-ns": namespace
                      })

    app_cr = AppCR.objects(kube_cluster.kube_client).get_by_name(app_name)
    app_version = app_cr.obj["status"]["version"]
    assert app_version == chart_version
    wait_for_deployments_to_run(
        kube_cluster.kube_client,
        [
            "linkerd-controller",
            "linkerd-destination",
            "linkerd-identity",
            "linkerd-proxy-injector",
            "linkerd-sp-validator",
        ],
        namespace,
        timeout,
    )
    logger.info(f"Installed App CR shows installed appVersion {app_version}")

# @pytest.mark.functional
# def test_linkerd_cli_check_passes(kube_cluster: Cluster, linkerd_app_cr: AppCR):
#    app_version = linkerd_app_cr.obj["status"]["appVersion"]
#    kube_cluster.kubectl("apply", filename="test-app-manifests.yaml", output=None)
#    logger.info("Installed additional manifest with to be injected proxy")
#
#    kube_cluster.kubectl("annotate namespace kube-system linkerd.io/inject=disabled")
#    kube_cluster.kubectl("label namespace kube-system config.linkerd.io/admission-webhooks=disabled")
#
#    get_linkerd_cli(app_version)
#
#    curr = 0
#    while curr < timeout:
#        success = exec_linkerd_cli(kube_cluster.kube_config_path, cni_namespace, linkerd_namespace, test_app_namespace)["success"]
#        if success:
#            break
#        time.sleep(1)
#
#    cli_output = exec_linkerd_cli(kube_cluster.kube_config_path, cni_namespace, linkerd_namespace, test_app_namespace)
#
#    logger.info(f"Final output of 'linkerd check`: {cli_output}")
#
#    assert cli_output["success"]
#
