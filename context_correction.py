import spacy
from transformers import pipeline
import torch

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load grammar correction model
grammar_corrector = pipeline(
    "text2text-generation",
    model="prithivida/grammar_error_correcter_v1",
    device=0 if torch.cuda.is_available() else -1
)

def analyze_sentence(text):
    doc = nlp(text)
    errors = []

    for token in doc:
        if token.dep_ == "nsubj" and token.head.tag_ != "VBZ":
            errors.append(f"Verb agreement error with: {token.text}")

    return errors

def correct_text(text):
    text = text.strip()

    corrected = grammar_corrector(
        text,
        max_length=128,
        num_beams=4,
        early_stopping=True
    )[0]['generated_text']

    errors = analyze_sentence(corrected)

    return corrected, errors
