"""Static educational seed content for DEHA VEDA ECOSYSTEM.

Nutrition values are per 100 g edible portion, rounded, based on USDA FoodData Central.
Water-quality reference values are based on WHO Guidelines for Drinking-water Quality
and BIS IS 10500:2012 (Indian Standard for Drinking Water).
"""

FOOD_CATEGORIES = [
    "Fruits", "Vegetables", "Grains", "Pulses", "Nuts", "Seeds", "Dairy",
    "Protein-rich", "Traditional", "Healthy Snacks", "Beverages",
]

# name, category, kcal, protein, carbs, fat, fiber, micros, note
_FOODS = [
    ("Apple", "Fruits", 52, 0.3, 13.8, 0.2, 2.4, "Vitamin C, Potassium", "Most fibre sits in the skin; eat unpeeled when possible."),
    ("Banana", "Fruits", 89, 1.1, 22.8, 0.3, 2.6, "Potassium, Vitamin B6", "Quick carbohydrate source, useful before activity."),
    ("Mango", "Fruits", 60, 0.8, 15.0, 0.4, 1.6, "Vitamin A, Vitamin C", "Rich in beta-carotene, a vitamin A precursor."),
    ("Papaya", "Fruits", 43, 0.5, 10.8, 0.3, 1.7, "Vitamin C, Folate", "Contains the enzyme papain."),
    ("Guava", "Fruits", 68, 2.6, 14.3, 1.0, 5.4, "Vitamin C, Folate", "Exceptionally high vitamin C for a fruit."),
    ("Orange", "Fruits", 47, 0.9, 11.8, 0.1, 2.4, "Vitamin C, Thiamine", "Whole fruit gives more fibre than juice."),
    ("Pomegranate", "Fruits", 83, 1.7, 18.7, 1.2, 4.0, "Vitamin K, Potassium", "Arils contain polyphenols."),
    ("Watermelon", "Fruits", 30, 0.6, 7.6, 0.2, 0.4, "Vitamin A, Lycopene", "About 92% water by weight."),
    ("Grapes", "Fruits", 69, 0.7, 18.1, 0.2, 0.9, "Vitamin K, Copper", "Energy-dense for a fruit; portion matters."),
    ("Spinach", "Vegetables", 23, 2.9, 3.6, 0.4, 2.2, "Vitamin K, Folate, Iron", "Plant iron absorbs better with vitamin C."),
    ("Broccoli", "Vegetables", 34, 2.8, 6.6, 0.4, 2.6, "Vitamin C, Vitamin K", "Steaming retains more vitamin C than boiling."),
    ("Carrot", "Vegetables", 41, 0.9, 9.6, 0.2, 2.8, "Vitamin A (beta-carotene)", "Carotenoids absorb better with some fat."),
    ("Tomato", "Vegetables", 18, 0.9, 3.9, 0.2, 1.2, "Vitamin C, Lycopene", "Cooking increases lycopene availability."),
    ("Cauliflower", "Vegetables", 25, 1.9, 5.0, 0.3, 2.0, "Vitamin C, Vitamin K", "Low calorie, versatile cruciferous vegetable."),
    ("Bottle Gourd", "Vegetables", 14, 0.6, 3.4, 0.0, 0.5, "Vitamin C, Potassium", "Very high water content, light on digestion."),
    ("Okra (Bhindi)", "Vegetables", 33, 1.9, 7.5, 0.2, 3.2, "Vitamin K, Folate", "Mucilage contributes soluble fibre."),
    ("Sweet Potato", "Vegetables", 86, 1.6, 20.1, 0.1, 3.0, "Vitamin A, Potassium", "Lower glycaemic impact when boiled vs baked."),
    ("Beetroot", "Vegetables", 43, 1.6, 9.6, 0.2, 2.8, "Folate, Manganese, Nitrates", "Dietary nitrates are studied for blood-flow effects."),
    ("Brown Rice", "Grains", 123, 2.7, 25.6, 1.0, 1.6, "Magnesium, Manganese", "Cooked values; bran layer retains fibre."),
    ("White Rice", "Grains", 130, 2.7, 28.2, 0.3, 0.4, "Manganese, Selenium", "Cooked; polishing removes most bran fibre."),
    ("Whole Wheat Flour", "Grains", 340, 13.2, 72.0, 2.5, 10.7, "Iron, Magnesium, B vitamins", "Raw flour values."),
    ("Oats", "Grains", 389, 16.9, 66.3, 6.9, 10.6, "Manganese, Phosphorus, Beta-glucan", "Beta-glucan is a soluble fibre."),
    ("Finger Millet (Ragi)", "Grains", 328, 7.3, 72.0, 1.3, 3.6, "Calcium, Iron", "Among the higher-calcium cereal grains."),
    ("Pearl Millet (Bajra)", "Grains", 361, 11.6, 67.5, 5.0, 1.2, "Iron, Magnesium", "Traditional dryland grain of India."),
    ("Quinoa", "Grains", 120, 4.4, 21.3, 1.9, 2.8, "Magnesium, Folate", "Cooked; contains all essential amino acids."),
    ("Red Lentils (Masoor Dal)", "Pulses", 116, 9.0, 20.1, 0.4, 7.9, "Folate, Iron, Potassium", "Cooked values; quick-cooking pulse."),
    ("Chickpeas (Chana)", "Pulses", 164, 8.9, 27.4, 2.6, 7.6, "Folate, Iron, Manganese", "Cooked; pairs well with cereals for protein quality."),
    ("Kidney Beans (Rajma)", "Pulses", 127, 8.7, 22.8, 0.5, 6.4, "Folate, Iron", "Must be boiled well; never eat undercooked."),
    ("Pigeon Pea (Toor Dal)", "Pulses", 343, 21.7, 62.8, 1.5, 15.0, "Folate, Magnesium", "Raw values; a staple Indian dal."),
    ("Green Gram (Moong)", "Pulses", 105, 7.0, 19.2, 0.4, 7.6, "Folate, Manganese", "Cooked; easily sprouted."),
    ("Almonds", "Nuts", 579, 21.2, 21.6, 49.9, 12.5, "Vitamin E, Magnesium", "Energy dense; a 28 g handful is a typical serving."),
    ("Walnuts", "Nuts", 654, 15.2, 13.7, 65.2, 6.7, "Omega-3 ALA, Copper", "Highest plant ALA among common nuts."),
    ("Cashews", "Nuts", 553, 18.2, 30.2, 43.9, 3.3, "Copper, Magnesium, Iron", "Higher carbohydrate than most nuts."),
    ("Peanuts", "Nuts", 567, 25.8, 16.1, 49.2, 8.5, "Niacin, Folate, Vitamin E", "Botanically a legume, used like a nut."),
    ("Pistachios", "Nuts", 560, 20.2, 27.2, 45.3, 10.6, "Vitamin B6, Potassium", "Shelling slows eating pace naturally."),
    ("Flax Seeds", "Seeds", 534, 18.3, 28.9, 42.2, 27.3, "Omega-3 ALA, Lignans", "Grind before eating for better absorption."),
    ("Chia Seeds", "Seeds", 486, 16.5, 42.1, 30.7, 34.4, "Calcium, Phosphorus", "Absorbs many times its weight in water."),
    ("Pumpkin Seeds", "Seeds", 559, 30.2, 10.7, 49.1, 6.0, "Magnesium, Zinc, Iron", "Notably high in magnesium."),
    ("Sesame Seeds", "Seeds", 573, 17.7, 23.4, 49.7, 11.8, "Calcium, Copper", "Traditional til used in Indian sweets."),
    ("Sunflower Seeds", "Seeds", 584, 20.8, 20.0, 51.5, 8.6, "Vitamin E, Selenium", "Good source of vitamin E."),
    ("Cow Milk (Whole)", "Dairy", 61, 3.2, 4.8, 3.3, 0.0, "Calcium, Vitamin B12, Riboflavin", "Per 100 ml; a cup is about 240 ml."),
    ("Curd / Yogurt (Plain)", "Dairy", 61, 3.5, 4.7, 3.3, 0.0, "Calcium, B12, Probiotic cultures", "Live cultures vary by product."),
    ("Paneer", "Dairy", 265, 18.3, 1.2, 20.8, 0.0, "Calcium, Phosphorus", "Fresh Indian cheese; energy dense."),
    ("Buttermilk (Chaas)", "Dairy", 40, 3.3, 4.8, 0.9, 0.0, "Calcium, Potassium", "Traditional light post-meal drink."),
    ("Ghee", "Dairy", 900, 0.0, 0.0, 100.0, 0.0, "Vitamin A, Vitamin K2", "Almost pure fat; use small quantities."),
    ("Egg (Whole, boiled)", "Protein-rich", 155, 12.6, 1.1, 10.6, 0.0, "Vitamin B12, Choline, Selenium", "Complete protein with high digestibility."),
    ("Chicken Breast (cooked)", "Protein-rich", 165, 31.0, 0.0, 3.6, 0.0, "Niacin, B6, Selenium", "Lean animal protein."),
    ("Rohu Fish", "Protein-rich", 97, 16.6, 0.0, 1.4, 0.0, "Vitamin B12, Phosphorus", "Common Indian freshwater fish."),
    ("Tofu", "Protein-rich", 76, 8.1, 1.9, 4.8, 0.3, "Calcium, Iron, Manganese", "Soy protein; calcium depends on the setting agent."),
    ("Soybean (boiled)", "Protein-rich", 172, 18.2, 8.4, 9.0, 6.0, "Iron, Folate, Magnesium", "One of the highest-protein plant foods."),
    ("Idli", "Traditional", 130, 3.9, 27.0, 0.4, 1.2, "B vitamins from fermentation", "Steamed and fermented, easy to digest."),
    ("Dosa (plain)", "Traditional", 168, 3.7, 30.0, 3.7, 1.5, "B vitamins, Iron", "Fermented rice-lentil crepe."),
    ("Khichdi", "Traditional", 120, 4.5, 20.0, 2.2, 2.0, "Iron, Folate", "Rice and dal together give a fuller amino profile."),
    ("Poha", "Traditional", 130, 2.5, 27.0, 1.5, 1.0, "Iron", "Flattened rice, often fortified with iron."),
    ("Upma", "Traditional", 145, 3.6, 24.0, 3.8, 1.8, "B vitamins", "Semolina based, quick breakfast."),
    ("Roasted Chana", "Healthy Snacks", 380, 22.0, 58.0, 5.0, 18.0, "Iron, Folate, Fibre", "High-fibre, high-protein dry snack."),
    ("Makhana (Fox Nut)", "Healthy Snacks", 347, 9.7, 76.9, 0.1, 14.5, "Magnesium, Potassium", "Very low fat when dry roasted."),
    ("Sprouts Salad", "Healthy Snacks", 90, 6.5, 14.0, 0.6, 4.5, "Vitamin C, Folate", "Sprouting increases vitamin C."),
    ("Fruit Chaat", "Healthy Snacks", 75, 1.0, 18.0, 0.3, 2.5, "Vitamin C, Potassium", "Keep added salt and sugar low."),
    ("Coconut Water", "Beverages", 19, 0.7, 3.7, 0.2, 1.1, "Potassium, Magnesium", "Per 100 ml; natural electrolyte drink."),
    ("Green Tea (unsweetened)", "Beverages", 1, 0.0, 0.0, 0.0, 0.0, "Catechins, Fluoride", "Essentially calorie free without sugar or milk."),
    ("Lemon Water (no sugar)", "Beverages", 6, 0.1, 2.0, 0.0, 0.1, "Vitamin C", "Simple low-calorie hydration option."),
    ("Sugarcane Juice", "Beverages", 74, 0.2, 18.0, 0.0, 0.0, "Potassium, Iron", "High free-sugar content; drink sparingly."),
    ("Masala Chai (with milk & sugar)", "Beverages", 62, 1.5, 9.5, 1.8, 0.0, "Calcium", "Calories depend heavily on sugar added."),
]

