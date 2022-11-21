

tunnel:
	localtunnel client --host https://localtunnel.me --subdomain lando --port 8000

tunnel-custom DOMAIN PORT:
	localtunnel client --host https://localtunnel.me --subdoman {{DOMAIN}} --port {{PORT}}	
