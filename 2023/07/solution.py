import argparse
import logging
from typing import List, Dict
from dataclasses import dataclass, field
from functools import total_ordering


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Card:
    label: str
    part: int

    def __str__(self):
        return self.label

    def value(self) -> int:
        scores = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 11 if self.part == 1 else 1,
            "T": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2,
        }
        return scores[self.label]


def two_unique(hand: str, unique: str, wildcard: bool) -> int:
    if hand.count(unique[0]) == 4 or hand.count(unique[1]) == 4:
        if wildcard and (hand.count("J") == 1 or hand.count("J") == 4):
            # If Four of a Kind and the fifth is a wildcard,
            # or vice-versa, best result is `Five of a Kind`
            return 7
        # Four of a Kind
        return 6
    if (hand.count(unique[0]) == 2 and hand.count(unique[1]) == 3) or (
        hand.count(unique[1]) == 2 and hand.count(unique[0]) == 3
    ):
        if wildcard:
            # If Full House and either set are a wildcard,
            # best result is `Five of a Kind`
            return 7
        # Full House
        return 5


def three_unique(hand: str, unique: str, wildcard: bool) -> int:
    if any(
        [
            hand.count(unique[0]) == 3,
            hand.count(unique[1]) == 3,
            hand.count(unique[2]) == 3,
        ]
    ):
        if wildcard:
            # If Three of a Kind and wildcard,
            # the best result is `Four of a Kind`
            return 6
        # Three of a Kind
        return 4
    else:
        if wildcard:
            if hand.count("J") == 1:
                # If Two Pair and one wildcard,
                # the best result is `Full House`
                return 5
            else:
                # If Two Pair and wildcard,
                # the best result is `Four of a Kind`
                return 6
        # Two Pair
        return 3


@total_ordering
@dataclass
class Hand:
    cards: List[Card]
    bid: int
    type: int = 0
    rank: int = 0

    def __str__(self) -> str:
        return "".join([c.label for c in self.cards])

    def hand_type(self, part=1) -> int:
        hand = str(self)
        wildcard = ("J" in hand) and (part == 2)
        unique = "".join(set(hand))
        logging.debug(f"Unique: {unique}, Wildcard: {wildcard}")
        if len(unique) == 1:
            # Five of a Kind
            return 7
        if len(unique) == 2:
            return two_unique(hand, unique, wildcard)
        if len(unique) == 3:
            return three_unique(hand, unique, wildcard)
        if len(unique) == 4:
            if wildcard:
                # If one pair and a wildcard, the best result
                # is `Three of a Kind`. The other possibility is
                # `Two Pair`, but that's a lower value.
                return 4
            # One pair
            return 2
        if len(unique) == 5:
            if wildcard:
                # If all are unique and a wildcard,
                # the best result is `One Pair`
                return 2
            return 1
        return 0

    def __lt__(self, other):
        for i in range(5):
            logging.debug(f"Comparing {self.cards[i]} to {other.cards[i]}")
            if self.cards[i].value() == other.cards[i].value():
                continue
            if self.cards[i].value() < other.cards[i].value():
                logging.debug(f"{str(self)} is less than {str(other)}")
                return True
            if self.cards[i].value() > other.cards[i].value():
                logging.debug(f"{str(self)} is greater than {str(other)}")
                return False

    def __eq__(self, other):
        eq = str(self) == str(other)
        logging.debug(f"{str(self)} is {'not ' if eq else ''}equal to {str(other)}")
        return eq


@dataclass
class Game:
    hands: Dict[int, List[Hand]] = field(default_factory=dict)

    def sort(self):
        for t, hands in self.hands.items():
            self.hands[t] = sorted(hands)

    def score(self) -> int:
        rank = 1
        score = 0
        for i in range(8):
            for hand in self.hands.get(i, []):
                total = rank * hand.bid
                score += total
                logging.debug(
                    f"Hand: {str(hand)} ({hand.type}), Rank: {rank}, "
                    f"Bid: {hand.bid}, Total: {total}, Current score: {score}"
                )
                rank += 1

        return score


def load_data(part) -> Game:
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    game = Game()
    for l in inf:
        cards, bid = l.split(" ")
        h = Hand([Card(c, part) for c in cards], int(bid))
        h.type = h.hand_type(part)
        logging.debug(f"{h}, {h.type}")
        if game.hands.get(h.type) is None:
            game.hands[h.type] = []
        game.hands[h.type].append(h)

    return game


def main(part):
    game: Game = load_data(part)
    logging.debug(f"{game}")
    game.sort()
    logging.debug(f"{game}")
    score = game.score()
    logging.info(f"Part {'One' if part == 1 else 'Two'} Answer: {score}")


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
