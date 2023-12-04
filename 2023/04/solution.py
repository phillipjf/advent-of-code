import argparse
import logging


from typing import List, Tuple
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Card:
    number: int
    winning_numbers: List[int]
    numbers: List[int]

    def score(self) -> int:
        score = 0
        for n in self.numbers:
            if n in self.winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score += score
        return score

    def matching_numbers(self) -> int:
        return len([n for n in self.numbers if n in self.winning_numbers])


def winning_cards(cards: List[Card], match_range: Tuple[int, int], score: int) -> int:
    for c in cards[match_range[0]:match_range[1]]:
        match_count = c.matching_numbers()
        ind = c.number
        mr = (ind, ind+match_count)
        cc = cards[mr[0]:mr[1]]
        logging.debug(f"Card: {c.number}, Score: {score}, Match Count: {match_count}; {cc}")
        score += winning_cards(cards, mr, match_count)
    return score


def main(part):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    score = 0
    cards = []
    for c in inf:
        cn, numbers = c.split(': ')
        cn = int(cn.split(' ')[-1])
        winning_numbers, numbers = numbers.split(' | ')
        winning_numbers = [int(n) for n in winning_numbers.split(' ') if n != '']
        numbers = [int(n) for n in numbers.split(' ') if n != '']
        logging.debug(f"Card: {cn}; Winning Numbers: {winning_numbers}, Numbers: {numbers}")
        card = Card(number=cn, winning_numbers=winning_numbers, numbers=numbers)
        cards.append(card)
        score += card.score()

    logging.info(f"Part One Answer: {score}")

    w_cards = winning_cards(cards, (0, len(cards)), len(cards))
    logging.info(f"Part Two Answer: {w_cards}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "part",
        metavar="P",
        type=int,
        choices=[1, 2],
        help="Problem part (1 or 2)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel)
    main(args.part)
