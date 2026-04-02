# This project implements a simple ETL pipeline:

- Extracts data from REST Countries API

- Transforms nested JSON into tabular format

- Loads data into PostgresSQL (Docker)

- Visualizes data using Dash


## Tech Stack

- Python
- pandas
- requests
- PostgreSQL
- Docker
- Dash


## How to Run

1. Start PostgreSQL (Docker)
```bash
docker compose up -d
```

1. Run ETL pipeline
```bash
python main.py
```

1. Run Dashboard
```bash
python visualisation.py
```

1. Open in browser:
http://127.0.0.1:8050

## Notes

- API allows maximum 10 fields per request
- Some fields may be missing (e.g. capital)
- Currencies use dynamic keys (USD, EUR, etc.)

