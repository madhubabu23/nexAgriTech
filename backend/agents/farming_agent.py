"""Safety-first, offline organic farming guidance templates (not a diagnosis)."""
def answer(question:str,language:str='en')->str:
    q=question.lower(); te=language=='te'; hi=language=='hi'
    if any(w in q for w in ('curl','tomato','leaf','టమాట','आम')):
        return ('ఆకుల వెనుక భాగంలో తెల్లదోమ లేదా పేనును పరిశీలించండి. వేర్ల దగ్గర నేల తేమను చూడండి. చికిత్సకు ముందు స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.' if te else 'पत्तियों के नीचे सफेद मक्खी या माहू और जड़ों के पास मिट्टी की नमी जाँचें। उपचार से पहले स्थानीय कृषि अधिकारी से सलाह लें।' if hi else 'Leaf curl can have several causes, including pests, heat and water stress. Inspect multiple leaves and soil moisture; share clear photos with a local horticulture officer before choosing treatment.')
    if any(w in q for w in ('compost','manure','కంపోస్ట','खाद')):
        return ('ఎండిన ఆకులు, పంట అవశేషాలు, పాత కంపోస్ట్‌ను పొరలుగా వేసి తేమగా ఉంచండి. ప్రతి 1–2 వారాలకు తిప్పండి.' if te else 'सूखी पत्तियों और फसल अवशेषों की परतें बनाएँ, नम रखें और हर 1–2 सप्ताह पलटें।' if hi else 'Layer dry leaves with crop residues and mature compost. Keep it damp, turn every 1–2 weeks, and use when dark and crumbly.')
    if any(w in q for w in ('water','irrigat','turmeric','నీరు','पानी')):
        return ('వేర్ల దగ్గర మట్టి ఎండడం మొదలైతే నీరు పెట్టండి; నీరు నిల్వ కాకుండా చూడండి.' if te else 'जड़ों के पास मिट्टी सूखने लगे तभी पानी दें; जलभराव से बचें।' if hi else 'Check soil near the roots. Water when it starts to dry, avoid waterlogging, and use mulch to conserve moisture.')
    return ('పంటను, నేల తేమను పరిశీలించి మార్పులను నమోదు చేయండి. స్థానిక వ్యవసాయ నిపుణుడిని సంప్రదించండి.' if te else 'फसल और मिट्टी की नमी देखें, बदलाव दर्ज करें और स्थानीय कृषि विशेषज्ञ से सलाह लें।' if hi else 'Inspect affected and healthy plants, note when symptoms began, and check soil moisture and recent weather. Consult a local agriculture expert for treatment decisions.')
