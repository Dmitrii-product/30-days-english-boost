import json
import urllib.request
import time

levels_words = {
    "A1": [
        "apple", "book", "cat", "dog", "elephant", "fish", "girl", "house", "ice", "juice",
        "kite", "lion", "monkey", "nut", "orange", "pig", "queen", "rabbit", "sun", "tree",
        "umbrella", "van", "water", "xylophone", "yellow", "zebra", "boy", "car", "door", "egg",
        "flower", "grape", "hat", "island", "jam", "key", "leaf", "mouse", "nose", "owl",
        "pen", "quilt", "ring", "star", "table", "uncle", "vase", "window", "box", "yard"
    ],
    "A2": [
        "arrive", "beautiful", "careful", "decide", "empty", "famous", "guess", "huge", "invite", "joke",
        "kiss", "loud", "meal", "nervous", "offer", "promise", "quiet", "relax", "share", "tired",
        "useful", "village", "wake", "accept", "borrow", "choose", "describe", "earn", "forget", "happen",
        "improve", "join", "keep", "laugh", "mention", "notice", "own", "prepare", "repair", "spend",
        "teach", "understand", "visit", "worry", "agree", "believe", "cancel", "dream", "explain", "fail"
    ],
    "B1": [
        "advantage", "confident", "develop", "experience", "frequent", "gather", "hesitate", "independent", "justify", "knowledge",
        "locate", "manage", "negotiate", "observe", "participate", "qualify", "recognize", "suggest", "translate", "unique",
        "valuable", "wonder", "achieve", "balance", "challenge", "defend", "encourage", "familiar", "generate", "handle",
        "identify", "judge", "maintain", "organize", "perform", "recommend", "satisfy", "tend", "urgent", "variety",
        "wealth", "abroad", "benefit", "compete", "demand", "efficient", "feature", "guarantee", "highlight", "ignore"
    ],
    "B2": [
        "analyze", "beneficial", "controversy", "demonstrate", "evaluate", "facilitate", "generate", "hypothesis", "implement", "justify",
        "kinematics", "logical", "manipulate", "neutral", "objective", "perspective", "qualitative", "relevant", "significant", "theoretical",
        "undergo", "validity", "widespread", "abandon", "consequence", "crucial", "distinguish", "emerge", "fundamental", "hierarchy",
        "imply", "inevitable", "modify", "notion", "obtain", "perceive", "proportion", "reject", "reveal", "sequence",
        "subsequent", "transform", "ultimate", "vary", "visible", "accommodate", "anticipate", "coherent", "contradict", "derive"
    ],
    "C1": [
        "ambiguous", "diligent", "mitigate", "paradigm", "synthesize", "abundant", "cohesive", "discrepancy", "empirical", "fluctuate",
        "innovative", "lucrative", "meticulous", "nuance", "obscure", "pragmatic", "quantifiable", "resilient", "tentative", "viable",
        "alleviate", "catalyst", "delineate", "elucidate", "foster", "intrinsic", "marginal", "omnipresent", "pervasive", "reiterate",
        "scrutinize", "tangible", "ubiquitous", "vindicate", "zealous", "arbitrary", "cogent", "dexterity", "exacerbate", "feasible",
        "garrulous", "impetuous", "juxtapose", "lethargic", "myopic", "nefarious", "obfuscate", "pedantic", "quixotic", "rhetoric",
        "sycophant"
    ],
    "C2": [
        "aberration", "capricious", "ephemeral", "fastidious", "iconoclast", "cacophony", "ebullient", "facetious", "gregarious", "hackneyed",
        "idyllic", "jargon", "knell", "lackadaisical", "magnanimous", "nonchalant", "obsequious", "panacea", "quandary", "recalcitrant",
        "stoic", "trepidation", "unctuous", "vacillate", "winsome", "xenophobia", "yoke", "zephyr", "alacrity", "bellicose",
        "chicanery", "deleterious", "enervate", "fatuous", "gauche", "hubris", "incognito", "jejune", "kinetic", "loquacious",
        "lugubrious", "mendacious", "nadir", "obdurate", "parsimonious", "querulous", "sagacious", "truculent", "usurp", "vicarious"
    ]
}

def get_word_data(word, level):
    definition = f"A {level} level English word."
    example = f"I learned the word '{word}' today."
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            meanings = data[0].get('meanings', [])
            if meanings:
                # Try to find a definition with an example
                found_def = False
                for meaning in meanings:
                    for d in meaning.get('definitions', []):
                        if not found_def:
                            definition = d.get('definition', definition)
                            found_def = True
                        if d.get('example'):
                            definition = d.get('definition')
                            example = d.get('example')
                            return definition, example
    except Exception as e:
        pass
        
    return definition, example

def main():
    all_words_data = []
    total = sum(min(50, len(words)) for words in levels_words.values())
    processed = 0
    
    for level, words in levels_words.items():
        for word in words[:50]:
            definition, example = get_word_data(word, level)
            all_words_data.append({
                "word": word.capitalize(),
                "level": level,
                "definition": definition,
                "example": example.capitalize() if example else f"Can you use '{word}' in a sentence?"
            })
            processed += 1
            if processed % 20 == 0:
                print(f"Processed {processed}/{total} words...")
            # Small delay to respect rate limits
            time.sleep(0.2)
            
    with open('words.json', 'w', encoding='utf-8') as f:
        json.dump(all_words_data, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully saved {len(all_words_data)} words to words.json!")

if __name__ == "__main__":
    main()
