# Sea Shanty Generator
AI-generated sea shanties... yarrr

## TODOs
- [x] Obtain the initial dataset from http://shanty.rendance.org
- [ ] Augment dataset (switch up pronouns, names, places, etc. using NER and dictionary/MLM)
- [x] Train GPT-2 model
- [ ] Deploy model to huggingface model hub
- [ ] ???   
- [ ] Profit

## Instructions
1. Create and activate a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
2. (Optional) Install torch for CPU if you don't have CUDA: `pip3 install torch --index-url https://download.pytorch.org/whl/cpu`
3. Install dependencies: `pip install -r requirements.txt`
4. Run `python3 collect_dataset.py output/raw_dataset.json` to download the dataset
5. Train the model using `time python3 train.py output/raw_dataset.json output/model`
6. Try the model using `python3 generate_shanty.py output/model`
