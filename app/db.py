import psycopg2


class Database():
    def __init__(self, user, psw):
        self.user = user
        self.psw = psw
        self.host = 'dpg-cmcvn5ed3nmc73dfkgkg-a.oregon-postgres.render.com'
        self.port = '5432'
        self.database = 'biblioteca_wlmx'

    def getConnection(self):
        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.psw,
                host=self.host,
                port=self.port,
                database=self.database
            )
            conn.autocommit = True
            return conn
        except Exception as e:
            raise Exception(
                "ERROR FATAL: Error al conectar a la base de datos " + str(e))

    def closeConnection(self, conn):
        conn.close()


database = Database("biblioteca_wlmx_user", "cPvaiR2ZXVbsASFQw7ZLhOU3PW1SXyPO")
