import json
import urllib.request
import time

levels_words = {
    "A1": [
        "apple", "book", "cat", "dog", "elephant", "fish", "girl", "house", "ice", "juice",
        "kite", "lion", "monkey", "nut", "orange", "pig", "queen", "rabbit", "sun", "tree",
        "umbrella", "van", "water", "xylophone", "yellow", "zebra", "boy", "car", "door", "egg",
        "flower", "grape", "hat", "island", "jam", "key", "leaf", "mouse", "nose", "owl",
        "pen", "quilt", "ring", "star", "table", "uncle", "vase", "window", "box", "yard",
        "ball", "bed", "bird", "bread", "brother", "chair", "child", "clock", "cold", "cow",
        "cup", "desk", "duck", "earth", "eye", "farm", "fire", "foot", "friend", "game",
        "glass", "hand", "head", "horse", "hotel", "hour", "man", "milk", "money", "month",
        "moon", "morning", "mother", "night", "paper", "park", "phone", "pencil", "picture", "plane",
        "river", "road", "room", "school", "sea", "shoe", "sister", "snow", "train", "woman"
    ],
    "A2": [
        "arrive", "beautiful", "careful", "decide", "empty", "famous", "guess", "huge", "invite", "joke",
        "kiss", "loud", "meal", "nervous", "offer", "promise", "quiet", "relax", "share", "tired",
        "useful", "village", "wake", "accept", "borrow", "choose", "describe", "earn", "forget", "happen",
        "improve", "join", "keep", "laugh", "mention", "notice", "own", "prepare", "repair", "spend",
        "teach", "understand", "visit", "worry", "agree", "believe", "cancel", "dream", "explain", "fail",
        "actor", "address", "adult", "advice", "airport", "animal", "answer", "area", "art", "aunt",
        "autumn", "baby", "bag", "bake", "band", "bank", "bath", "bear", "beard", "beat",
        "beef", "beer", "bell", "belt", "bike", "bill", "bite", "blood", "board", "boat",
        "body", "bone", "border", "bottle", "bowl", "brain", "branch", "bridge", "budget", "build",
        "burn", "bush", "button", "cake", "camera", "camp", "card", "castle", "cause", "chain"
    ],
    "B1": [
        "advantage", "confident", "develop", "experience", "frequent", "gather", "hesitate", "independent", "justify", "knowledge",
        "locate", "manage", "negotiate", "observe", "participate", "qualify", "recognize", "suggest", "translate", "unique",
        "valuable", "wonder", "achieve", "balance", "challenge", "defend", "encourage", "familiar", "generate", "handle",
        "identify", "judge", "maintain", "organize", "perform", "recommend", "satisfy", "tend", "urgent", "variety",
        "wealth", "abroad", "benefit", "compete", "demand", "efficient", "feature", "guarantee", "highlight", "ignore",
        "ability", "absolute", "academic", "access", "accident", "account", "action", "active", "actual", "addition",
        "admit", "advance", "affair", "affect", "afford", "agency", "agent", "agreement", "ahead", "aim",
        "airline", "alive", "allow", "amount", "amuse", "ancient", "anger", "announce", "annual", "anyway",
        "apart", "apparent", "appeal", "appear", "apply", "approach", "argue", "arise", "army", "arrange",
        "arrest", "attack", "attempt", "attend", "attract", "author", "average", "avoid", "award", "aware"
    ],
    "B2": [
        "analyze", "beneficial", "controversy", "demonstrate", "evaluate", "facilitate", "generate", "hypothesis", "implement", "justify",
        "kinematics", "logical", "manipulate", "neutral", "objective", "perspective", "qualitative", "relevant", "significant", "theoretical",
        "undergo", "validity", "widespread", "abandon", "consequence", "crucial", "distinguish", "emerge", "fundamental", "hierarchy",
        "imply", "inevitable", "modify", "notion", "obtain", "perceive", "proportion", "reject", "reveal", "sequence",
        "subsequent", "transform", "ultimate", "vary", "visible", "accommodate", "anticipate", "coherent", "contradict", "derive",
        "abstract", "accurate", "acknowledge", "acquire", "adequate", "adjacent", "adjust", "administer", "advocate", "aggregate",
        "allocate", "alter", "alternative", "amend", "analogy", "anticipate", "apparent", "append", "appreciate", "approach",
        "appropriate", "approximate", "arbitrary", "aspect", "assemble", "assess", "assign", "assist", "assume", "assure",
        "attach", "attain", "attitude", "attribute", "authority", "automate", "available", "behalf", "bias", "bond",
        "brief", "bulk", "capable", "capacity", "category", "cease", "channel", "clause", "collapse", "commission"
    ],
    "C1": [
        "ambiguous", "diligent", "mitigate", "paradigm", "synthesize", "abundant", "cohesive", "discrepancy", "empirical", "fluctuate",
        "innovative", "lucrative", "meticulous", "nuance", "obscure", "pragmatic", "quantifiable", "resilient", "tentative", "viable",
        "alleviate", "catalyst", "delineate", "elucidate", "foster", "intrinsic", "marginal", "omnipresent", "pervasive", "reiterate",
        "scrutinize", "tangible", "ubiquitous", "vindicate", "zealous", "arbitrary", "cogent", "dexterity", "exacerbate", "feasible",
        "garrulous", "impetuous", "juxtapose", "lethargic", "myopic", "nefarious", "obfuscate", "pedantic", "quixotic", "rhetoric",
        "sycophant",
        "appalling", "apprehend", "archaic", "articulate", "ascertain", "assiduous", "assimilate", "asterisk", "astute", "audacious",
        "augment", "austere", "authentic", "autonomous", "avert", "avid", "axiom", "baffle", "banal", "barrage",
        "barren", "barrier", "bashful", "beguile", "behoove", "belie", "belligerent", "benchmark", "benevolent", "benign",
        "berate", "bereft", "beseech", "beset", "besiege", "bizarre", "bland", "blatant", "bleak", "blight",
        "boisterous", "bolster", "bombastic", "boycott", "brace", "bravado", "brazen", "brevity", "cacophony", "cajole"
    ],
    "C2": [
        "aberration", "capricious", "ephemeral", "fastidious", "iconoclast", "cacophony", "ebullient", "facetious", "gregarious", "hackneyed",
        "idyllic", "jargon", "knell", "lackadaisical", "magnanimous", "nonchalant", "obsequious", "panacea", "quandary", "recalcitrant",
        "stoic", "trepidation", "unctuous", "vacillate", "winsome", "xenophobia", "yoke", "zephyr", "alacrity", "bellicose",
        "chicanery", "deleterious", "enervate", "fatuous", "gauche", "hubris", "incognito", "jejune", "kinetic", "loquacious",
        "lugubrious", "mendacious", "nadir", "obdurate", "parsimonious", "querulous", "sagacious", "truculent", "usurp", "vicarious",
        "abstruse", "acumen", "adulterate", "adumbrate", "aggrandize", "alloy", "amalgamate", "ameliorate", "amenable", "anachronism",
        "anathema", "ancillary", "antediluvian", "apodictic", "apocryphal", "apotheosis", "apposite", "apprise", "approbation", "arcane",
        "arrogate", "ascetic", "asperity", "aspersion", "attenuate", "augury", "auspicious", "autocratic", "avarice", "aver",
        "avuncular", "baleful", "beatify", "bedizen", "beneficent", "bifurcate", "blandishment", "boombastic", "boorish", "bucolic",
        "burgeon", "burnish", "byzantine", "cabal", "cadge", "calumny", "canonical", "captious", "castigate", "catalyst"
    ]
}

