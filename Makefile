extract :
	pybabel extract --input-dirs=. -o locales/messages.pot

init :
	pybabel init -i locales/messages.pot -d locales -D messages -l uz
	pybabel init -i locales/messages.pot -d locales -D messages -l ru
	pybabel init -i locales/messages.pot -d locales -D messages -l en

update :
	pybabel update -d locales -D messages -i locales/messages.pot

compile :
	pybabel compile -d locales -D messages

admin:
	uvicorn web.app:app --host=localhost --port=8000