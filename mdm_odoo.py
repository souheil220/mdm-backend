from fastapi import FastAPI
from xmlrpc import client as xmlrpclib
from fastapi.middleware.cors import CORSMiddleware
from sql import ConnexionOdoo
from datetime import datetime

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/",
]

url = "http://10.20.10.101:8069"
dbo = "hasnaoui"
username = "admin"
password = "4g$1040"

models = xmlrpclib.ServerProxy("{}/xmlrpc/2/object".format(url))
common = xmlrpclib.ServerProxy("{}/xmlrpc/2/common".format(url))
uid = common.authenticate(dbo, username, password, {})


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inventory = {}


def productExist(code):
    product = models.execute_kw(
        dbo,
        uid,
        password,
        "product.product",
        "search_read",
        [[["default_code", "=", code]]],
        {"fields": ["product_tmpl_id"], "limit": 1},
    )
    print(product)
    if len(product) > 0:
        product_template = models.execute_kw(
            dbo,
            uid,
            password,
            "product.template",
            "search_read",
            [[["id", "=", product[0]["product_tmpl_id"][0]]]],
            {"fields": ["uom_id", "list_price", ""], "limit": 1},
        )

        print("product_template ", product_template)
        return [True, product[0], product_template]
    else:
        return [False, 0]


def addSaleOrder(
    pricelist_id,
    partner_id,
    partner_shipping_id,
    warehouseId,
    addressFacturationID,
    addressDeLivraisonID,
    compteAnalytique,
):
    ir_sequence = models.execute_kw(
        dbo,
        uid,
        password,
        "ir.sequence",
        "next_by_id",
        [7473],
        {},
    )

    product = models.execute_kw(
        dbo,
        uid,
        password,
        "sale.order",
        "create",
        [
            {
                "partner_id": partner_id,
                "company_id": 14,
                "sate": "draft",
                "pricelist_id": pricelist_id,
                "partner_invoice_id": partner_id,
                "create_uid": 772,
                "name": ir_sequence,
                "partner_shipping_id": partner_shipping_id,
                "order_policy": "picking",
                "picking_policy": "direct",
                "warehouse_id": warehouseId,
                "partner_invoice_id": addressFacturationID,
                "partner_shipping_id": addressDeLivraisonID,
                "project_id": compteAnalytique,
            }
        ],
    )

    return product


def addSaleOrderLine(
    item, commande_id, product_name, product_temp_info, addressFacturationID
):
    models.execute_kw(
        dbo,
        uid,
        password,
        "sale.order.line",
        "create",
        [
            {
                "product_uos_qty": int(item["quantite"]),
                "product_uom": product_temp_info[0]["uom_id"][0],
                "price_unit": 1000,
                "product_uom_qty": int(item["quantite"]),
                "name": product_name,
                "delay": 0,
                "state": "draft",
                "order_id": commande_id,
                "order_partner_id": addressFacturationID,
            }
        ],
    )


@app.get("/")
def home():
    return "test"


@app.post("/commande-ouvrant")
def ouvrant(items: list):
    print(items)
    product_names = []
    product_temp_info = []
    for item in items:
        exist = productExist(item["code"])
        if exist[0]:
            product_names.append(exist[1]["product_tmpl_id"][1])
            product_temp_info.append(exist[2])
        if not exist[0]:
            error = {
                "title": "Error",
                "message": "Le produit {} n'exist pas veuillez le creer".format(
                    item["code"]
                ),
            }
            return {"error": error}
    commande_id = addSaleOrder(
        1,
        items[0]["client"],
        items[0]["client"],
        items[0]["warehouse"],
        items[0]["addressFacturation"],
        items[0]["addressDeLivraison"],
        items[0]["compteAnalytique"],
    )
    i = 0
    for item in items:
        addSaleOrderLine(
            item,
            commande_id,
            product_names[i],
            product_temp_info[i],
            items[0]["addressFacturation"],
        )
        i += 1
    return {"success": 201}


@app.get("/get-warehouse")
def getCompany(name: str):
    warhouse_name = ConnexionOdoo.getWarehouses(ConnexionOdoo, name)
    final_warehouses_names = []
    for warehouse in warhouse_name:
        final_warehouses_names.append({"label": warehouse[1], "value": warehouse[0]})
    return final_warehouses_names


@app.get("/get-address")
def getAddress(address: str, type: str, parent_id: int):
    warhouse_name = ConnexionOdoo.getAddressFacturationOULivraison(
        ConnexionOdoo, address, parent_id, type
    )
    final_warehouses_names = []
    for warehouse in warhouse_name:
        final_warehouses_names.append({"label": warehouse[1], "value": warehouse[0]})
    return final_warehouses_names


@app.get("/get-companny")
def getCompany(name: str):
    company_name = ConnexionOdoo.getCompanies(ConnexionOdoo, name)
    final_company_names = []
    for company in company_name:
        final_company_names.append({"label": company[1], "value": company[0]})
    print(final_company_names)
    return final_company_names


@app.get("/get-compteAnalytique")
def getCompany(contratAnalytique: str):
    compte_analytiques = ConnexionOdoo.getCompteAnalytique(
        ConnexionOdoo, contratAnalytique
    )
    final_comptes_analytiques = []
    for compte_analytique in compte_analytiques:
        final_comptes_analytiques.append(
            {"label": compte_analytique[1], "value": compte_analytique[0]}
        )
    print(final_comptes_analytiques)
    return final_comptes_analytiques
