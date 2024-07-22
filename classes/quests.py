from __future__ import annotations

from enum import Enum


class Quest:
    def __init__(
            self,
            name: str,
            continue_count: int,
            verify_count: int = 0,
            skip: bool = False,
            quiz_answer: str | None = None,
            vote_options: int = 0,
    ):
        self.name = name
        self.layer_url = 'https://app.layer3.xyz/quests/' + name
        self.continue_count = continue_count
        self.verify_count = verify_count
        self.skip = skip
        self.quiz_answer = quiz_answer
        self.vote_options = vote_options


class Quests(Enum):
    # Week 1
    quest_1 = Quest('introduction-to-linea-culture-szn', continue_count=5)
    quest_2 = Quest('linea-lxp', continue_count=5)
    quest_3 = Quest('nft-learn', continue_count=3, quiz_answer='Open MetaMask Portfolio, sign in with MetaMask, and navigate to the')
    quest_4 = Quest('how-to-avoid-nft-scams', continue_count=6, quiz_answer='Verify all links and announcements')
    quest_5 = Quest('what-are-metamask-snaps', continue_count=3, quiz_answer='Share you secret recovery phrase with degens')
    quest_6 = Quest('w1-octomos', continue_count=3, verify_count=2)
    quest_7 = Quest('w1-crazy-show', continue_count=2, verify_count=2)
    quest_8 = Quest('w1-push', 2, verify_count=2)
    quest_9 = Quest('w1-wizards-of-linea', continue_count=1, verify_count=2)
    quest_10 = Quest('w1-efrogs', continue_count=3, verify_count=1, skip=True)
    quest_12 = Quest('w2-satoshi-universe', continue_count=2, verify_count=2)
    quest_13 = Quest('w2-linus', continue_count=1, verify_count=2)
    quest_14 = Quest('w2-yooldo', continue_count=1, verify_count=2)
    quest_15 = Quest('w2-frog-wars', continue_count=2, verify_count=2)
    quest_16 = Quest('w2-acg', continue_count=2, verify_count=2)
    quest_17 = Quest('w2-toad', continue_count=2, verify_count=2)
    quest_18 = Quest('week-2-voting', continue_count=2, verify_count=1, vote_options=6)
    quest_19 = Quest('w3-ascendtheend-1', continue_count=1, verify_count=2)
    quest_20 = Quest('w3-sendingme', continue_count=2, verify_count=2)
    quest_21 = Quest('w3-townstory', continue_count=2, verify_count=2)
    quest_22 = Quest('w3-danielle-zosavac', continue_count=1, verify_count=2)
    quest_23 = Quest('w3-demmortal', continue_count=1, verify_count=2)
    quest_24 = Quest('w3-foxy', continue_count=1, verify_count=2)
    quest_25 = Quest('week-3-voting', continue_count=2, verify_count=1, vote_options=6)
    quest_26 = Quest('w4-coop-records', continue_count=1, verify_count=2)

