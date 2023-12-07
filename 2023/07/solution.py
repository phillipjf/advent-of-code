import argparse
import logging
from typing import List, Dict
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Card:
    label: str

    def __str__(self):
        return self.label

    def value(self) -> int:
        scores = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 11,
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


@dataclass
class Hand:
    cards: List[Card]
    bid: int
    rank: int = 0

    def __str__(self) -> str:
        return "".join([c.label for c in self.cards])

    def hand_type(self) -> int:
        hand = str(self)
        unique = "".join(set(hand))
        logging.debug(f"Unique: {unique}")
        if len(unique) == 1:
            # Five of a Kind
            return 7
        if len(unique) == 2:
            if hand.count(unique[0]) == 4 or hand.count(unique[1]) == 4:
                # Four of a Kind
                return 6
            if (hand.count(unique[0]) == 2 and hand.count(unique[1]) == 3) or (
                hand.count(unique[1]) == 2 and hand.count(unique[0]) == 3
            ):
                # Full House
                return 5
        if len(unique) == 3:
            if any(
                [
                    hand.count(unique[0]) == 3,
                    hand.count(unique[1]) == 3,
                    hand.count(unique[2]) == 3,
                ]
            ):
                # Three of a Kind
                return 4
            else:
                # Two Pair
                return 3
        if len(unique) == 4:
            # One pair
            return 2
        if len(unique) == 5:
            return 1
        return 0

    def compare(self, hand) -> int:
        # Returns 1 if `hand`>self
        # Returns -1 if `hand`<self
        for i in range(5):
            if self.cards[i].value() == hand.cards[i].value():
                continue
            if self.cards[i].value() > hand.cards[i].value():
                return -1
            if self.cards[i].value() < hand.cards[i].value():
                return 1
        return 0


@dataclass
class Game:
    hands: Dict[int, List[Hand]] = field(default_factory=dict)

    def sort(self):
        i = 0
        for t, hands in self.hands.items():
            sort_hands = []
            for h in hands:
                if len(sort_hands) == 0:
                    logging.debug(f"Rank: {t}; First hand to sort...")
                    sort_hands.append(h)
                for i, hh in enumerate(sort_hands):
                    if hh.compare(h) == -1:
                        logging.debug(f"Rank: {t}; Hand {h} is less than {hh}")
                        sort_hands.insert(i, h)
                        break
                    if hh.compare(h) == 1:
                        logging.debug(f"Rank: {t}; Hand {h} is greater than {hh}")
                        if i == len(sort_hands) - 1:
                            logging.debug(f"Rank: {t}; Hand {h} is the largest hand")
                            sort_hands.append(h)
                            break
                        else:
                            continue
                logging.debug(f"Rank: {t}; Sort hands looks like: {sort_hands}")
            self.hands[t] = sort_hands

    def score(self) -> int:
        h = []
        score = 0
        for i in range(8):
            hands = self.hands.get(i, [])
            logging.debug(f"Extending with {i} {hands}")
            h.extend(hands)
        logging.debug(f"Order of hands: {h}")
        for i, hand in enumerate(h, 1):
            logging.debug(f"Rank: {i}, Bid: {hand.bid}")
            score += i * hand.bid

        return score


def load_data(part) -> Game:
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    game = Game()
    for l in inf:
        cards, bid = l.split(" ")
        h = Hand([Card(c) for c in cards], int(bid))
        h_type = h.hand_type()
        logging.debug(f"{h}, {h_type}")
        if game.hands.get(h_type) is None:
            game.hands[h_type] = []
        game.hands[h_type].append(h)

    return game


def main(part):
    game: Game = load_data(part)
    logging.debug(f"{game}")
    game.sort()
    logging.debug(f"{game}")
    score = game.score()
    logging.info(f"Part One Answer: {score}")


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
