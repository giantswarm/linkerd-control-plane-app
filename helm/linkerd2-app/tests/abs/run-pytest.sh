pipenv run pytest \
  -s \
  -o log_cli=true -o log_cli_level=INFO \
  -m smoke \
    --cluster-type external \
    --kube-config /abs/workdir/kubebox-kubeconfig \
    --chart-path linkerd2-app-0.6.0-beta-07a64af04fd847c0162b6816286452c05de1d5d6.tgz \
    --chart-version 0.6.0-beta-07a64af04fd847c0162b6816286452c05de1d5d6 \
    --chart-extra-info external_cluster_version=1.21.1 \
    --log-cli-level info
