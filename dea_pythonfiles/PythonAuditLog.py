import pyodbc
import logging
import time


class LogDBHandler(logging.Handler):
    """
    Customized logging handler that puts logs to the database.
    """

    def __init__(self, sql_conn, sql_cursor, db_tbl_log):
        logging.Handler.__init__(self)
        self.sql_cursor = sql_cursor
        self.sql_conn = sql_conn
        self.db_tbl_log = db_tbl_log

    def emit(self, record):
        # Set current time
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
        # Clear the log message so it can be put to db via sql (escape quotes)
        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace("'", "''")
        # Make the SQL insert
        sql = (
            "INSERT INTO dbo."
            + self.db_tbl_log
            + " (log_level, "
            + "log_levelname, log, created_at, created_by) "
            + "VALUES ("
            + ""
            + str(record.levelno)
            + ", "
            + "'"
            + str(record.levelname)
            + "', "
            + "'"
            + str(self.log_msg)
            + "', "
            + "(convert(datetime2(7), '"
            + tm
            + "')), "
            + "'"
            + str(record.name)
            + "')"
        )
        try:
            self.sql_cursor.execute(sql)
            self.sql_conn.commit()
        # If error - print it out on screen. Since DB is not working - there's
        # no point making a log about it to the database :)
        except pyodbc.Error as e:
            print(sql)
            print("Failed connection to database for logging.")


def PythonLogging(server, script_name):
    db_name = "EDW"
    log_table_name = "PythonAuditLog"
    connection_string = (
        "DRIVER={};SERVER={};DATABASE={};Trusted_Connection=yes;Encrypt=yes".format(
            "ODBC Driver 17 for SQL Server", server, db_name
        )
    )

    log_conn = pyodbc.connect(connection_string)
    log_cursor = log_conn.cursor()
    logdb = LogDBHandler(log_conn, log_cursor, log_table_name)

    logging.getLogger("").addHandler(logdb)
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(script_name)

    return log
