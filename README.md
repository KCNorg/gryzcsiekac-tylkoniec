```
poetry install
docker-compose up -d
poetry run alembic upgrade head
poetry run python src/main.py
```

Db credentials
```
l: postgres
p: postgres
```

```
alembic revision --autogenerate -m ""
poetry run alembic downgrade -1
```
