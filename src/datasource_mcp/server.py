import json
import os
from contextlib import contextmanager
from datetime import date, datetime
from decimal import Decimal

from fastmcp import FastMCP
from mysql.connector import connect, Error

mcp = FastMCP("datasource-mcp")

DEFAULT_MAX_ROWS = 100
READ_SQL_PREFIXES = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")


def _json_default(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def get_db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "database": os.getenv("DB_NAME", "aix"),
        "charset": "utf8mb4",
        "connection_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "5")),
        "use_pure": True,
    }


def _format_success(payload: dict) -> str:
    return json.dumps({"success": True, **payload}, ensure_ascii=False, default=_json_default)


def _format_error(message: str) -> str:
    return json.dumps({"success": False, "error": message}, ensure_ascii=False)


def _is_read_sql(sql: str) -> bool:
    first_token = sql.strip().split(maxsplit=1)[0].upper()
    return first_token in READ_SQL_PREFIXES


@contextmanager
def mysql_cursor():
    conn = None
    cursor = None
    try:
        conn = connect(**get_db_config())
        cursor = conn.cursor(dictionary=True)
        yield cursor
        conn.commit()
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@mcp.tool
def db_exe(sql: str, max_rows: int = DEFAULT_MAX_ROWS) -> str:
    """
    执行 SQL 并返回 JSON 字符串结果。
    :param sql: SQL 语句
    :param max_rows: 查询最大返回行数，防止结果过大导致 MCP 超时
    :return: JSON 字符串，格式为 {"success": true/false, ...}
    """
    if not sql or not sql.strip():
        return _format_error("SQL 不能为空")

    sql = sql.strip()
    max_rows = max(1, min(max_rows, 1000))

    try:
        with mysql_cursor() as cursor:
            cursor.execute(sql)

            if _is_read_sql(sql):
                rows = cursor.fetchmany(max_rows + 1)
                truncated = len(rows) > max_rows
                if truncated:
                    rows = rows[:max_rows]
                return _format_success(
                    {
                        "row_count": len(rows),
                        "truncated": truncated,
                        "rows": rows,
                    }
                )

            return _format_success({"affected_rows": cursor.rowcount})
    except Error as e:
        return _format_error(f"数据库错误: {e}")
    except Exception as e:
        return _format_error(f"执行失败: {e}")


def main() -> None:
    mcp.run(transport="stdio")
