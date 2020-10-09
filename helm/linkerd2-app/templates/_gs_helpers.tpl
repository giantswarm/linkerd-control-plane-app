{{/* vim: set filetype=mustache: */}}
{{/*
Set cert-manager API group based on .Values.global.cert-manager.version.
*/}}
{{- define "cert-manager.apigroup" -}}
{{- if semverCompare ">=0.11.0" .Values.global.certManager.version -}}
{{- printf "%s" "cert-manager.io" -}}
{{- else -}}
{{- printf "%s" "certmanager.k8s.io" -}}
{{- end }}
{{- end -}}

{{/*
Set cert-manager API versions based on .Values.global.cert-manager.version.
*/}}
{{- define "cert-manager.apiversion" -}}
{{- if semverCompare ">=0.11.0" .Values.global.certManager.version -}}
{{- printf "%s" "cert-manager.io/v1alpha2" -}}
{{- else -}}
{{- printf "%s" "certmanager.k8s.io/v1alpha1" -}}
{{- end }}
{{- end -}}