FOODS = [
    {
        "name": n, "category": c, "serving_size": "100 g (or 100 ml for liquids)",
        "calories": kc, "protein_g": p, "carbs_g": cb, "fat_g": f, "fiber_g": fb,
        "micronutrients": m, "note": note,
        "source": "USDA FoodData Central / IFCT",
    }
    for (n, c, kc, p, cb, f, fb, m, note) in _FOODS
]

WATER_TYPES = [
    {"name": "What is water?", "summary": "Water is a molecule of two hydrogen atoms bonded to one oxygen atom (H2O). Its polarity makes it an excellent solvent, which is why natural water always carries dissolved minerals, gases and sometimes contaminants."},
    {"name": "Drinking Water", "summary": "Water intended for human consumption that meets microbiological and chemical safety standards. WHO defines safe drinking water as water that does not represent a significant risk to health over a lifetime of consumption."},
    {"name": "Groundwater", "summary": "Water stored below the land surface in the pores and fractures of soil and rock, forming aquifers. It is usually low in turbidity and microbes but can carry dissolved minerals such as fluoride, iron, arsenic or nitrate depending on local geology."},
    {"name": "Surface Water", "summary": "Water in rivers, lakes, ponds and reservoirs. It is more exposed to rainfall runoff, sewage and industrial discharge, so it generally needs full treatment including disinfection."},
    {"name": "Rainwater", "summary": "Precipitation collected before it touches the ground for long. Naturally low in dissolved minerals and slightly acidic because it absorbs atmospheric carbon dioxide. Roof material and first-flush handling decide its safety."},
    {"name": "Mineral Water", "summary": "Water from a protected underground source with a stable, naturally occurring mineral content. Regulations require the mineral composition to be declared on the label."},
    {"name": "Spring Water", "summary": "Groundwater that flows naturally to the surface at a spring. Composition depends entirely on the rock it passed through, and it still requires testing before consumption."},
    {"name": "Filtered Water", "summary": "Water passed through a physical or activated-carbon medium to reduce turbidity, chlorine, taste and odour. Simple filtration alone does not reliably remove bacteria, viruses or dissolved salts."},
    {"name": "Purified Water", "summary": "An umbrella term for water treated to remove chemicals and microbes, by methods such as distillation, deionisation or reverse osmosis, to meet a defined purity specification."},
    {"name": "RO Water", "summary": "Reverse osmosis forces water through a semi-permeable membrane, removing most dissolved salts, heavy metals and microbes. It also removes beneficial minerals and produces reject water, so it is best used where TDS is genuinely high."},
    {"name": "Distilled Water", "summary": "Water boiled to steam and condensed back to liquid, leaving nearly all dissolved solids behind. It is very pure but flat tasting and mineral free; mostly used for laboratory and appliance purposes."},
    {"name": "Bottled Water", "summary": "Packaged water which may be mineral, spring, purified or RO water. Quality varies by brand and storage; heat and sunlight exposure and plastic type affect taste and possible leaching."},
]

