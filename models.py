from typing import Optional
from pydantic import BaseModel


class Ouvrant(BaseModel):
    code: str
    quantité_commandé: int
    type_de_Porte: str
    modele_de_porte: str
    matière_de_finition: str
    couleur: str
    nombre_de_ventaux: int
    largeur_precadre_intérieur: int
    hauteur_ouvrant: int
    largueur_1er_ouvrant: int
    mécanisation_de_Serrure: str
    serrure: bool
    protecteur: str
    sens_douverture: str
    vitrage: str
    grille_d_airation: str
    quincaillerie: str
    client: str
    code_model: str
    code_protecteur: str
    code_vitrage: str
    code_grille: str
