# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

tunnel:
	localtunnel client --host https://localtunnel.me --subdomain lando --port 8000

tunnel-custom DOMAIN PORT:
	localtunnel client --host https://localtunnel.me --subdomain {{DOMAIN}} --port {{PORT}}	