WATER_JOURNEY = [
    {"step": 1, "title": "Rain", "description": "Precipitation falls, absorbing atmospheric gases and dust.", "risk": "Air pollution and dust can dissolve into falling rain."},
    {"step": 2, "title": "Soil", "description": "Water infiltrates topsoil where organic matter and minerals interact with it.", "risk": "Fertiliser, pesticide and animal-waste leaching."},
    {"step": 3, "title": "Groundwater", "description": "Water accumulates in aquifers, dissolving minerals from the surrounding rock.", "risk": "Geogenic fluoride, arsenic, iron and salinity; over-extraction."},
    {"step": 4, "title": "Collection", "description": "Water is drawn through borewells, open wells, or taken from rivers and reservoirs.", "risk": "Unsealed well heads and contaminated surroundings."},
    {"step": 5, "title": "Treatment", "description": "Screening, coagulation, sedimentation, filtration and disinfection remove particles and pathogens.", "risk": "Under-dosed disinfection or treatment breakdown."},
    {"step": 6, "title": "Storage", "description": "Treated water is held in service reservoirs and overhead tanks before supply.", "risk": "Uncovered tanks, biofilm growth, insect and bird ingress."},
    {"step": 7, "title": "Distribution", "description": "Pipelines and pumps carry water to neighbourhoods.", "risk": "Leaking joints and low pressure allow back-siphoning of sewage."},
    {"step": 8, "title": "Home", "description": "Water reaches household tanks, filters and taps.", "risk": "Dirty sumps, unwashed filters, expired filter cartridges."},
    {"step": 9, "title": "Drinking", "description": "Water is poured, stored in a vessel and consumed.", "risk": "Unclean bottles and jugs, dipping hands into stored water."},
]

