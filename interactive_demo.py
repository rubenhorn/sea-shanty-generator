#! /usr/bin/env python3

import sys
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f'Usage: python3 {sys.argv[0]} <input model path>', file=sys.stderr)
        sys.exit(1)

    print('Loading model...', file=sys.stderr, end='', flush=True)
    generator = pipeline('text-generation', model=sys.argv[1])
    print('done', file=sys.stderr)
    while True:
        try:
            prompt = input('> ')
            print(generator(prompt, max_length=100,
                  pad_token_id=generator.tokenizer.eos_token_id)[0]['generated_text'])
        except:
            print()
            sys.exit(0)
