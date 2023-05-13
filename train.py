#! /usr/bin/env python3

import datasets
import multiprocessing
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling

CHECKPOINT = 'distilgpt2'
EPOCHS = 20


def create_pretrained_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def create_pretrained_model():
    return AutoModelForCausalLM.from_pretrained(CHECKPOINT)


def load_datasets(filename, train_eval_split=0.9):
    split_at_percent = int(train_eval_split * 100)
    train_dataset, eval_dataset = datasets.load_dataset(
        'json', data_files=filename, split=[f'train[:{split_at_percent}%]', f'train[{split_at_percent}%:]'])
    return train_dataset, eval_dataset


def get_training_args():
    return TrainingArguments(
        'test-trainer',
        optim='adamw_torch',
        num_train_epochs=EPOCHS,
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f'Usage: python3 {sys.argv[0]} <input json file> <generated model path> [<checkpoint>] [<epochs>]', file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 4:
        print(f'No checkpoint specified. Using default model: {CHECKPOINT}')
    else:
        CHECKPOINT = sys.argv[3]

    if len(sys.argv) >= 5:
        EPOCHS = int(sys.argv[4])

    # Load dataset
    tokenizer = create_pretrained_tokenizer()
    tokenizer.pad_token = tokenizer.eos_token
    train_dataset, eval_dataset = load_datasets(sys.argv[1])
    def tokenize(x): return tokenizer(x['text'])
    train_dataset = train_dataset.map(tokenize, remove_columns=['text'])
    eval_dataset = eval_dataset.map(tokenize, remove_columns=['text'])

    # Limit hardward usage by pytorch
    torch.set_num_threads(min(1, multiprocessing.cpu_count() // 2))

    # Train
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False)
    training_args = get_training_args()
    trainer = Trainer(
        create_pretrained_model(),
        training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    trainer.train()

    # Save model
    print(
        f'Finished training. Saving model to {sys.argv[2]}...', file=sys.stderr, end='', flush=True)
    trainer.save_model(sys.argv[2])
    print('done.', file=sys.stderr)
