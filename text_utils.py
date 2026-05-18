import numpy as np

def decode_sequence(sequence, tokenizer):
    """
    Converts a sequence of integers back to readable text
    """
    reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}

    words = []
    for idx in sequence:
        if idx == 0:
            continue
        word = reverse_word_index.get(idx, "")
        words.append(word)

    return " ".join(words)


def clean_text(text):
    """
    Simple text cleaning
    """
    return text.replace("<OOV>", "").strip()
