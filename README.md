# Sea Shanty Generator
AI-generated sea shanties... yarrr

Here's a taste of the lyrical genius you can expect
```
> Who lives in a pineapple under the sea?
Who lives in a pineapple under the sea? 
Weibo, weibo, weibo-o
yarr, weibo, weibo-o
Themes we all come from around the globe;
yarr, a tropical land
that's the life of man
Always was since the world began;
yarr, a tropical land
Full of rocks and thieves and fleas and sand;
yarr, a tropical paradise
Full of rocks and thieves and fleas
```

## TODOs
- [x] Obtain the initial dataset from http://shanty.rendance.org
- [ ] Augment dataset more (names, places, etc. using NER and dictionary/MLM or paraphrase using eugenesiow/bart-paraphrase)
- [x] Train text generation model
- [ ] Fix tendency to overfit
- [ ] Deploy model to huggingface model hub
- [ ] ???   
- [ ] Profit

## Instructions
1. Create and activate a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
2. (Optional) Install torch for CPU if you don't have CUDA: `pip3 install torch --index-url https://download.pytorch.org/whl/cpu`
3. Install dependencies: `pip install -r requirements.txt`
4. Run `python3 collect_dataset.py generated/raw_dataset.json` to download the dataset
5. Augment the dataset with `python3 augment_dataset.py generated/raw_dataset.json generated/augmented_dataset.json`
6. Train the model using `time python3 train.py generated/augmented_dataset.json generated/model [<checkpoint>]`
7. Try the model using `python3 interactive_demo.py generated/model`

## Train model in Google Colab
Run the following cell in Google Colab:
```bash
#@title Create dataset and train model (Last output is download link)
!rm -rf sea-shanty-generator && \
git clone https://github.com/rubenhorn/sea-shanty-generator.git && \
cd sea-shanty-generator && \
pip install -r requirements.txt && \
python3 collect_dataset.py generated/raw_dataset.json && \
python3 augment_dataset.py generated/raw_dataset.json generated/augmented_dataset.json && \
time python3 train.py generated/augmented_dataset.json generated/model distilgpt2 3 && \
zip -r generated.zip generated && \
curl --upload-file sea-shanty-generator/generated.zip https://transfer.sh/generated.zip
```
