{{- define "linkerd.configs.global" -}}
{
  "linkerdNamespace": "{{.Namespace}}",
  "cniEnabled": false,
  "version": "{{.LinkerdVersion}}",
  "identityContext":{
    "trustDomain": "{{.Identity.TrustDomain}}",
{{if and (.Identity.Issuer) (eq .Identity.Issuer.Scheme "linkerd.io/cert-manager") -}}
    "trustAnchorsPem": "REPLACE_ME",
{{- end}}
{{if and (.Identity.Issuer) (eq .Identity.Issuer.Scheme "linkerd.io/tls") -}}
    "trustAnchorsPem": "{{required "Please provide the identity trust anchors" .Identity.TrustAnchorsPEM | trim | replace "\n" "\\n"}}",
{{- end}}
    "issuanceLifeTime": "{{.Identity.Issuer.IssuanceLifeTime}}",
    "clockSkewAllowance": "{{.Identity.Issuer.ClockSkewAllowance}}",
    "scheme": "{{.Identity.Issuer.Scheme}}"
  },
  "autoInjectContext": null,
  "omitWebhookSideEffects": {{.OmitWebhookSideEffects}},
  "clusterDomain": "{{.ClusterDomain}}"
}
{{- end -}}

{{- define "linkerd.configs.proxy" -}}
{
  "proxyImage":{
    "imageName":"{{.Proxy.Image.Name}}",
    "pullPolicy":"{{.Proxy.Image.PullPolicy}}"
  },
  "proxyInitImage":{
    "imageName":"{{.ProxyInit.Image.Name}}",
    "pullPolicy":"{{.ProxyInit.Image.PullPolicy}}"
  },
  "controlPort":{
    "port": {{.Proxy.Ports.Control}}
  },
  "ignoreInboundPorts":[
    {{- $ports := splitList "," .ProxyInit.IgnoreInboundPorts -}}
    {{- if gt (len $ports) 1}}
    {{- $last := sub (len $ports) 1 -}}
    {{- range $i,$port := $ports -}}
    {"port":{{$port}}}{{ternary "," "" (ne $i $last)}}
    {{- end -}}
    {{- end -}}
  ],
  "ignoreOutboundPorts":[
    {{- $ports := splitList "," .ProxyInit.IgnoreOutboundPorts -}}
    {{- if gt (len $ports) 1}}
    {{- $last := sub (len $ports) 1 -}}
    {{- range $i,$port := $ports -}}
    {"port":{{$port}}}{{ternary "," "" (ne $i $last)}}
    {{- end -}}
    {{- end -}}
  ],
  "inboundPort":{
    "port": {{.Proxy.Ports.Inbound}}
  },
  "adminPort":{
    "port": {{.Proxy.Ports.Admin}}
  },
  "outboundPort":{
    "port": {{.Proxy.Ports.Outbound}}
  },
  "resource":{
    "requestCpu": "{{.Proxy.Resources.CPU.Request}}",
    "limitCpu": "{{.Proxy.Resources.CPU.Limit}}",
    "requestMemory": "{{.Proxy.Resources.Memory.Request}}",
    "limitMemory": "{{.Proxy.Resources.Memory.Limit}}"
  },
  "proxyUid": {{.Proxy.UID}},
  "logLevel":{
    "level": "{{.Proxy.LogLevel}}"
  },
  "disableExternalProfiles": {{not .Proxy.EnableExternalProfiles}},
  "proxyVersion": "{{.Proxy.Image.Version}}",
  "proxyInitImageVersion": "{{.ProxyInit.Image.Version}}"
}
{{- end -}}

{{- define "linkerd.configs.install" -}}
{
  "cliVersion":"{{ .LinkerdVersion }}",
  "flags":[]
}
{{- end -}}
