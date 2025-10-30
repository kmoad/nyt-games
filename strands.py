from collections import defaultdict
import itertools
from pathlib import Path
from prefixtree import PrefixTree
import requests
import datetime

class StrandsPuzzle():

    def __init__(self, grid: list[list[str]]):
        self._grid = grid
        self._dim = [len(self._grid), len(self._grid[0])]

    @classmethod
    def from_file(cls, fp: Path):
        grid = []
        for line in fp.open():
            grid.append([_ for _ in line.strip()])
        return cls(grid)
    
    def _get_neighbor_coordinates(self, coord: tuple[int,int]) -> list[tuple[int,int]]:
        """
        Get coordinates of grid positions around the current one (adjacent or diagonal)
        """
        i, j = coord
        neighbors = []
        # Iterate the 9 positions near provided coordinates
        for ni, nj in itertools.product((i-1, i, i+1), (j-1,j,j+1)):
            # Drop the provided position
            if ni == i and nj == j:
                continue
            # Drop out-of-bounds
            if ni < 0 or ni >= self._dim[0]:
                continue
            if nj < 0 or nj >= self._dim[1]:
                continue
            neighbors.append((ni,nj))
        return neighbors    

    def __getitem__(self, coord: tuple[int,int]) -> str:
        """
        Get the letter at a coordinate
        """
        return self._grid[coord[0]][coord[1]]

    def _find_words(self, coords: list[tuple[int,int]], prev_pt: PrefixTree) -> tuple[str,list[tuple[int,int]]]:
        """
        Find words from a position chain.

        Arguments:
            coords: The coordinates of the path taken to get to this position,
                ending with the coordinate of the current position. This is to 
                avoid using positions more than once in a word.
            prev_pt: The node in the prefix tree up to but not including the
                current letter. Thus, prev_pt.prefix is the word so far.
        """
        cur_coord = coords[-1]
        cur_let = self[cur_coord]
        words = []
        # Proceed if adding cur_let will continue to a valid word
        if cur_let in prev_pt:
            cur_pt = prev_pt[cur_let]
            # Check for complete word
            if cur_pt.is_word:
                words.append((cur_pt.prefix, coords))
            # Proceed to neighboring positions
            for neighbor_coord in self._get_neighbor_coordinates(cur_coord):
                # Can only use a position once
                if neighbor_coord in coords:
                    continue
                # Recur into next position
                words += self._find_words(coords+[neighbor_coord], cur_pt)
        return words
    
    def solve(self, pt: PrefixTree) -> dict[str:list[list[tuple[int,int]]]]:
        """
        Find words in PrefixTree that are creatable in this puzzle
        """
        solutions = defaultdict(list)
        # Iterate every location
        range_x = range(0, self._dim[0])
        range_y = range(0, self._dim[1])
        for starting_coord in itertools.product(range_x, range_y):
            for word, chain in puzzle._find_words([starting_coord], pt):
                solutions[word].append(chain)
        return solutions

def save_todays_puzzle(out_path: Path):
    today = datetime.datetime.today()
    date_str = today.strftime(r'%Y-%m-%d')
    print(date_str)
    url = f'https://www.nytimes.com/svc/strands/v2/{date_str}.json'
    r = requests.get(url)
    r.raise_for_status()
    with out_path.open('w') as wf:
        for row in r.json()['startingBoard']:
            wf.write(row+'\n')

if __name__ == '__main__':
    from argparse import ArgumentParser

    word_list_dir = Path('lists')

    parser = ArgumentParser(
        description = 'Solve NYT Strands puzzles'
    )
    parser.add_argument('--puzzle',
        type = Path,
        help = 'Path to puzzle file',
    )
    parser.add_argument('--save-today',
        type = Path,
        help = 'Fetch today\'s puzzle and save to file',    
    )
    parser.add_argument('--words',
        type = Path,
        required = False,
        default = word_list_dir/'easy.txt',
        help = 'Path to words file',
    )
    parser.add_argument('--show',
        type = int,
        default = 10,
        help = 'Number of words to show',
    )
    args = parser.parse_args()

    if args.save_today:
        save_todays_puzzle(args.save_today)
        exit()

    all_words = [l.strip().upper() for l in args.words.open()]
    # Words must have more than 3 letters
    words = list(filter(lambda _: len(_) > 3, all_words))
    pt = PrefixTree(words)

    puzzle = StrandsPuzzle.from_file(args.puzzle)
    
    solutions = puzzle.solve(pt)

    solution_words = list(solutions.keys())
    solution_words.sort(key=lambda _: len(_), reverse=True)
    for word in solution_words[:args.show]:
        print(word, solutions[word][0][0])