WATER_PARAMETERS = [
    {"name": "pH", "meaning": "A measure of how acidic or alkaline water is on a 0-14 scale.", "why": "Extreme pH corrodes pipes, changes taste and reduces the effectiveness of chlorine disinfection.", "measured": "pH meter with a glass electrode, or colour comparator strips.", "high": "Alkaline water; bitter or soda-like taste, scaling on fixtures.", "low": "Acidic water; can leach metals such as lead and copper from plumbing.", "reference": "WHO: no health-based guideline value, operational range 6.5-8.5. BIS IS 10500: 6.5-8.5."},
    {"name": "TDS (Total Dissolved Solids)", "meaning": "The total concentration of dissolved inorganic salts and small amounts of organic matter.", "why": "Affects taste, hardness and appliance scaling; very high TDS often signals other quality problems.", "measured": "Gravimetric evaporation, or estimated from electrical conductivity by a TDS meter.", "high": "Salty, bitter or brackish taste; scaling; possible high sulphate or chloride.", "low": "Flat taste and low mineral content, as with distilled or over-treated RO water.", "reference": "BIS IS 10500: desirable 500 mg/L, permissible up to 2000 mg/L when no alternative source exists. WHO considers below 600 mg/L generally palatable."},
    {"name": "Total Hardness", "meaning": "Mainly calcium and magnesium content, expressed as mg/L of calcium carbonate.", "why": "Hard water scales geysers and kettles, and consumes more soap; it is not considered a health hazard.", "measured": "EDTA titration or an ion-selective analyser.", "high": "Scale deposits, poor lathering, spotting on utensils.", "low": "Soft water, more corrosive to metal plumbing.", "reference": "BIS IS 10500: desirable 200 mg/L, permissible 600 mg/L. WHO: no health-based guideline value."},
    {"name": "Turbidity", "meaning": "Cloudiness caused by suspended particles such as silt, clay and microorganisms.", "why": "Particles shield microbes from disinfection and indicate treatment failure.", "measured": "Nephelometer, reported in NTU.", "high": "Visibly cloudy water; higher microbial risk.", "low": "Clear water, though clarity alone does not prove safety.", "reference": "WHO: ideally below 1 NTU for effective disinfection. BIS IS 10500: 1 NTU desirable, 5 NTU permissible."},
    {"name": "Chloride", "meaning": "The dissolved chloride ion, usually from natural salts, sewage or seawater intrusion.", "why": "Drives salty taste and accelerates corrosion of metal pipes.", "measured": "Argentometric titration or ion chromatography.", "high": "Salty taste; may indicate sewage contamination or saline intrusion.", "low": "No taste impact.", "reference": "BIS IS 10500: desirable 250 mg/L, permissible 1000 mg/L. WHO: taste threshold around 200-300 mg/L."},
    {"name": "Fluoride", "meaning": "A naturally occurring ion released from fluoride-bearing rocks.", "why": "Small amounts help protect teeth, while sustained excess causes dental and skeletal fluorosis.", "measured": "Ion-selective electrode or SPADNS colorimetric method.", "high": "Mottled teeth and, at prolonged high exposure, skeletal fluorosis.", "low": "Higher risk of dental caries where no other fluoride source exists.", "reference": "WHO guideline value: 1.5 mg/L. BIS IS 10500: desirable 1.0 mg/L, permissible 1.5 mg/L."},
    {"name": "Nitrate", "meaning": "An oxidised nitrogen compound largely from fertiliser, manure and sewage.", "why": "High nitrate is a health concern for bottle-fed infants because of methaemoglobinaemia risk.", "measured": "UV spectrophotometry or ion chromatography.", "high": "Strong indicator of agricultural or sewage contamination; infant health risk.", "low": "Normal for protected deep groundwater.", "reference": "WHO guideline value: 50 mg/L as nitrate. BIS IS 10500: 45 mg/L, no relaxation."},
    {"name": "Iron", "meaning": "Dissolved iron, common in reducing groundwater conditions.", "why": "Causes metallic taste, reddish-brown staining of clothes and fixtures, and encourages iron bacteria.", "measured": "Atomic absorption spectroscopy or phenanthroline colorimetry.", "high": "Rusty colour after standing, staining, metallic taste.", "low": "No aesthetic issue.", "reference": "BIS IS 10500: acceptable limit 1.0 mg/L. WHO: no health-based guideline, taste noticeable above about 0.3 mg/L."},
    {"name": "Alkalinity", "meaning": "The capacity of water to neutralise acid, mostly from bicarbonate and carbonate.", "why": "Buffers pH swings and influences corrosion control and treatment chemistry.", "measured": "Acid titration to defined pH endpoints.", "high": "Bitter taste, scaling tendency.", "low": "Poor pH buffering, water becomes corrosive more easily.", "reference": "BIS IS 10500: desirable 200 mg/L, permissible 600 mg/L as CaCO3."},
    {"name": "Microbial Contamination", "meaning": "Presence of bacteria, viruses or protozoa, monitored using indicator organisms such as E. coli and total coliforms.", "why": "This is the most immediate health risk in drinking water and causes most waterborne disease.", "measured": "Membrane filtration, multiple-tube fermentation, or H2S strip presence-absence tests.", "high": "Any detection indicates faecal or environmental contamination; water is unsafe until treated.", "low": "Absence of E. coli in a 100 mL sample is the basic safety expectation.", "reference": "WHO and BIS IS 10500: E. coli and thermotolerant coliforms must not be detectable in any 100 mL sample."},
]

