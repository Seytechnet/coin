import psycopg2


def main():
    conn = psycopg2.connect('postgres://avnadmin:AVNS_XM80rUTI1A96C569XYl@pg-1318a66-akinfenwaobaseyi03-b760.k.aivencloud.com:22655/defaultdb?sslmode=require')

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(version)


if __name__ == "__main__":
    main()