# S-number: s31719
# Name: Vitalii Korytnyi
# Date: 2026-05-02 (2 May)
# Description:
# So i did random DNA sequence generator with FASTA formatting,
# it silently inserts my name: vitalii korytnyi into the sequence without affecting the biological math or line-break formatting
# i implemented those features:
# 1) Batch Mode to generate multiple sequences in one run
# 2) Configurable distribution to manually weight the probability of A/C/G/T
# 3) Motif Searching to find the exact positions of specific strings (when it finds it prints something like: "Motif 'ATG' found at positions: [65, 68, 84, 87, 121, 172]" \\ Motif 'ATG' found at positions: [89] \\ Motif 'ATG' not found.
# 4) In Silico Transcription, which automatically generates and saves a corresponding mRNA record (it swaps from T to U for every DNA created)
# also you can find Test1.fasta, Test2.fasta, Test3.fasta that were generated during program testing

import random


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """
    gets an integer from the user in a range, in case of an error, repeats the question
    """
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")


def generate_sequence(length: int, distribution: dict = None) -> str:
    """
    returns a random DNA sequence of the specified length, if a distribution dictionary is provided, nucleotides are weighted accordingly
    """
    nucleotides = ['A', 'C', 'G', 'T']
    if distribution:
        weights = [distribution['A'], distribution['C'], distribution['G'], distribution['T']]
        seq_list = random.choices(nucleotides, weights=weights, k=length)
    else:
        seq_list = random.choices(nucleotides, k=length)
    return "".join(seq_list)


def calculate_stats(sequence: str) -> dict:
    """
    returns a dictionary of sequence statistics. keys: "A", "C", "G", "T" (float values, %), "GC" (float value, %)
    """
    pure_seq = "".join(c for c in sequence if c in "ACGT")
    length = len(pure_seq)

    if length == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "GC_content": 0.0}

    counts = {n: pure_seq.count(n) for n in "ACGT"}
    stats = {n: (counts[n] / length) * 100 for n in "ACGT"}
    stats["GC_content"] = ((counts["G"] + counts["C"]) / length) * 100

    return stats


def insert_name(sequence: str, name: str) -> str:
    """
    inserts a name at a random position in the sequence, name written in lowercase letters (with no spaces)
    """
    if not sequence:
        return name.lower()

    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name.lower() + sequence[pos:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """
    returns a formatted FASTA record as a string
    """
    header = f">{seq_id}"
    if description:
        header += f" {description}"

    lines = [header]
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    return "\n".join(lines)


# --- additional Features (task 5) ---
def feature_get_batch_count() -> int:
    """feature no. 1: Batch Mode. Gets the number of sequences to generate"""
    while True:
        ans = input("Do you want to generate multiple sequences (Batch mode)? (y/n): ").strip().lower()
        if ans == 'y':
            return validate_positive_int("Enter number of sequences to generate: ", 1, 10_000)
        elif ans == 'n':
            return 1


def feature_get_distribution() -> dict | None:
    """feature no. 2: Configurable Nucleotide Distribution"""
    while True:
        ans = input("Do you want to configure nucleotide distribution? (y/n): ").strip().lower()
        if ans == 'y':
            try:
                a = float(input("Enter % for A: "))
                c = float(input("Enter % for C: "))
                g = float(input("Enter % for G: "))
                t = float(input("Enter % for T: "))
                if abs((a + c + g + t) - 100.0) < 0.001:
                    return {'A': a, 'C': c, 'G': g, 'T': t}
                else:
                    print("Error: The sum of percentages must equal 100. Try again.")
            except ValueError:
                print("Error: Please enter valid numeric values.")
        elif ans == 'n':
            return None


def feature_search_motif(sequence: str, motif: str) -> list[int]:
    """feature no. 3: Searching for Motifs (1-indexed)"""
    if not motif:
        return []
    motif = motif.upper()
    positions = []
    start = 0
    while True:
        idx = sequence.find(motif, start)
        if idx == -1:
            break
        positions.append(idx + 1)
        start = idx + 1
    return positions


def feature_transcribe_to_mrna(sequence: str) -> str:
    """feature no. 4: In silico transcription (T -> U)"""
    return sequence.replace('T', 'U')


def main():
    length = validate_positive_int("Enter sequence length: ")

    while True:
        seq_id = input("Enter sequence ID: ").strip()
        if ' ' in seq_id or not seq_id:
            print("Error: ID cannot contain whitespace or be empty.")
        else:
            break

    description = input("Enter a description of the sequence: ").strip()

    name = "VitaliiKorytnyi"

    batch_count = feature_get_batch_count()
    distribution = feature_get_distribution()
    motif = input("Enter a motif to search for (e.g., ATG) or leave blank to skip: ").strip().upper()

    filename = f"{seq_id}.fasta"

    # clear previous runs on the same file (if any)
    with open(filename, 'w') as f:
        pass

    # main loop
    for i in range(1, batch_count + 1):
        current_id = f"{seq_id}_{i:03d}" if batch_count > 1 else seq_id

        # core generation of sequnce
        raw_sequence = generate_sequence(length, distribution)
        stats = calculate_stats(raw_sequence)
        seq_with_name = insert_name(raw_sequence, name)

        # formatting to fasta
        fasta_record = format_fasta(current_id, description, seq_with_name)

        # feature no. 4 processing
        mrna_sequence = feature_transcribe_to_mrna(raw_sequence)
        mrna_record = format_fasta(f"{current_id}_mRNA", f"{description} (mRNA)", mrna_sequence)

        # file saving
        with open(filename, 'a') as f:
            f.write(fasta_record + "\n")
            f.write(mrna_record + "\n")

        # printing logic
        if batch_count == 1:
            print(f"\nSequence saved to file: {filename}\n")
            print(f"Sequence statistics (n={length}):")
            print(f"A: {stats['A']:.2f}%")
            print(f"C: {stats['C']:.2f}%")
            print(f"G: {stats['G']:.2f}%")
            print(f"T: {stats['T']:.2f}%")
            print(f"GC-content: {stats['GC_content']:.2f}%")
        else:
            print(f"Sequence {current_id} generated and saved.")

        # feature no. 3 output
        if motif:
            found_positions = feature_search_motif(raw_sequence, motif)
            if found_positions:
                print(f"Motif '{motif}' found at positions: {found_positions}")
            else:
                print(f"Motif '{motif}' not found.")

    if batch_count > 1:
        print(f"\nAll {batch_count} sequences and their mRNA transcripts saved to file: {filename}")


if __name__ == "__main__":
    main()