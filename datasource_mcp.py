from fastmcp import FastMCP
from mysql.connector import connect, Error

# 初始化MCP服务
mcp = FastMCP("datasource-mcp")

def create_mysql_conn() -> connect:
    """
    创建Mysql连接
    :return:
    """
    try:
        conn = connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="aix",
            charset="utf8mb4",
            connection_timeout=5,
            use_pure=True,
        )
        return conn
    except Error as e:
        raise Exception(f"数据库连接失败:{str(e)}")

# 定义工具
@mcp.tool
def db_exe(sql: str) -> str:
    """
    执行任意SQL
    :param sql: sql语句
    :return: sql执行结果
    """
    if sql is None:
        return ""
    sql_lower = sql.strip().lower()
    try:
        conn = create_mysql_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_lower)
        result = cursor.fetchall()
    except Error as e:
        return "查询失败"
    finally:
        cursor.close()
        conn.close()
    return result

if __name__ == "__main__":
    # MCP标准stdio传输
    mcp.run(transport="stdio")