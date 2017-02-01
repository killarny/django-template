# {{project_name}}


## Setting up a development environment

1. Build and start the stack:

    ```bash
    docker-compose up -d
    ```

1. Create a superuser to access the admin:

    ```bash
    docker-compose run --rm site ./manage.py createsuperuser
    ```

## Typical development tasks

### Admin

Visit the admin in your browser at: [https://localhost/admin](https://localhost/admin)

### Run tests

Use the Django test framework to run project tests:

```bash
docker-compose run --rm site ./manage.py test
```

### Django shell

Enter a Django shell:

```bash
docker-compose run --rm site ./manage.py shell
```

### Postgres shell

Enter a PostgreSQL shell connected to the project database:

```bash
docker-compose exec database psql
```