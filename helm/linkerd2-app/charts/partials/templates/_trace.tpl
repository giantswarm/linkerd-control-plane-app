{{ define "partials.linkerd.trace" -}}
{{ if .Values.global.controlPlaneTracing -}}
- -trace-collector=linkerd-collector.{{.Release.Namespace}}.svc.{{.Values.global.clusterDomain}}:55678
{{ end -}}
{{- end }}

{{ define "partials.setControlPlaneTracing.proxy" -}}
{{ if .Values.global.controlPlaneTracing -}}
{{ $_ := set .Values.global.proxy.trace "collectorSvcAddr" (printf "linkerd-collector.%s.svc.%s:55678" .Release.Namespace .Values.global.clusterDomain) -}}
{{ $_ := set .Values.global.proxy.trace "collectorSvcAccount" (printf "linkerd-collector.%s" .Release.Namespace) -}}
{{ end -}}
{{- end }}
