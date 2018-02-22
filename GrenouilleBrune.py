#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pylatex import Document, Section, Subsection, Subsubsection, Command, Figure
from pylatex.utils import NoEscape
import sqlite3
import os
table = """
CREATE TABLE 'Photo' (
'id'	INTEGER ,
'file' TEXT,
'date'	TEXT,
'sexe'	TEXT,
'espece' TEXT,
PRIMARY KEY(id)
);
"""
chem_photos = "photos"
remplir = """
INSERT INTO Photo (file, date, sexe, espece)
VALUES (:file, :date, :sexe, :espece);
"""
select_categorie = """
SELECT DISTINCT date FROM Photo
WHERE sexe = :sexe AND espece = :espece
"""
select_photo = """
SELECT file FROM photo
WHERE sexe = :sexe AND espece = :espece AND date = :date
"""


def creer_donnees():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute(table)
    conn.commit()
    for date in os.listdir(chem_photos):
        chemin1 = os.path.join(chem_photos, date)
        for sexe in os.listdir(chemin1):
            chemin2 = os.path.join(chemin1, sexe)
            for espece in os.listdir(chemin2):
                chemin3 = os.path.join(chemin2, espece)
                for fichier in os.listdir(chemin3):
                    chemin4 = os.path.join(chemin3, fichier)
                    cur.execute(remplir, {
                        'date': date,
                        'espece': espece,
                        'sexe': sexe,
                        'file': chemin4
                    })
    conn.commit()
    return cur
#f = cur.execute("SELECT * FROM Photo")
#d = f.fetchone()
#d[1].encode()


def creer_section(cur, doc):
    for espece in ("agile", "rousse"):
        with doc.create(Section(espece.upper())):
            for sexe in ("male", "femelle"):
                with doc.create(Subsection(sexe.upper())):
                    for date in cur.execute(select_categorie, {
                        'espece': espece,
                        'sexe': sexe
                    }):
                        date = date[0]
                        print(date)
                        with doc.create(Subsubsection(date.encode().upper())):
                            for chemin in cur.execute(select_photo, {
                                'espece': espece,
                                'sexe': sexe,
                                'date': date
                            }):
                                chemin = chemin[0]
                                print(chemin)

                                with doc.create(
                                    Figure(width=NoEscape(r'\linewidth'))
                                ) as frog:
                                    frog.add_image(
                                        chemin,
                                        width=NoEscape(r'0.45\linewidth')
                                        )


if __name__ == '__main__':
    # Basic document
    doc = Document("GrenouilleBrune")

    doc.preamble.append(Command('title', 'Awesome Title'))
    doc.preamble.append(Command('author', 'Lucas Boutarfa'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    cur = creer_donnees()
    creer_section(cur, doc)

    doc.create(Section("une autre section"))
    doc.append("plus de texte")
    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()
