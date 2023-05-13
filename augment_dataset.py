#! /usr/bin/env python3

import json
import random
import re
import sys

random.seed(42)

if len(sys.argv) < 3:
    print(f'Usage: python3 {sys.argv[0]} <input json file> <output json file>')
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

shanties = [x['text'] for x in data]

print(f'Original dataset size: {len(shanties)}')

gender_swapping = [('he', 'she'), ('his', 'her'),  # FIXME does not consider 'him'
                   ('himself', 'herself'),
                   ('boy', 'girl'), ('boys', 'girls'),
                   ('man', 'woman'), ('men', 'women'),
                   ]

antonyms = [('near', 'far'), ('north', 'south'),
            ('east', 'west'), ('old', 'young'),
            ('whiskey', 'rum'),  # Not really antonyms, but close enough
            ('red', 'blue'), ('sailor', 'pirate'),
            ('oh', 'yarr'), ('we', 'they'),
            ('us', 'them'), ('our', 'their'),
            ('ours', 'theirs'), ('early', 'late'),
            ('my', 'your'), ('mine', 'yours'),
            ('day', 'night'), ('morning', 'evening'),
            ('mornin', 'evenin'),
            ('ship', 'boat'), ('ships', 'boats'),
            ('big', 'small'), ('sun', 'moon'),
            ('gold', 'silver'),
            ('golden', 'shiny'), # Not really antonyms, but close enough
            ]

synonyms = [('sailor', 'seaman'), ('but', 'yet'),
            ('whiskey', 'grog'),  # Not really synonyms, but close enough
            ('sail', 'roam'), ('damn', 'darn'),
            ('hey', 'ho'), ('song', 'chantey'),
            ('tough', 'hard'), ('round', 'around'),
            ('skipper', 'captain'),
            ]


def apply_substitution(shanties, substitutions, probability=1, multiplier=1):
    for shanty in list(shanties) * multiplier:
        yield shanty
        substitution_words = [w for ww in substitutions for w in ww]
        found_in_shanty = sum([re.findall(r'\b' + w + r'\b', shanty)
                               for w in substitution_words], [])
        # Avoid duplicating shanties exactly
        if len(found_in_shanty) == 0:
            continue
        for w in substitution_words:
            if random.random() > probability:
                continue
            shanty = re.sub(r'\b' + w + r'\b',
                            f'<{w.upper()}>', shanty, flags=re.IGNORECASE)
            shanty = re.sub(r'\b' + w + '\'',
                            f'<{w.upper()}>\'', shanty, flags=re.IGNORECASE)
        for a, b in substitutions:
            shanty = shanty.replace(f'<{a.upper()}>', b)
            shanty = shanty.replace(f'<{b.upper()}>', a)
        yield shanty


shanties = apply_substitution(shanties, gender_swapping)
shanties = apply_substitution(
    shanties, antonyms, probability=0.5, multiplier=10)
shanties = apply_substitution(
    shanties, synonyms, probability=0.5, multiplier=10)
# Remove any duplicates and shuffle data to avoid biasing the model
shanties = list(set(shanties))
random.shuffle(shanties)

print(f'Augmented dataset size: {len(shanties)}')

with open(sys.argv[2], 'w') as f:
    json.dump([{'text': x} for x in shanties], f, indent=2)
