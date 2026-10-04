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
