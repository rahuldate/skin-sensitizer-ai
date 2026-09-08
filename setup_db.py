import sqlite3

conn = sqlite3.connect("chem_index.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS chemicals (
    cas TEXT PRIMARY KEY,
    name TEXT,
    smiles TEXT,
    cid INTEGER
)
""")

# Pre-seed comprehensive benchmark dataset (sensitizers, non-sensitizers, acids, metals)
data = [
    ("65-85-0", "Benzoic acid", "C1=CC=C(C=C1)C(=O)O", 243),
    ("69-72-7", "Salicylic acid", "C1=CC=C(C(=C1)C(=O)O)O", 338),
    ("104-55-2", "Cinnamaldehyde", "C1=CC=C(C=C1)C=CC=O", 637511),
    ("99-76-3", "Methylparaben", "COC(=O)C1=CC=C(C=C1)O", 7456),
    ("62-53-3", "Aniline", "NC1=CC=CC=C1", 6115),
    ("79-06-1", "Acrylamide", "C=CC(=O)N", 6579),
    ("79-10-7", "Acrylic acid", "C=CC(=O)O", 6581),
    ("111-44-4", "Bis(2-chloroethyl) ether", "ClCCOCCCl", 8107),
    ("50-00-0", "Formaldehyde", "C=O", 712),
    ("106-99-0", "1,3-Butadiene", "C=CC=C", 7845),
    ("78-70-6", "Linalool", "CC(=CCCC(C)(C=C)O)C", 6549),
    ("97-53-0", "Eugenol", "COC1=C(C=CC(=C1)CC=C)O", 3314),
    ("107-02-8", "Acrolein", "C=CC=O", 7847),
    ("101-68-8", "4,4'-MDI", "C1=CC(=CC=C1CC2=CC=C(C=C2)N=C=O)N=C=O", 7570),
    ("7440-02-0", "Nickel", "[Ni]", 935),
    ("7440-48-4", "Cobalt", "[Co]", 104727),
    ("7440-47-3", "Chromium", "[Cr]", 23976),
    ("7778-50-9", "Potassium dichromate", "[K+].[K+].[O-][Cr](=O)(=O)O[Cr](=O)(=O)[O-]", 24502),
    ("107-13-1", "Acrylonitrile", "C=CC#N", 7855),
    ("80-62-6", "Methyl methacrylate", "CC(=C)C(=O)OC", 6658),
    ("100-42-5", "Styrene", "C=CC1=CC=CC=C1", 7501),
    ("108-95-2", "Phenol", "C1=CC=C(C=C1)O", 996),
    ("123-31-9", "Hydroquinone", "OC1=CC=C(O)C=C1", 285),
    ("106-51-4", "p-Benzoquinone", "O=C1C=CC(=O)C=C1", 4650),
    ("118-58-1", "Benzyl salicylate", "C1=CC=C(C=C1)COC(=O)C2=CC=CC=C2O", 8363),
    ("149-30-4", "2-Mercaptobenzothiazole", "C1=CC=C2C(=C1)NC(=S)S2", 8989),
    ("586-62-9", "Terpinolene", "CC1=CCC(=C(C)C)CC1", 11463),
]

c.executemany("INSERT OR REPLACE INTO chemicals VALUES (?,?,?,?)", data)
conn.commit()
conn.close()
print("Local SQLite database 'chem_index.db' created successfully.")
