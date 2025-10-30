# Solve NYT Games

## [Wordle](https://www.nytimes.com/games/wordle/index.html)

```
usage: wordle.py [-h] [-i INCLUDE] [-e EXCLUDE] [-f FIXED] [-a]

options:
  -h, --help            show this help message and exit
  -i INCLUDE, --include INCLUDE
                        Letters to include, and positions they are not in.
                        Format A24,B0
  -e EXCLUDE, --exclude EXCLUDE
                        letters to exclude
  -f FIXED, --fixed FIXED
                        letters with fixed positions. Must be 5 letters long.
                        Use _ for unknown letters
  -a, --all             Print all suggested words, not just first 10
```

## [Letter Boxed](https://www.nytimes.com/puzzles/letter-boxed)

```
usage: letter-boxed.py [-h] [-l MAX_LENGTH] [--min-word-length MIN_WORD_LENGTH] [--max-word-length MAX_WORD_LENGTH] [-w WORDS_FP] [--box-words]
                       letters

positional arguments:
  letters               Format: ABC-DEF-GHI-JKL

options:
  -h, --help            show this help message and exit
  -l, --length MAX_LENGTH
                        Max solution length. Default: 2
  --min-word-length MIN_WORD_LENGTH
                        Minimum word length
  --max-word-length MAX_WORD_LENGTH
                        Minimum word length
  -w, --words WORDS_FP  File containing words. Default: words-easy.txt
  --box-words           Output just the words that fit the box
```

## [Strands](https://www.nytimes.com/games/strands)

```
usage: strands.py [-h] [--puzzle PUZZLE] [--save-today SAVE_TODAY] [--words WORDS] [--show SHOW]

Solve NYT Strands puzzles

options:
  -h, --help            show this help message and exit
  --puzzle PUZZLE       Path to puzzle file
  --save-today SAVE_TODAY
                        Fetch today's puzzle and save to file
  --words WORDS         Path to words file
  --show SHOW           Number of words to show
```

See `ex-strands-puzzle.txt` for formatting. Use upper-case to show letters that
haven't been used yet and lower-case for letters that have been used.

## [Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee)

```
usage: spelling-bee.py [-h] [--words WORDS] [--show SHOW]
                       center periphery

positional arguments:
  center
  periphery

options:
  -h, --help     show this help message and exit
  --words WORDS  File containing words
  --show SHOW    Number of valid words to show
```