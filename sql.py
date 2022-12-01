import psycopg2


class ConnexionOdoo:
    def connect():
        conn_string = (
            "host=10.20.10.101 dbname=hasnaoui user=odoo password=odoo_hasnaoui_2021"
        )
        print("Connecting to database\n	->%s" % (conn_string))
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        return cursor

    def getCompanies(self, company_name):
        cursor = self.connect()
        cursor.execute(
            """SELECT id,name
                from res_company rc 
                where 
                rc.name LIKE '%"""
            + company_name.upper()
            + """%' limit 5"""
        )
        records = cursor.fetchall()
        cursor.close()
        return records

    def getWarehouses(self, warehouse_name):
        cursor = self.connect()
        cursor.execute(
            """SELECT id,name
                from stock_warehouse sw 
                where 
                company_id IN (14) AND
                sw.name LIKE '%"""
            + warehouse_name.upper()
            + """%' limit 5"""
        )

        records = cursor.fetchall()
        cursor.close()
        return records
