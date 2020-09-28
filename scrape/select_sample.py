import os
import psycopg2

DATABASE_URL='postgresql://postgres:postgres@postgres:5432/metabase'

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def main():
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select domain_name, title from contents;'
    
    cur.execute(sql)
    
    results = cur.fetchall() 
    for row in results: 
        print(row)

    cur.close()

if __name__ == '__main__':
    main()