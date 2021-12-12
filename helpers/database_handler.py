import sqlite3
from sqlite3 import Error



def query_all_tables( db_fullpath: str ) -> dict:
    tables = ['credible_refs', 'infamous_refs', 'neutral_sites']
    db_conn = None

    try:
        db_conn = sqlite3.connect( db_fullpath )
    except Error as e:
        print( f'Database connection error: {e}' )
        return

    results = dict()

    for table in tables:
        table_content = list()

        with db_conn:
            query = f'SELECT * FROM {table};'
            cursor = db_conn.cursor()
            cursor.execute( query )
            rows = cursor.fetchall()

            for row in rows:
                table_content.append( row[0].strip() )

            results[table] = table_content

    return results