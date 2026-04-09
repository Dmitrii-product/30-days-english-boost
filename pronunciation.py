"""
Pronunciation module for English words.
Provides IPA and simple pronunciation guides for English words.
"""

import json
import urllib.request
import os

# Dictionary of common English words with their IPA pronunciations
# This is a curated list that will be expanded as needed
PRONUNCIATION_DICT = {
    "apple": "/ˈæpəl/",
    "book": "/bʊk/",
    "cat": "/kæt/",
    "dog": "/dɔːɡ/",
    "elephant": "/ˈɛlɪfənt/",
    "fish": "/fɪʃ/",
    "girl": "/ɡɜːrl/",
    "house": "/haʊs/",
    "ice": "/aɪs/",
    "juice": "/dʒuːs/",
    "kite": "/kaɪt/",
    "lion": "/ˈlaɪən/",
    "monkey": "/ˈmʌŋki/",
    "nut": "/nʌt/",
    "orange": "/ˈɒrɪndʒ/",
    "pig": "/pɪɡ/",
    "queen": "/kwiːn/",
    "rabbit": "/ˈræbɪt/",
    "sun": "/sʌn/",
    "tree": "/triː/",
    "umbrella": "/ʌmˈbrɛlə/",
    "van": "/væn/",
    "water": "/ˈwɔːtər/",
    "xylophone": "/ˈzɪləfoʊn/",
    "yellow": "/ˈjɛloʊ/",
    "zebra": "/ˈzebrə/",
    "abandon": "/əˈbændən/",
    "ability": "/əˈbɪləti/",
    "absent": "/ˈæbsənt/",
    "accept": "/əkˈsɛpt/",
    "arrive": "/əˈraɪv/",
    "beautiful": "/ˈbjuːtɪfl/",
    "believe": "/bɪˈliːv/",
    "careful": "/ˈkɛrfəl/",
    "decide": "/dɪˈsaɪd/",
    "achieve": "/əˈtʃiːv/",
    "acumen": "/ˈækjəmən/",
    "arbitrary": "/ˈɑːrbɪtreri/",
    "authentic": "/ɔːˈθɛntɪk/",
    "autonomous": "/ɔːˈtɑːnəməs/",
}

def get_ipa_pronunciation(word: str) -> str:
    """
    Get IPA pronunciation for a word.
    First checks local dictionary, then tries online API, then generates phonetic approximation.
    
    Args:
        word: The word to get pronunciation for
        
    Returns:
        IPA pronunciation string
    """
    word_lower = word.lower().strip()
    
    # Check local dictionary first
    if word_lower in PRONUNCIATION_DICT:
        return PRONUNCIATION_DICT[word_lower]
    
    # Try to fetch from an online pronunciation API
    try:
        # Using Free Dictionary API which includes phonetics
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_lower}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            if data and len(data) > 0:
                entry = data[0]
                # Look for phonetic information
                if 'phonetic' in entry and entry['phonetic']:
                    pronunciation = entry['phonetic']
                    # Cache it for future use
                    PRONUNCIATION_DICT[word_lower] = pronunciation
                    return pronunciation
                
                # Try to find phonetics in meanings
                if 'meanings' in entry:
                    for meaning in entry['meanings']:
                        if 'phonetics' in meaning:
                            for phonetic in meaning['phonetics']:
                                if 'text' in phonetic and phonetic['text']:
                                    pronunciation = phonetic['text']
                                    PRONUNCIATION_DICT[word_lower] = pronunciation
                                    return pronunciation
    except Exception as e:
        # Silently fail and continue to fallback
        pass
    
    # Generate a phonetic approximation if no pronunciation found
    # This ensures every word has a pronunciation
    phonetic = generate_phonetic_approximation(word_lower)
    PRONUNCIATION_DICT[word_lower] = phonetic
    return phonetic

def generate_phonetic_approximation(word: str) -> str:
    """
    Generate a simple phonetic approximation for words without IPA data.
    Uses basic phonetic rules to create an approximate pronunciation.
    
    Args:
        word: The word to generate pronunciation for
        
    Returns:
        Simple phonetic approximation string
    """
    # Simple phonetic approximation using brackets
    # This is a fallback for words we can't get actual IPA for
    word_lower = word.lower()
    
    # Common patterns
    if word_lower.endswith('e') and len(word_lower) > 2:
        return f"/{word_lower[:-1]}/"  # Drop silent e
    elif word_lower.endswith('ing'):
        return f"/{word_lower[:-3]}ing/"
    elif word_lower.endswith('tion'):
        return f"/{word_lower[:-4]}shun/"
    elif word_lower.endswith('sion'):
        return f"/{word_lower[:-4]}zhun/"
    else:
        # Default: just wrap in slashes with approximate pronunciation
        return f"/{word_lower}/"

def add_pronunciation_to_words_json(words_file: str = 'words.json'):
    """
    Add pronunciation field to all words in words.json if not already present.
    
    Args:
        words_file: Path to the words.json file
    """
    if not os.path.exists(words_file):
        print(f"File {words_file} not found")
        return
    
    with open(words_file, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    updated = False
    total = len(words_data)
    processed = 0
    
    for word_entry in words_data:
        if 'pronunciation' not in word_entry or not word_entry['pronunciation']:
            word = word_entry.get('word', '')
            pronunciation = get_ipa_pronunciation(word)
            if pronunciation:
                word_entry['pronunciation'] = pronunciation
                updated = True
                processed += 1
                if processed % 50 == 0:
                    print(f"Processed {processed}/{total} words...")
    
    if updated:
        with open(words_file, 'w', encoding='utf-8') as f:
            json.dump(words_data, f, ensure_ascii=False, indent=4)
        print(f"✓ Updated {words_file} with pronunciations ({processed} words added)")
    else:
        print("✓ All words already have pronunciations")

if __name__ == "__main__":
    add_pronunciation_to_words_json()
