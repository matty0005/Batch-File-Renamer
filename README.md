# Batch-File-Renamer
Rename a whole folder, even recursively. Designed for series.

Can rename all files in a folder, and even sub folders.

Note, for this to work, each file needs to have a number (eg, episode number).

# Usage
`python3 main.py -dir/-d directory [--recusive/-r]`

Note: the directory needs to be the full path to the folder. 
If you wish to have the renamer search for files within a sub folder, include the `-r` or `--recursive` argument.

The renamer will prompt you with a sample file name, if it is incorrect, you can manually rename it.
