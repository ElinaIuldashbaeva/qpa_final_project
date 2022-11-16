from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import data.database as db
import matplotlib.pyplot as plt
import numpy as np

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
<<<<<<< HEAD


def plot_the_gc_ratio(sequence: str, step=100) -> None:
    """ Function that plots the GC-content graph """

    ratios = []
    start, end = 0, step
    while end <= len(sequence):
        bases_number = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
        for base in sequence[start:end]:
            bases_number[base] += 1
        ratio = ((bases_number['G'] + bases_number['C']) / step) * 100
        ratios.append(ratio)
        start += step
        end += step
    ratios.append(ratios[-1])
    x = np.arange(0, len(sequence), step)
    plt.step(x, ratios, where='post')
    plt.suptitle('GC content distribution')
    plt.ylabel('guanine-cytosine ratio (%)')
    plt.xlabel('DNA bases position')
    plt.savefig('gc_ratio_of_genome.png')

=======
>>>>>>> 8d4203f8b40639e1e2b7d202130f9267558058ed
