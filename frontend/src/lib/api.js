import axios from "axios";

export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;
export const TOKEN_KEY = "dv_token";

export const api = axios.create({ baseURL: API, withCredentials: true });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export function apiError(err, fallback = "Something went wrong. Please try again.") {
  const detail = err?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((e) => (e && typeof e.msg === "string" ? e.msg : JSON.stringify(e))).join(" ");
  }
  if (detail && typeof detail.msg === "string") return detail.msg;
  return err?.message || fallback;
}

export const FOOD_IMAGES = {
  Fruits: "/images/food/fruits.jpg",
  Vegetables: "/images/food/vegetables.jpg",
  Grains: "/images/food/grains.jpg",
  Pulses: "/images/food/pulses.jpg",
  Nuts: "/images/food/nuts.jpg",
  Seeds: "/images/food/seeds.jpg",
  Dairy: "/images/food/dairy.jpg",
  "Protein-rich": "/images/food/protein.jpg",
  Traditional: "/images/food/traditional.jpg",
  "Healthy Snacks": "/images/food/snacks.jpg",
  Beverages: "/images/food/beverages.jpg",
};

export const foodImage = (category) => FOOD_IMAGES[category] || "/images/food/fruits.jpg";

/**
 * Per-food-item image map — keyed by exact food name as stored in the database.
 * Paths resolve to files in /public/images/food/ (photos) or
 * /public/images/food/items/ (SVG illustrations) where no photo is available.
 */
export const FOOD_ITEM_IMAGES = {
  "Apple":                          "/images/food/apple.jpg",
  "Banana":                         "/images/food/banana.jpg",
  "Mango":                          "/images/food/mango.webp",
  "Papaya":                         "/images/food/papaya.jpeg",
  "Guava":                          "/images/food/guava.jpeg",
  "Orange":                         "/images/food/orange.jpeg",
  "Pomegranate":                    "/images/food/items/pomegranate.svg",
  "Watermelon":                     "/images/food/watermelon.webp",
  "Grapes":                         "/images/food/grapes.webp",
  "Spinach":                        "/images/food/spinach.webp",
  "Broccoli":                       "/images/food/broccoli.jpg",
  "Carrot":                         "/images/food/carrot.webp",
  "Tomato":                         "/images/food/tomato.jpg",
  "Cauliflower":                    "/images/food/cauliflower.jpeg",
  "Bottle Gourd":                   "/images/food/bottle-gourd.jpg",
  "Okra (Bhindi)":                  "/images/food/okra-bhindi.jpeg",
  "Sweet Potato":                   "/images/food/sweet-potato.webp",
  "Beetroot":                       "/images/food/beetroot.jpg",
  "Brown Rice":                     "/images/food/brown-rice.avif",
  "White Rice":                     "/images/food/white_rice.jpeg",
  "Whole Wheat Flour":              "/images/food/whole-wheat-flour.jpg",
  "Oats":                           "/images/food/oats.jpg",
  "Finger Millet (Ragi)":           "/images/food/finger-millet-ragi.jpg",
  "Pearl Millet (Bajra)":           "/images/food/pearl-millet-bajra.webp",
  "Quinoa":                         "/images/food/quinoa.jpeg",
  "Red Lentils (Masoor Dal)":       "/images/food/red-lentils-masoor-dal.jpeg",
  "Chickpeas (Chana)":              "/images/food/chickpeas-chana.jpg",
  "Kidney Beans (Rajma)":           "/images/food/kidney-beans-rajma.jpg",
  "Pigeon Pea (Toor Dal)":          "/images/food/pigeon-pea-toor-dal.jpeg",
  "Green Gram (Moong)":             "/images/food/green-gram-moong.webp",
  "Almonds":                        "/images/food/almonds.jpg",
  "Walnuts":                        "/images/food/walnuts.webp",
  "Cashews":                        "/images/food/cashews.webp",
  "Peanuts":                        "/images/food/peanuts.webp",
  "Pistachios":                     "/images/food/pistachios.jpg",
  "Flax Seeds":                     "/images/food/flax-seeds.jpeg",
  "Chia Seeds":                     "/images/food/chia-seeds.webp",
  "Pumpkin Seeds":                  "/images/food/pumpkin-seeds.webp",
  "Sesame Seeds":                   "/images/food/sesame-seeds.webp",
  "Sunflower Seeds":                "/images/food/sunflower-seeds.webp",
  "Cow Milk (Whole)":               "/images/food/cow-milk-whole.jpg",
  "Curd / Yogurt (Plain)":          "/images/food/curd-yogurt-plain.jpeg",
  "Paneer":                         "/images/food/paneer.webp",
  "Buttermilk (Chaas)":             "/images/food/buttermilk-chaas.webp",
  "Ghee":                           "/images/food/ghee.jpeg",
  "Egg (Whole, boiled)":            "/images/food/egg-whole-boiled.jpeg",
  "Chicken Breast (cooked)":        "/images/food/chicken-breast-cooked.jpg",
  "Rohu Fish":                      "/images/food/rohu-fish.jpg",
  "Tofu":                           "/images/food/tofu.jpeg",
  "Soybean (boiled)":               "/images/food/soybean-boiled.jpg",
  "Idli":                           "/images/food/idli.webp",
  "Dosa (plain)":                   "/images/food/dosa-plain.jpg",
  "Khichdi":                        "/images/food/khichdi.jpg",
  "Poha":                           "/images/food/poha.jpeg",
  "Upma":                           "/images/food/upma.webp",
  "Roasted Chana":                  "/images/food/roasted-chana.jpg",
  "Makhana (Fox Nut)":              "/images/food/makhana-fox-nut..jpeg",
  "Sprouts Salad":                  "/images/food/sprouts-salad.jpg",
  "Fruit Chaat":                    "/images/food/fruit-chaat.jpg",
  "Coconut Water":                  "/images/food/coconut-water.jpg",
  "Green Tea (unsweetened)":        "/images/food/green-tea-unsweetened.jpg",
  "Lemon Water (no sugar)":         "/images/food/lemon-water-no-sugar.jpeg",
  "Sugarcane Juice":                "/images/food/sugarcane-juice..avif",
  "Masala Chai (with milk & sugar)": "/images/food/masalachaiwithmilksugar.jpeg",
};

