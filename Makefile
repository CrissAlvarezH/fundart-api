

updb:
	docker-compose up database

rmdb:
	docker-compose down
	docker volume ls
	docker volume rm fundart_api_dbdata