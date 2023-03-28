After initializing, you should run alembic code inside de web container:
docker-compose exec web alembic upgrade head
