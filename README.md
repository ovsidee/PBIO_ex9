# PBIO_ex9

## Infromation about the task:

 - S-number: s31719
 - Name: Vitalii Korytnyi

# Description:
- So i did random **DNA sequence generator** with FASTA formatting,
- it prompts from the user the name and inserts it in random place while not affecting the biological math or line-break formatting
- i implemented those features:
1) **_Batch Mode_** to generate multiple sequences in one run
2) **_Configurable distribution_** to manually weight the probability of A/C/G/T
3) **_Motif Searching_** to find the exact positions of specific strings (when it finds it prints something like:
   ```
   Motif 'ATG' found at positions: [65, 68, 84, 87, 121, 172]
   Motif 'ATG' found at positions: [89]
   Motif 'ATG' not found.
   ```
6) **_In Silico Transcription_**, which automatically generates and saves a corresponding mRNA record (it swaps from T to U for every DNA created)

## also you can find Test1.fasta, Test2.fasta, Test3.fasta that were generated during program testing