WATER_CONTAMINATION = [
    {"type": "Biological Contamination", "detail": "Bacteria, viruses, protozoa and helminths entering water from human or animal faeces. Causes diarrhoeal disease, typhoid, hepatitis A and giardiasis.", "prevention": "Protect the source, disinfect (boiling, chlorination, UV), and keep storage sealed."},
    {"type": "Chemical Contamination", "detail": "Industrial solvents, detergents, disinfection by-products and petroleum compounds dissolved in water. Effects depend on the chemical and dose.", "prevention": "Source control, activated carbon, and regular laboratory testing."},
    {"type": "Heavy Metals", "detail": "Arsenic, lead, cadmium, chromium and mercury from geology, old plumbing or industry. Chronic exposure is the main concern rather than immediate illness.", "prevention": "Switch to a safe source, replace lead plumbing, use verified RO or specific media filters."},
    {"type": "Agricultural Contamination", "detail": "Fertiliser nitrate, phosphate and pesticide residues washed into surface water or leached to shallow groundwater.", "prevention": "Buffer strips, controlled fertiliser use, deeper protected wells, activated carbon for pesticides."},
    {"type": "Industrial Contamination", "detail": "Untreated effluent adding metals, dyes, acids, alkalis and organics; often shows up as unusual colour, foam or odour.", "prevention": "Effluent treatment enforcement, alternative sources, community monitoring."},
    {"type": "Microplastics and Emerging Contaminants", "detail": "Plastic fragments, pharmaceutical residues and personal-care chemicals now detected at low levels in many supplies. WHO notes current evidence does not indicate a health risk at observed levels, but data are still limited.", "prevention": "Reduce plastic use, prefer glass or steel storage, advanced filtration where available."},
    {"type": "Storage Contamination", "detail": "Safe water becoming unsafe at home through uncovered tanks, dirty sumps, algae growth, dipping utensils or unwashed bottles.", "prevention": "Clean tanks every six months, keep lids closed, use narrow-mouth vessels with taps."},
]