a1_a2_translations = {
    # A1
    "apple": "яблоко", "book": "книга", "cat": "кот", "dog": "собака", "elephant": "слон", 
    "fish": "рыба", "girl": "девочка", "house": "дом", "ice": "лёд", "juice": "сок",
    "kite": "воздушный змей", "lion": "лев", "monkey": "обезьяна", "nut": "орех", "orange": "апельсин", 
    "pig": "свинья", "queen": "королева", "rabbit": "кролик", "sun": "солнце", "tree": "дерево",
    "umbrella": "зонт", "van": "фургон", "water": "вода", "xylophone": "ксилофон", "yellow": "жёлтый", 
    "zebra": "зебра", "boy": "мальчик", "car": "машина", "door": "дверь", "egg": "яйцо",
    "flower": "цветок", "grape": "виноград", "hat": "шляпа", "island": "остров", "jam": "варенье", 
    "key": "ключ", "leaf": "лист", "mouse": "мышь", "nose": "нос", "owl": "сова",
    "pen": "ручка", "quilt": "одеяло", "ring": "кольцо", "star": "звезда", "table": "стол", 
    "uncle": "дядя", "vase": "ваза", "window": "окно", "box": "коробка", "yard": "двор",
    "ball": "мяч", "bed": "кровать", "bird": "птица", "bread": "хлеб", "brother": "брат", "chair": "стул",
    "child": "ребёнок", "clock": "часы", "cold": "холод", "cow": "корова", "cup": "чашка", "desk": "парта",
    "duck": "утка", "earth": "земля", "eye": "глаз", "farm": "ферма", "fire": "огонь", "foot": "нога",
    "friend": "друг", "game": "игра", "glass": "стекло", "hand": "рука", "head": "голова", "horse": "лошадь",
    "hotel": "отель", "hour": "час", "man": "мужчина", "milk": "молоко", "money": "деньги", "month": "месяц",
    "moon": "луна", "morning": "утро", "mother": "мать", "night": "ночь", "paper": "бумага", "park": "парк",
    "phone": "телефон", "pencil": "карандаш", "picture": "картина", "plane": "самолёт", "river": "река", "road": "дорога",
    "room": "комната", "school": "школа", "sea": "море", "shoe": "обувь", "sister": "сестра", "snow": "снег",
    "train": "поезд", "woman": "женщина",
    # A2
    "arrive": "прибывать", "beautiful": "красивый", "careful": "осторожный", "decide": "решать", "empty": "пустой", 
    "famous": "знаменитый", "guess": "угадывать", "huge": "огромный", "invite": "приглашать", "joke": "шутка",
    "kiss": "поцелуй", "loud": "громкий", "meal": "приём пищи", "nervous": "нервный", "offer": "предлагать", 
    "promise": "обещать", "quiet": "тихий", "relax": "отдыхать", "share": "делиться", "tired": "уставший",
    "useful": "полезный", "village": "деревня", "wake": "просыпаться", "accept": "принимать", "borrow": "одалживать", 
    "choose": "выбирать", "describe": "описывать", "earn": "зарабатывать", "forget": "забывать", "happen": "случаться",
    "improve": "улучшать", "join": "присоединяться", "keep": "хранить", "laugh": "смеяться", "mention": "упоминать", 
    "notice": "замечать", "own": "владеть", "prepare": "готовиться", "repair": "чинить", "spend": "тратить",
    "teach": "учить", "understand": "понимать", "visit": "посещать", "worry": "волноваться", "agree": "соглашаться", 
    "believe": "верить", "cancel": "отменять", "dream": "мечтать", "explain": "объяснять", "fail": "потерпеть неудачу",
    "actor": "актёр", "address": "адрес", "adult": "взрослый", "advice": "совет", "airport": "аэропорт", "animal": "животное",
    "answer": "ответ", "area": "область", "art": "искусство", "aunt": "тётя", "autumn": "осень", "baby": "малыш",
    "bag": "сумка", "bake": "печь", "band": "группа", "bank": "банк", "bath": "ванна", "bear": "медведь",
    "beard": "борода", "beat": "бить", "beef": "говядина", "beer": "пиво", "bell": "колокол", "belt": "ремень",
    "bike": "велосипед", "bill": "счёт", "bite": "кусать", "blood": "кровь", "board": "доска", "boat": "лодка",
    "body": "тело", "bone": "кость", "border": "граница", "bottle": "бутылка", "bowl": "миска", "brain": "мозг",
    "branch": "ветка", "bridge": "мост", "budget": "бюджет", "build": "строить", "burn": "гореть", "bush": "куст",
    "button": "кнопка", "cake": "торт", "camera": "камера", "camp": "лагерь", "card": "карта", "castle": "замок",
    "cause": "причина", "chain": "цепь"
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
    total = sum(len(words) for words in levels_words.values())
    processed = 0
    
    for level, words in levels_words.items():
        for word in words:
            definition, example = get_word_data(word, level)
            
            # Add Russian translation for A1 and A2 level words
            if level in ["A1", "A2"] and word.lower() in a1_a2_translations:
                ru_trans = a1_a2_translations[word.lower()]
                definition = f"{definition} ({ru_trans})"
                
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
