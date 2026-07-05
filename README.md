# datasource-mcp

MySQL datasource MCP server for AI clients (Cursor, Claude Desktop, etc.).

> **Database Support:** Currently supports **MySQL only**. Support for PostgreSQL, SQLite, and other databases is planned for future releases.

## Install

```bash
pip install datasource-mcp
```

If the package is not yet available on your PyPI mirror, use the official index:

```bash
pip install datasource-mcp -i https://pypi.org/simple/
```

Or run without installing (requires [uv](https://docs.astral.sh/uv/)):

```bash
uvx datasource-mcp
```

> **Note:** `uvx datasource-mcp` downloads the package and immediately starts the MCP stdio server. It will block the terminal while waiting for a client connection. Configure it in your MCP client instead of running it manually.

## Cursor / MCP Client Config

### Option 1: pip install (local environment)

Run `pip install datasource-mcp` first, then add this to `mcp.json`:

```json
{
  "mcpServers": {
    "datasource-mcp": {
      "command": "datasource-mcp",
      "env": {
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "3306",
        "DB_USER": "root",
        "DB_PASSWORD": "your_password",
        "DB_NAME": "your_database"
      }
    }
  }
}
```

### Option 2: uvx without installing (recommended)

No `pip install` required — `uvx` fetches the package from PyPI and runs it automatically. Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) to be installed.

```json
{
  "mcpServers": {
    "datasource-mcp": {
      "command": "uvx",
      "args": ["datasource-mcp"],
      "env": {
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "3306",
        "DB_USER": "root",
        "DB_PASSWORD": "your_password",
        "DB_NAME": "your_database"
      }
    }
  }
}
```

After updating the config, click **Refresh** in the MCP panel to apply changes.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `127.0.0.1` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | `root` | MySQL password |
| `DB_NAME` | `aix` | Database name |
| `DB_CONNECT_TIMEOUT` | `5` | Connection timeout (seconds) |

## Tools

### `db_exe`

Execute SQL and return a JSON string:

```json
{"success": true, "row_count": 1, "truncated": false, "rows": [...]}
```

Error response:

```json
{"success": false, "error": "error message"}
```

## Local Development

```bash
uv sync
uv run datasource-mcp
# or
uv run python -m datasource_mcp
```

Requires Python >= 3.11.
