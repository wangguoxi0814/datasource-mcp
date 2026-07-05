from datasource_mcp import db_exe


def main():
    sql = "select * from chat_message limit 5;"
    result = db_exe(sql)
    print(f"result is {result}")


if __name__ == "__main__":
    main()
