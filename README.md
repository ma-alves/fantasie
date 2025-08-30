# Fantasie
Fantasie is a RESTful API for costume rental with JWT Authentication using Python, FastAPI and SQLite3 as its core technologies.

## Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) - Web Framework
- [SQLite3](https://www.sqlite.org/index.html) - Database
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL Toolkit and ORM
- [Docker](https://www.docker.com/) - Environment Setup
- [GitHub Actions](https://docs.github.com/en/actions) - CI
- [Pytest](https://docs.pytest.org/en/8.2.x/) - Testing
- [PyJWT](https://pypi.org/project/PyJWT/) - Authentication
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Migrations

## Getting Started
1. Clone this repository:\
`git clone https://github.com/ma-alves/fantasie.git`
2. Copy the environment variables to .env and change the values:\
`cp .env.example .env`
3. Create a database file:\
`touch database.db`
4. Build the image:\
`docker build -t fantasie:v1 .`
5. Run the container with a volume:\
`docker run -v fantasie-data:/app --publish 8000:8000 --name fantasie-container fantasie:v1`
6. Go to http://localhost:8000/docs to access the API Swagger.

## Executing Tests
1. After building the image, run the container without the volume in detached mode:\
`docker run -d --publish 8000:8000 --name fantasie-container fantasie:v1`
2. Then run the following command:\
`docker exec -it fantasie-container task test`
3. All tests should pass :) 
