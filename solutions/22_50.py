from itertools import zip_longest
from typing import Generator


AA_CODON = {'Ala': 'GCU GCC GCA'.split(),
            'Leu': 'UUA UUG CUU CUC CUA CUG'.split(),
            'Arg': 'CGU CGC CGA CGG AGA AGG'.split(),
            'Lys': 'AAA AAG'.split(),
            'Asn': 'AAU AAC'.split(),
            'Met': 'AUG'.split(),
            'Asp': 'GAU GAC'.split(),
            'Phe': 'UUU UUC'.split(),
            'Cys': 'UGU UGC'.split(),
            'Pro': 'CCU CCC CCA CCG'.split(),
            'Gln': 'CAA CAG'.split(),
            'Ser': 'UCU UCC UCA UCG AGU AGC'.split(),
            'Glu': 'GAA GAG'.split(),
            'Thr': 'ACU ACC ACA ACG'.split(),
            'Gly': 'GGU GGC GGA GGG'.split(),
            'Trp': 'UGG'.split(),
            'His': 'CAU CAC'.split(),
            'Tyr': 'UAU UAC'.split(),
            'Ile': 'AUU AUC AUA'.split(),
            'Val': 'GUU GUC GUA GUG'.split(),
            'Stop': 'UAG UGA UAA'.split(),}

DNA_RNA = {'T': 'A',
           'A': 'U',
           'C': 'G',
           'G': 'C',}


def transcribe(dna: str) -> str:
    """Transcribes DNA sequence into complementary RNA."""
    transcription_table = str.maketrans(DNA_RNA)
    rna = dna.translate(transcription_table)
    return rna


def to_codons(seq: str) -> Generator[str, None, None]:
    """Iterator that splits sequence into codon strings."""
    for codon in zip_longest(seq[::3], seq[1::3], seq[2::3], fillvalue=''):
        yield ''.join(codon)


def solution(sequence: str) -> tuple[str, str]:
    """Exercise from 22_50

    :Examples:
    >>> solution('TACAGCTCGCTATGAATC')
    ('AUG UCG AGC GAU ACU UAG', 'Met Ser Ser Asp Thr Stop')

    >>> solution('ACGTG')
    ('UGC AC', 'Cys')
    """
    codon_aa = {codon: aa for aa, codons in AA_CODON.items() for codon in codons}
    mrna = transcribe(sequence)
    codons = list(to_codons(mrna))
    primary_sequence = [codon_aa[cdn] for cdn in codons if cdn in codon_aa]
    return ' '.join(codons), ' '.join(primary_sequence)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
