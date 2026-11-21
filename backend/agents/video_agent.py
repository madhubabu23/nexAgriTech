def make_script(crop:str,kind:str,language:str)->str:
    if language=='te':
        return f'{crop} వంటకం: తాజా పంటను కడిగి, పదార్థాలు సిద్ధం చేసి, మెల్లగా ఉడికించి వడ్డించండి.' if kind=='recipe' else f'{crop} సాగు: నేలను సిద్ధం చేయండి, స్థానిక విత్తన రకం ఎంచుకోండి, సరైన దూరంలో నాటండి, కంపోస్ట్ వాడండి, తేమ మరియు తెగుళ్లను గమనించి, పంట సిద్ధమైనప్పుడు కోయండి.'
    if language=='hi':
        return f'{crop} रेसिपी: ताज़ी उपज धोएँ, सामग्री तैयार करें और धीमी आँच पर पकाएँ।' if kind=='recipe' else f'{crop} उगाना: मिट्टी तैयार करें, उपयुक्त बीज चुनें, सही दूरी पर बोएँ, कम्पोस्ट डालें, नमी और कीट देखें और पकने पर कटाई करें।'
    return f'{crop} recipe: wash and prepare the produce, gather seasonal ingredients, cook gently, season and serve.' if kind=='recipe' else f'{crop} growing lesson: prepare well-drained soil, choose a locally suitable variety, sow at recommended spacing, use mature compost, monitor moisture and pests, and harvest at maturity.'
