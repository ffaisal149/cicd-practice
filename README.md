# cicd-practice

A learning sandbox for CI/CD with GitHub Actions: a deliberately small FastAPI app on
SQL Server, with Alembic migrations, a pytest suite and a one-page React front end.

**Everything here is synthetic.** This repository contains no proprietary code, no real
customer or company data, no real hostnames, and no secrets. The pipeline is the subject;
the app exists only to give it something to build, test and deploy.

## Run it locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="mssql+pymssql://sa:YOUR_LOCAL_PASSWORD@localhost:1433/practice"
alembic upgrade head
uvicorn app.main:app --reload     # http://127.0.0.1:8000/health
pytest -q
```

A local SQL Server, if you want one (on Apple Silicon, enable Rosetta in Docker Desktop):

```bash
docker run -d --name practice-sql -e ACCEPT_EULA=Y -e MSSQL_SA_PASSWORD='YOUR_LOCAL_PASSWORD' \
  -p 1433:1433 mcr.microsoft.com/mssql/server:2022-latest
docker exec practice-sql /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa \
  -P 'YOUR_LOCAL_PASSWORD' -C -Q "CREATE DATABASE practice"
```
