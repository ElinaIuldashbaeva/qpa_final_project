from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import data.database as db

CODON_LENGTH = 3

engine = create_engine("sqlite:///data/genetics.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


def convert_dna_to_rna(dna: str) -> str:
    """ Function that imitates the transcription process """

    rna = ''
    with Session() as session:
        for base in dna:
            query = session.query(db.Dna).join(db.Rna)
            entry = query.filter(db.Dna.dna_base == base).one()
            rna += str(entry.rna_base)
    return rna


def convert_rna_to_protein(rna: str) -> str:
    """ Function that imitates the translation process """

    start, end = 0, CODON_LENGTH
    polypeptide = ''
    with Session() as session:
        while end <= len(rna):
            codon = rna[start:end]
            query = session.query(db.Triplets).join(db.AminoAcids)
            entry = query.filter(db.Triplets.codon == codon).one()
            polypeptide += str(entry.aminoacid)
            start += CODON_LENGTH
            end += CODON_LENGTH
    return polypeptide


assert convert_dna_to_rna('ATTTGGCTACTAACAATCTA') == 'AUUUGGCUACUAACAAUCUA'
assert convert_dna_to_rna('GTTGTAATGGCCTACATTA') == 'GUUGUAAUGGCCUACAUUA'
assert convert_dna_to_rna('CAGGTGGTGTTGTTCAGTT') == 'CAGGUGGUGUUGUUCAGUU'
assert convert_dna_to_rna('GCTAACTAAC') == 'GCUAACUAAC'
assert convert_rna_to_protein('AUUUGGCUACUAACAAUCUA') == 'IWLLTI'
assert convert_rna_to_protein('GUUGUAAUGGCCUACAUUA') == 'VVMAYI'
assert convert_rna_to_protein('CAGGUGGUGUUGUUCAGUU') == 'QVVLFS'
assert convert_rna_to_protein('GCUAACUAAC') == 'AN.'
assert convert_rna_to_protein('GCUAACUAACAUCUUUGGCACUGUU') == 'AN.HLWHC'
