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
    example = None
    best_example = None

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            meanings = data[0].get('meanings', [])
            if meanings:
                # Use the first definition we find
                definition = meanings[0].get('definitions', [{}])[0].get('definition', definition)

                # Search ALL meanings and ALL definitions for any real example
                for meaning in meanings:
                    for d in meaning.get('definitions', []):
                        if d.get('example'):
                            # Prefer examples that actually contain the word itself
                            ex = d.get('example')
                            best_definition = d.get('definition', definition)
                            if word.lower() in ex.lower():
                                # Best case: example contains the word
                                return best_definition, ex
                            elif best_example is None:
                                # Save first example found as fallback
                                best_example = ex
                                definition = best_definition
    except Exception:
        pass

    if best_example:
        return definition, best_example

    # Smart fallback: construct a natural example from the definition
    fallback = f"Someone who is {word.lower()} tends to {definition[:60].rstrip('.').lower()}."
    if "to " in definition[:3].lower():
        # Verb — use "She decided to..." style
        fallback = f"She decided to {word.lower()} the situation carefully."
    elif definition[0].isupper() and "ing" not in word:
        # Noun/adj — use "The {word} was..." style
        fallback = f"The {word.lower()} of her argument was immediately clear to everyone."

    return definition, fallback

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
