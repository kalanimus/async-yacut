# async-yacut

An async URL shortener built with Flask, featuring Yandex Disk file upload support.

## Features

- **URL shortening** — shorten long URLs with custom or auto-generated short IDs
- **File upload** — upload files to Yandex Disk with auto-generated short links
- **REST API** — full JSON API for URL shortening
- **Async uploads** — concurrent file uploads using asyncio + aiohttp

## Quick Start

```bash
git clone https://github.com/kalanimus/async-yacut.git
cd async-yacut

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env with your settings

# Initialize database
flask db upgrade

# Run
flask run
```

## Configuration

Create a `.env` file in the project root:

```
FLASK_APP=yacut
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your-yandex-disk-oauth-token  # optional, for file upload
```

## API

### Create short link

```json
POST /api/id/
{"url": "https://example.com", "custom_id": "ex"}

→ 201 {"url": "https://example.com", "short_link": "http://localhost/ex"}
```

### Resolve short link

```
GET /api/id/<short_id>/
→ 200 {"url": "https://example.com"}
```

## Running tests

```bash
pytest -v
```

## License

MIT
