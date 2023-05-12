# Sea Shanty Generator
AI-generated sea shanties... yarrr

## TODOs
- [x] Obtain the initial dataset from http://shanty.rendance.org
- [ ] Augment dataset (switch up pronouns, names, places, etc. using NER and dictionary/MLM)
- [x] Train text generation model
- [ ] Resumable and longer training
- [ ] Deploy model to huggingface model hub
- [ ] ???   
- [ ] Profit

## Instructions
1. Create and activate a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
2. (Optional) Install torch for CPU if you don't have CUDA: `pip3 install torch --index-url https://download.pytorch.org/whl/cpu`
3. Install dependencies: `pip install -r requirements.txt`
4. Run `python3 collect_dataset.py generated/raw_dataset.json` to download the dataset
5. Train the model using `time python3 train.py generated/raw_dataset.json generated/model [<checkpoint>]`
6. Try the model using `python3 generate_shanty.py generated/model`

## Trained model in Google Colab
```bash
#@title Create dataset and trained model
!rm -rf sea-shanty-generator && \
git clone https://github.com/rubenhorn/sea-shanty-generator.git && \
cd sea-shanty-generator && \
pip install -r requirements.txt && \
python3 collect_dataset.py generated/raw_dataset.json && \
time python3 train.py generated/raw_dataset.json generated/model && \
zip -r generated.zip generated && \
python3 -c "from google.colab import files; files.download('generated.zip')"
```
