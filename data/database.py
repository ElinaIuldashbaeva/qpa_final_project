from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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

if __name__ == '__main__':
    Base.metadata.create_all(engine)

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

    ala = AminoAcids(aminoacid='A')
    gly = AminoAcids(aminoacid='G')
    met = AminoAcids(aminoacid='M')
    ser = AminoAcids(aminoacid='S')
    cys = AminoAcids(aminoacid='C')
    his = AminoAcids(aminoacid='H')
    asn = AminoAcids(aminoacid='N')
    thr = AminoAcids(aminoacid='T')
    asp = AminoAcids(aminoacid='D')
    ile = AminoAcids(aminoacid='I')
    pro = AminoAcids(aminoacid='P')
    val = AminoAcids(aminoacid='V')
    glu = AminoAcids(aminoacid='E')
    lys = AminoAcids(aminoacid='K')
    gln = AminoAcids(aminoacid='Q')
    trp = AminoAcids(aminoacid='W')
    phe = AminoAcids(aminoacid='F')
    leu = AminoAcids(aminoacid='L')
    arg = AminoAcids(aminoacid='R')
    tyr = AminoAcids(aminoacid='Y')
    stop = AminoAcids(aminoacid='.')

    uuu = Triplets(codon='UUU', aminoacid=phe)
    uuc = Triplets(codon='UUC', aminoacid=phe)
    uua = Triplets(codon='UUA', aminoacid=leu)
    uug = Triplets(codon='UUG', aminoacid=leu)
    ucu = Triplets(codon='UCU', aminoacid=ser)
    ucc = Triplets(codon='UCC', aminoacid=ser)
    uca = Triplets(codon='UCA', aminoacid=ser)
    ucg = Triplets(codon='UCG', aminoacid=ser)
    uau = Triplets(codon='UAU', aminoacid=tyr)
    uac = Triplets(codon='UAC', aminoacid=tyr)
    uaa = Triplets(codon='UAA', aminoacid=stop)
    uag = Triplets(codon='UAG', aminoacid=stop)
    ugu = Triplets(codon='UGU', aminoacid=cys)
    ugc = Triplets(codon='UGC', aminoacid=cys)
    uga = Triplets(codon='UGA', aminoacid=stop)
    ugg = Triplets(codon='UGG', aminoacid=trp)
    cuu = Triplets(codon='CUU', aminoacid=leu)
    cuc = Triplets(codon='CUC', aminoacid=leu)
    cua = Triplets(codon='CUA', aminoacid=leu)
    cug = Triplets(codon='CUG', aminoacid=leu)
    ccu = Triplets(codon='CCU', aminoacid=pro)
    ccc = Triplets(codon='CCC', aminoacid=pro)
    cca = Triplets(codon='CCA', aminoacid=pro)
    ccg = Triplets(codon='CCG', aminoacid=pro)
    cau = Triplets(codon='CAU', aminoacid=his)
    cac = Triplets(codon='CAC', aminoacid=his)
    caa = Triplets(codon='CAA', aminoacid=gln)
    cag = Triplets(codon='CAG', aminoacid=gln)
    cgu = Triplets(codon='CGU', aminoacid=arg)
    cgc = Triplets(codon='CGC', aminoacid=arg)
    cga = Triplets(codon='CGA', aminoacid=arg)
    cgg = Triplets(codon='CGG', aminoacid=arg)
    auu = Triplets(codon='AUU', aminoacid=ile)
    auc = Triplets(codon='AUC', aminoacid=ile)
    aua = Triplets(codon='AUA', aminoacid=ile)
    aug = Triplets(codon='AUG', aminoacid=met)
    acu = Triplets(codon='ACU', aminoacid=thr)
    acc = Triplets(codon='ACC', aminoacid=thr)
    aca = Triplets(codon='ACA', aminoacid=thr)
    acg = Triplets(codon='ACG', aminoacid=thr)
    aau = Triplets(codon='AAU', aminoacid=asn)
    aac = Triplets(codon='AAC', aminoacid=asn)
    aaa = Triplets(codon='AAA', aminoacid=lys)
    aag = Triplets(codon='AAG', aminoacid=lys)
    agu = Triplets(codon='AGU', aminoacid=ser)
    agc = Triplets(codon='AGC', aminoacid=ser)
    aga = Triplets(codon='AGA', aminoacid=arg)
    agg = Triplets(codon='AGG', aminoacid=arg)
    guu = Triplets(codon='GUU', aminoacid=val)
    guc = Triplets(codon='GUC', aminoacid=val)
    gua = Triplets(codon='GUA', aminoacid=val)
    gug = Triplets(codon='GUG', aminoacid=val)
    gcu = Triplets(codon='GCU', aminoacid=ala)
    gcc = Triplets(codon='GCC', aminoacid=ala)
    gca = Triplets(codon='GCA', aminoacid=ala)
    gcg = Triplets(codon='GCG', aminoacid=ala)
    gau = Triplets(codon='GAU', aminoacid=asp)
    gac = Triplets(codon='GAC', aminoacid=asp)
    gaa = Triplets(codon='GAA', aminoacid=glu)
    gag = Triplets(codon='GAG', aminoacid=glu)
    ggu = Triplets(codon='GGU', aminoacid=gly)
    ggc = Triplets(codon='GGC', aminoacid=gly)
    gga = Triplets(codon='GGA', aminoacid=gly)
    ggg = Triplets(codon='GGG', aminoacid=gly)

    codons = [
        uuu, uuc, uua, uug, ucu, ucc, uca, ucg, uau, uac, uaa, uag, ugu, ugc, uga, ugg,
        cuu, cuc, cua, cug, ccu, ccc, cca, ccg, cau, cac, caa, cag, cgu, cgc, cga, cgg,
        auu, auc, aua, aug, acu, acc, aca, acg, aau, aac, aaa, aag, agu, agc, aga, agg,
        guu, guc, gua, gug, gcu, gcc, gca, gcg, gau, gac, gaa, gag, ggu, ggc, gga, ggg
    ]

    with Session() as session:
        session.add_all(codons)
        session.commit()