/** Returns the per-food-item image path if one exists, otherwise undefined. */
export const foodItemImage = (name) => FOOD_ITEM_IMAGES[name];

export const GALLERIES = {
  ahara: [
    { url: "/images/ahara-board.jpg", caption: "Whole foods across every category", alt: "Wooden board with sliced fruits, vegetables and nuts" },
    { url: "/images/ahara-pulses.jpg", caption: "Pulses — the protein backbone of Indian meals", alt: "Six piles of dried legumes arranged in a flower shape" },
    { url: "/images/ahara-peas.jpg", caption: "Split peas and chickpeas, side by side", alt: "Yellow split peas next to dried chickpeas" },
    { url: "/images/ahara-spices.jpg", caption: "Spices carry flavour, not calories", alt: "Steel masala box filled with coloured ground spices" },
    { url: "/images/ahara-spoons.jpg", caption: "Portion size decides the number on the label", alt: "Four small steel spoons holding different condiments" },
  ],
  manas: [
    { url: "/images/manas-deck.jpg", caption: "Attention rests when the surroundings are quiet", alt: "Woman sitting cross-legged on a wooden deck at sunrise" },
    { url: "/images/manas-calm.jpg", caption: "Calm is a condition you set up, not force", alt: "Stone statue surrounded by green leaves with the word calm" },
    { url: "/images/manas-rock.jpg", caption: "Time outdoors helps attention recover", alt: "Person seated on a rock formation in daylight" },
    { url: "/images/manas-night.jpg", caption: "Breathing practice needs no equipment", alt: "Person meditating in a park in low light" },
  ],
};

export const PILLARS = [
  {
    code: "ahara",
    accentText: "#B45309",
    index: "01",
    name: "AHARA",
    subtitle: "Food & Nutrition",
    blurb: "Learn about healthy foods, nutrients, calories and everyday nutrition.",
    path: "/ahara",
    accent: "#E07A5F",
    image: "/images/ahara-board.jpg",
  },
  {
    code: "jala",
    accentText: "#0369A1",
    index: "02",
    name: "JALA",
    subtitle: "Water & Water Knowledge",
    blurb: "Understand drinking water, groundwater, minerals, contamination and quality.",
    path: "/jala",
    accent: "#38BDF8",
    image: "/images/jala-borewell.jpg",
  },
  {
    code: "manas",
    accentText: "#047857",
    index: "03",
    name: "MANAS",
    subtitle: "Mind",
    blurb: "Brain and mind, thoughts, attention, memory, emotion and calmer states.",
    path: "/manas",
    accent: "#10B981",
    image: "/images/pillar-manas.jpg",
  },
];
