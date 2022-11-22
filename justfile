# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

tunnel:
	localtunnel client --host https://localtunnel.me --subdomain lando --port 5000

tunnel-custom DOMAIN PORT:
	localtunnel client --host https://localtunnel.me --subdomain {{DOMAIN}} --port {{PORT}}	

test-api: run-local-new
	src/consumer.py

run:
	start powershell -ArgumentList "-noexit", "-command &{just tunnel}"
	start powershell -ArgumentList "-noexit", "-command &{python src/app.py}"
			
run-local:
	conda activate torch
	python src/app.py
	
run-local-new:
	start powershell -ArgumentList "-noexit", "-command &{just run-local}"
	