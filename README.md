# datasource-mcp

MySQL datasource MCP server for AI clients (Cursor, Claude Desktop, etc.).

## Install

```bash
pip install datasource-mcp
# or
uvx datasource-mcp
```

## Cursor / MCP Client Config

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

## Local Development

```bash
uv sync
uv run datasource-mcp
# or
uv run python -m datasource_mcp
```
