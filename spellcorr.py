from symspellpy import SymSpell, Verbosity
import os

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = os.path.join(os.getcwd(), "frequency_dictionary_en_82_765.txt")
term_index = 0
count_index = 1

# Load dictionary
if os.path.exists(dictionary_path):
    sym_spell.load_dictionary(dictionary_path, term_index, count_index)
else:
    raise FileNotFoundError("Dictionary file not found!")

def correct_spelling(text):
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return text
