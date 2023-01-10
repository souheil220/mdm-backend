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
                from res_partner rc 
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

    def getAddressFacturationOULivraison(self, adress, parent_id, type):
        cursor = self.connect()
        query = (
            """select id,name 
               from res_partner rp 
             where parent_id = 
             """
            + str(parent_id)
            + """
               and type = '
               """
            + type
            + """' 
               AND rp.name LIKE '%
               """
            + adress.upper()
            + """%' 
               limit 5"""
        )

        cursor.execute(
            """select id,name 
               from res_partner rp 
            
             where type = '"""
            + type
            + """' AND
                rp.name LIKE '%"""
            + adress.upper()
            + """%' limit 5"""
        )

        records = cursor.fetchall()
        cursor.close()
        return records

    def getCompteAnalytique(self, contrat_analytique):
        cursor = self.connect()
        cursor.execute(
            """select id,code  
                from account_analytic_account aaa 
                where aaa.code  LIKE '%"""
            + contrat_analytique.upper()
            + """%' limit 5"""
        )

        records = cursor.fetchall()
        cursor.close()
        return records
