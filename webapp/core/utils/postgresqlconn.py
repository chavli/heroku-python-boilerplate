import psycopg2
import psycopg2.extras
import psycopg2.pool
import os
import time
import traceback as tb
from io import StringIO


class PostgreSQLConn:
    isolation_opts = {
        "auto-commit": psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT,
        "read-committed": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    }
    __pool = psycopg2.pool.SimpleConnectionPool(1, 10, os.getenv("DATABASE_URL"))

    def __init__(self, dbname: str, isolation: str = "auto-commit"):
        # Establishes the connection with the backend databases.

        isolation_level = self.isolation_opts.get(isolation, psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        try:
            if dbname == "YOUR_DATABASE_NAME":
                self.__conn = self.__pool.getconn()
                self.__conn.set_isolation_level(isolation_level)
            else:
                self.__pool = None
                self.__conn = None
        except psycopg2.pool.PoolError as e:
            self.__pool = None
            self.__conn = None
            raise(e)
        except Exception as e:
            tb.print_exc()
            raise(e)

    def __enter__(self):
        """ implicity called before the first expression in a with-block """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ implicity called after the last expression within a with-block. exiting the with block also commits
        everything in the current transaction """
        self.__conn.commit()
        self.__del__()

        # https://infohost.nmt.edu/tcc/help/pubs/python/web/exit-method.html
        #   returning True surpresses any exceptions caused by the with block
        #   returning False implicitly raises exceptions caused by the with
        return False

    def __del__(self):
        """ implicitly called when garbage collections comes around to clean up objects.
        the database connection is returned to the pool """

        if self.__pool and self.__conn:
            self.__pool.putconn(self.__conn)
        self.__pool = None
        self.__conn = None

    def disconnect(self):
        """ close the connection. it doesn't return to the pool """
        if self.__pool and self.__conn:
            self.__pool.putconn(self.__conn, close=True)
        self.__pool = None
        self.__conn = None

    def commit_transaction(self):
        """ a function that allows explicit control over commiting transactions. this should be used when the
        isolation level is read-committed and you want control over when transactions are ended.
        """
        if self.__conn:
            self.__conn.commit()

    def rollback_transaction(self):
        """ explicit control over rolling back transactions. this will only work if the isolation level is
        set to read-committed. closing a connection without committing causes an implicit rollback """
        if self.__conn:
            self.__conn.rollback()

    def update_exact(self, table_name: str, conditions: dict, newvalues: dict) -> int:
        """ updates rows that match the given equality conditions with new values. both conditions
        and newvalues are dictionaries. kv pairs in conditions are translated into 'column = value'
        conditions and kv pairs in newvalues are used in the SET clause

        returns the number of rows updated
        """
        if not self.__conn:
            raise psycopg2.InterfaceError("null connection")

        try:
            pass
        except Exception as e:
            tb.print_exc()
            raise(e)

    def insert_one(self, table_name: str, row: dict, retcol: str):
        """ inserts a single row into the specified table and returns the value of the specified
        column.

        row - a dict containing all row values to insert

        returns: new id
        """
        if not self.__conn or not row:
            raise psycopg2.InterfaceError("null connection")

        try:
            columns = "(" + ",".join(row.keys()) + ")"
            holders = "(" + ",".join(["%s"] * len(row.keys())) + ")"
            fillers = tuple(row.values())
            query = "insert into {table_name} {columnnames} values {values} returning {retcol}".format(**{
                "table_name": table_name,
                "columnnames": columns,
                "values": holders,
                "retcol": retcol
                })

            with self.__conn.cursor() as curs:
                curs.execute(query, fillers)
                return curs.fetchone()[0]

        except Exception as e:
            tb.print_exc()
            raise(e)

    def insert_bulk(self, table_name: str, rows: list, unique_cols: list = []):
        """ just like insert except we use the postgres copy function to move new data from a temp
        table into the target table

        rows - a list of dicts representing all the new rows
        unique_cols - name of all unique columns. if duplicates are found then the newly given rows
            will overwrite the old rows.

        returns number of rows inserted or None on error
        """
        if not self.__conn or not rows:
            raise psycopg2.InterfaceError("null connection")

        # if the batch is small just resort to standard insert
        if not unique_cols and len(rows) < 10:
            return self.insert(table_name, rows)

        # The keys of the first dictionary in data are the column names we need
        cols = rows[0].keys()

        try:
            # Put the data into a string file-like object, in csv format
            csv = StringIO()
            for row in rows:
                # Strip all strings in values() and put them into a semicol del string
                tstr = "|".join([str(x).strip() for x in row.values()]) + "\n"
                csv.write(tstr)
            csv.seek(0)

            # Make a temp table to hold the imported data
            temptable = "{}_{}".format(table_name, int(time.time() * 100000))
            query = """
                    create temporary table {temptable} as
                        select {columns} from {table_name} where 1 = 0
                    """.format(**{
                    "temptable": temptable,
                    "columns": ",".join(cols),
                    "table_name": table_name
                })
            self.execute_write_query(query)

            with self.__conn.cursor() as curs:
                query = "copy {temptable} from stdin with null as 'None' delimiter '|'".format(
                         **{"temptable": temptable})
                curs.copy_expert(query, csv)

            # Delete duplicates from target table if unique_cols specified
            distinct = ""
            if unique_cols:
                colstr = ','.join(unique_cols)
                distinct = " distinct on ( {} ) ".format(colstr)
                where = " where ({}) in (select {} from {})".format(colstr, colstr, temptable)
                query = "delete from {} {}".format(table_name, where)
                self.execute_write_query(query)

            # Insert new rows into target
            query = "insert into %s (%s) select %s * from %s" % (table_name, ",".join(cols), distinct, temptable)
            n_inserted = self.execute_write_query(query)

            return n_inserted
        except Exception as e:
            tb.print_exc()
            raise(e)

    def insert(self, table_name: str, rows: list) -> int:
        """ inserts the given data into the specified table.

        An individual insert statement is generated per row. The query is handled as a prepared
        statement so multi-inserts are more efficient.

        table_name --
        rows -- list of dicts. each dict representing a row to be inserted

        returns: the number of rows inserted
        """
        n_inserted = 0
        if not self.__conn or not rows:
            raise psycopg2.InterfaceError("null connection")

        try:
            for row in rows:
                columns = "(" + ",".join(row.keys()) + ")"   # "(col1, col2, col3...)"
                params = ",".join(["%s"] * len(row.keys()))  # "%s, %s, %s..."

                query = "insert into {table_name} {columns} select {params}".format(**{
                    "table_name": table_name,
                    "columns": columns,
                    "params": params,
                    })

                n_inserted += self.execute_write_query(query, tuple(row.values()))
            return n_inserted
        except Exception as e:
            tb.print_exc()
            raise(e)

    def execute_read_query(self, query: str, args: tuple = ()) -> (list, list):
        """ results are returned as a list of dicts"""
        if not self.__conn:
            raise psycopg2.InterfaceError("null connection")

        rows = None

        try:
            with self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                curs.execute(query, args)
                rows = curs.fetchall()
        except Exception as e:
            tb.print_exc()
            raise(e)

        if len(rows) == 0:
            return []
        return rows

    def execute_write_query(self, query: str, args: tuple = ()) -> int:
        """ perform a write query

        query -- the query string with optional %s placeholders
        args -- optional tuple of values for %s placeholders

        returns number of rows modified
        """
        if not self.__conn:
            raise psycopg2.InterfaceError("null connection")

        try:
            with self.__conn.cursor() as curs:
                curs.execute(query, args)
        except Exception as e:
            tb.print_exc()
            raise(e)

        return curs.rowcount

    def generate_query(self, query: str, args: tuple = ()) -> str:
        """ return the query string, with the given parameters, that would be executed against the database.
        nothing is executed.
        """
        if not self.__conn:
            raise psycopg2.InterfaceError("null connection")

        try:
            with self.__conn.cursor() as curs:
                query_string = curs.mogrify(query, args)
        except Exception as e:
            tb.print_exc()
            raise(e)

        return query_string.decode("utf-8")