WATER_GALLERY = [
    {"caption": "Groundwater rising from a borewell", "alt": "Water gushing from a borewell pipe into a field", "url": "/images/jala-borewell.jpg"},
    {"caption": "Traditional open well recharge structure", "alt": "Open stone-lined well beside a tree in a green field", "url": "/images/jala-well.jpg"},
    {"caption": "Clarifier tank at a water treatment plant", "alt": "Aerial view of a circular water treatment clarifier", "url": "/images/jala-treatment.jpg"},
    {"caption": "Hand pump drawing shallow groundwater", "alt": "Iron hand pump standing in sandy soil near farmland", "url": "/images/jala-handpump.jpg"},
    {"caption": "River water, a common surface source", "alt": "River flowing between green banks", "url": "/images/jala-river.jpg"},
]

MANAS_TOPICS = [
    {"title": "What is the mind?", "detail": "In everyday and traditional usage the mind refers to the whole of our thinking, feeling and willing. Scientifically, mental activity is understood as processes arising from the brain and nervous system in interaction with the body and environment."},
    {"title": "Brain vs mind", "detail": "The brain is a physical organ that can be imaged and dissected. The mind is the set of functions and experiences associated with brain activity. Talking about them separately is useful, but the mind is not a separate object located somewhere in the skull."},
    {"title": "Thoughts", "detail": "Thoughts are transient patterns of neural activity that carry meaning. Most arise without deliberate effort; noticing them without immediately acting on them is a trainable skill."},
    {"title": "Attention", "detail": "Attention selects a small part of available information for deeper processing. It has limited capacity, which is why task switching costs time and accuracy."},
    {"title": "Memory", "detail": "Memory involves encoding, storage and retrieval across sensory, working and long-term systems. Spacing, retrieval practice and sleep all strengthen retention."},
    {"title": "Emotions", "detail": "Emotions are coordinated bodily, behavioural and experiential responses that bias attention and decision making. Naming an emotion accurately can help regulate it."},
    {"title": "Perception", "detail": "Perception is an active construction: the brain combines incoming signals with prior expectation. Illusions are useful evidence of this predictive process."},
    {"title": "Habits", "detail": "Habits are cue-driven behaviours that require little conscious control. Changing a habit is usually easier by redesigning the cue and environment than by relying on willpower."},
    {"title": "Stress", "detail": "Stress is the body's mobilisation response to demand. Short bursts can improve performance, while prolonged activation is linked to poorer sleep, mood and cardiovascular health."},
    {"title": "Relaxation", "detail": "Slow breathing, progressive muscle relaxation and restful activity shift the balance toward parasympathetic activity, which is measurable as lowered heart rate and breathing rate."},
    {"title": "Sleep", "detail": "Most adults need about seven to nine hours. Sleep supports memory consolidation, emotional regulation and metabolic health; consistent timing matters as much as duration."},
    {"title": "Focus", "detail": "Sustained focus improves with removing interruptions, working in defined blocks, and taking genuine breaks. Focus is a state you set up conditions for, not something forced."},
]

