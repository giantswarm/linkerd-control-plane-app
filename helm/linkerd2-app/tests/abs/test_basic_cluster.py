import json
import logging
import os
import requests
import shutil
import subprocess  # nosec
import time
from typing import Dict

import pykube
import pytest
from pytest_helm_charts.fixtures import Cluster
from pytest_helm_charts.giantswarm_app_platform.custom_resources import AppCR
from pytest_helm_charts.utils import wait_for_deployments_to_run

from fixtures.fixtures import linkerd_app_cr, cni_app_cr, catalogs

logger = logging.getLogger(__name__)

timeout: int = 360


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
        check=False,
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
def test_prepare_cni(kube_cluster: Cluster, cni_app_cr: AppCR):
    """Install using the linkerd cni"""
    app_version = cni_app_cr.obj["status"]["appVersion"]
    logger.info(f"cni App CR shows installed appVersion {app_version}")


@pytest.mark.smoke
def test_installation(kube_cluster: Cluster, linkerd_app_cr: AppCR):
    """Test using the linkerd cli using 'check'"""
    app_version = linkerd_app_cr.obj["status"]["appVersion"]
    logger.info(f"Installed App CR shows installed appVersion {app_version}")

    linkerd_namespace = "linkerd2-app"
    cni_namespace = "linkerd2-cni-app"
    test_app_namespace = "helloworld"

    wait_for_deployments_to_run(
        kube_cluster.kube_client,
        [
            "linkerd-controller",
            "linkerd-destination",
            "linkerd-identity",
            "linkerd-proxy-injector",
            "linkerd-sp-validator",
        ],
        linkerd_namespace,
        timeout,
    )

    kube_cluster.kubectl("apply", filename="test-app-manifests.yaml", output=None)
    logger.info("Installed additional manifest with to be injected proxy")

    kube_cluster.kubectl("annotate namespace kube-system linkerd.io/inject=disabled")
    kube_cluster.kubectl("label namespace kube-system config.linkerd.io/admission-webhooks=disabled")

    get_linkerd_cli(app_version)

    curr = 0
    while curr < timeout:
        success = exec_linkerd_cli(kube_cluster.kube_config_path, cni_namespace, linkerd_namespace, test_app_namespace)["success"]
        if success:
            break
        time.sleep(1)

    cli_output = exec_linkerd_cli(kube_cluster.kube_config_path, cni_namespace, linkerd_namespace, test_app_namespace)

    logger.info(f"Final output of 'linkerd check`: {cli_output}")

    assert cli_output["success"]
