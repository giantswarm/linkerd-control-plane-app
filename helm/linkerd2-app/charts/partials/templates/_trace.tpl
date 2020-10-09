{{ define "partials.linkerd.trace" -}}
{{ if .Values.global.controlPlaneTracing -}}
- -trace-collector=linkerd-collector.{{.Release.namespace}}.svc.{{.Values.global.clusterDomain}}:55678
{{ end -}}
{{- end }}