BRAIN_REGIONS = [
    {"key": "prefrontal", "name": "Prefrontal Cortex", "position": [0.0, 0.35, 1.05], "color": "#38BDF8", "detail": "The front region strongly associated with planning, working memory, decision making and inhibiting impulses. It is among the last areas to fully mature."},
    {"key": "motor", "name": "Motor Cortex", "position": [0.0, 1.05, 0.05], "color": "#F59E0B", "detail": "A strip running across the top of the brain that sends commands for voluntary movement, mapped roughly body-part by body-part."},
    {"key": "temporal", "name": "Temporal Lobe", "position": [-1.05, -0.3, 0.3], "color": "#A855F7", "detail": "Sits at the side and handles hearing, language comprehension and object recognition."},
    {"key": "hippocampus", "name": "Hippocampus", "position": [0.55, -0.35, 0.15], "color": "#10B981", "detail": "A deep, curved structure essential for forming new long-term memories and for spatial navigation."},
    {"key": "amygdala", "name": "Amygdala", "position": [-0.6, -0.5, 0.45], "color": "#EF4444", "detail": "An almond-shaped cluster that helps detect salience and threat and contributes to emotional learning."},
    {"key": "occipital", "name": "Occipital Lobe", "position": [0.0, 0.05, -1.1], "color": "#6366F1", "detail": "The rear region where visual information is first processed into edges, motion and colour."},
    {"key": "cerebellum", "name": "Cerebellum", "position": [0.0, -0.75, -0.85], "color": "#F472B6", "detail": "The 'little brain' below and behind the cerebrum, coordinating balance, timing and smooth movement, with a role in learning sequences."},
    {"key": "brainstem", "name": "Brainstem", "position": [0.0, -1.05, -0.1], "color": "#94A3B8", "detail": "Connects brain to spinal cord and regulates breathing, heart rate, arousal and sleep-wake transitions."},
]

PEACEFUL_MIND = [
    {"title": "Reduced distractions", "detail": "Fewer interruptions lower the mental cost of switching tasks and are associated with less perceived stress. Silencing notifications is a simple, evidence-aligned starting point."},
    {"title": "Sleep", "detail": "Regular, adequate sleep is one of the strongest correlates of stable mood and better attention the next day."},
    {"title": "Physical activity", "detail": "Regular moderate activity is consistently associated with improved mood and reduced anxiety symptoms in the general population."},
    {"title": "Breathing", "detail": "Slow paced breathing at around six breaths per minute can reduce measured arousal for many people. It is a self-regulation tool, not a treatment."},
    {"title": "Meditation and mindfulness", "detail": "Structured mindfulness programmes show small to moderate benefits for stress and wellbeing in reviews of controlled trials. Results vary between individuals."},
    {"title": "Environment", "detail": "Light, noise, temperature and time in green spaces all influence how calm a setting feels and how easily attention recovers."},
    {"title": "Attention management", "detail": "Choosing what to attend to, in blocks, with defined stopping points, reduces the feeling of mental overload."},
    {"title": "Social connection", "detail": "Supportive relationships are among the strongest population-level predictors of wellbeing."},
    {"title": "Relaxation practices", "detail": "Progressive muscle relaxation, unhurried walks, music and rest are low-risk ways to lower physiological arousal."},
]
