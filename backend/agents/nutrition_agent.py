"""Generic sample nutrient lookup; values are estimates, not lab results."""
NUTRITION={'tomato':'18 kcal · 0.9g protein · 0.2g fat · 3.9g carbohydrates · 1.2g fiber','chilli':'40 kcal · 2g protein · 0.4g fat · 9g carbohydrates · 1.5g fiber','brinjal':'25 kcal · 1g protein · 0.2g fat · 6g carbohydrates · 3g fiber','onion':'40 kcal · 1.1g protein · 0.1g fat · 9.3g carbohydrates · 1.7g fiber'}
def lookup(name:str)->dict:
    key=next((k for k in NUTRITION if k in name.lower()),None)
    return {'per_100g':NUTRITION.get(key,'Nutrition values not available'),'source_note':'Generic estimate; values vary by variety and growing conditions.'}
