# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

# read env variables
set dotenv-load

tunnel:
	localtunnel client --host https://localtunnel.me --subdomain lando --port $SERVER_PORT

tunnel-custom DOMAIN PORT:
	localtunnel client --host https://localtunnel.me --subdomain {{DOMAIN}} --port {{PORT}}	

test-api: run-local-new
	src/consumer.py

test-worker:
	python src/consumer.py
	Invoke-Item generated/A_photo_of_an_astronaut_on_mars.png

test-worker-custom PROMPT:
	python src/consumer.py "{{PROMPT}}"
	Invoke-Item generated/{{replace(PROMPT, ' ', '_')}}.png

call-api PROMPT STEPS:
	python src/consumer.py --prompt "{{PROMPT}}" --steps {{STEPS}}
	just open-last

call-api-seeded PROMPT STEPS SEED:
	python src/consumer.py --prompt "{{PROMPT}}" --steps {{STEPS}} --seed {{SEED}}
	just open-last

open-last:
	cd generated
	Get-Childitem | sort lastwritetime | select -last 1 | Get-ItemPropertyValue -Name Name | Invoke-Item
	cd ..

run:
	start powershell -ArgumentList "-noexit", "-command &{just tunnel}"
	start powershell -ArgumentList "-noexit", "-command &{python src/app.py}"
			
run-local:
	python src/app.py
	
run-local-new:
	start powershell -ArgumentList "-noexit", "-command &{just run-local}"
	