from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

CODONS_AMINOACIDS_MAP = {
    'A': ['GCU', 'GCC', 'GCA', 'GCG'],
    'G': ['GGU', 'GGC', 'GGA', 'GGG'],
    'M': ['AUG'],
    'S': ['AGU', 'AGC', 'UCU', 'UCC', 'UCA', 'UCG'],
    'C': ['UGU', 'UGC'],
    'H': ['CAU', 'CAC'],
    'N': ['AAU', 'AAC'],
    'T': ['ACU', 'ACC', 'ACA', 'ACG'],
    'D': ['GAU', 'GAC'],
    'I': ['AUU', 'AUC', 'AUA'],
    'P': ['CCU', 'CCC', 'CCA', 'CCG'],
    'V': ['GUU', 'GUC', 'GUA', 'GUG'],
    'E': ['GAA', 'GAG'],
    'K': ['AAA', 'AAG'],
    'Q': ['CAA', 'CAG'],
    'W': ['UGG'],
    'F': ['UUU', 'UUC'],
    'L': ['CUU', 'CUC', 'CUA', 'CUG', 'UUA', 'UUG'],
    'R': ['AGA', 'AGG', 'CGU', 'CGC', 'CGA', 'CGG'],
    'Y': ['UAU', 'UAC'],
    '.': ['UAA', 'UAG', 'UGA']
}

engine = create_engine("sqlite:///genetics.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Creating tables

class Dna(Base):
    __tablename__ = "dna_bases"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    dna_base = Column(String(3))
    rna_base = relationship("Rna", back_populates="dna_base")
    rna_id = Column(Integer, ForeignKey("rna_bases.id"))

    def __str__(self):
        return f"{self.id}: DNA base - {self.dna_base}, RNA base - {self.rna_base}"


class Rna(Base):
    __tablename__ = "rna_bases"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    rna_base = Column(String(3))
    dna_base = relationship("Dna", back_populates="rna_base")

    def __str__(self):
        return f"{self.rna_base}"


class Triplets(Base):
    __tablename__ = "codons"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    codon = Column(String(5))
    aminoacid = relationship("AminoAcids", back_populates="codon")
    aminoacid_id = Column(Integer, ForeignKey("amino_acids.id"))

    def __str__(self):
        return f"Codon - {self.codon}, amino acid - {self.aminoacid}"


class AminoAcids(Base):
    __tablename__ = "amino_acids"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    aminoacid = Column(String(3))
    codon = relationship("Triplets", back_populates="aminoacid")

    def __str__(self):
        return f"{self.aminoacid}"


# Filling the tables with the data

def fill_rna_dna_tables():

    uracil = Rna(rna_base='U')
    cytosine_rna = Rna(rna_base='C')
    adenosine_rna = Rna(rna_base='A')
    guanine_rna = Rna(rna_base='G')

    thyamine = Dna(dna_base='T', rna_base=uracil)
    cytosine_dna = Dna(dna_base='C', rna_base=cytosine_rna)
    adenosine_dna = Dna(dna_base='A', rna_base=adenosine_rna)
    guanine_dna = Dna(dna_base='G', rna_base=guanine_rna)

    dna_bases = [thyamine, cytosine_dna, adenosine_dna, guanine_dna]

    with Session() as session:
        session.add_all(dna_bases)
        session.commit()


def fill_codons_aminoacids_tables():

    triplets_cls_objects = []
    for amino_ac, codons in CODONS_AMINOACIDS_MAP.items():
        for codon in codons:
            aminoacids_cls_object = AminoAcids(aminoacid=amino_ac)
            triplets_cls_objects.append(Triplets(codon=codon, aminoacid=aminoacids_cls_object))

    with Session() as session:
        session.add_all(triplets_cls_objects)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    fill_rna_dna_tables()
    fill_codons_aminoacids_tables()
