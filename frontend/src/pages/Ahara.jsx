import { useEffect, useMemo, useState } from "react";
import {
  Apple,
  Calculator,
  ChevronDown,
  Clock3,
  Flame,
  Leaf,
  Search,
  Sparkles,
  Utensils,
} from "lucide-react";

import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

import {
  api,
  apiError,
  GALLERIES,
  foodImage,
} from "../lib/api";


// =========================================================
// FOOD IMAGE
// =========================================================

function FoodImage({ name, category, imageUrl }) {
  const fallback = foodImage(category);

  return (
    <img
      src={imageUrl || fallback}
      alt={`${name} — ${category}`}
      loading="lazy"
      onError={(e) => {
        if (e.currentTarget.src !== fallback) {
          e.currentTarget.src = fallback;
        }
      }}
      className="h-full w-full object-cover transition-transform duration-700 hover:scale-105"
    />
  );
}


// =========================================================
// AHARA PAGE
// =========================================================

export default function Ahara() {
  const [foods, setFoods] = useState([]);
  const [categories, setCategories] = useState(["All"]);

  const [selectedCategory, setSelectedCategory] = useState("All");
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedFood, setSelectedFood] = useState(null);

  const [calorieForm, setCalorieForm] = useState({
    age: "",
    weight: "",
    height: "",
    gender: "female",
    activity: "moderate",
  });

  const [calorieResult, setCalorieResult] = useState(null);
  const [calorieLoading, setCalorieLoading] = useState(false);
  const [calorieError, setCalorieError] = useState("");

  // =======================================================
  // LOAD CATEGORIES
  // =======================================================

  useEffect(() => {
    let mounted = true;

    async function loadCategories() {
      try {
        const response = await api.get("/foods/categories");

        if (!mounted) return;

        const list = response.data?.categories || [];

        setCategories(["All", ...list]);
      } catch (err) {
        if (!mounted) return;

        setCategories(["All"]);
      }
    }

    loadCategories();

    return () => {
      mounted = false;
    };
  }, []);


  // =======================================================
  // LOAD FOODS
  // =======================================================

  useEffect(() => {
    let mounted = true;

    async function loadFoods() {
      setLoading(true);
      setError("");

      try {
        const response = await api.get("/foods", {
          params: {
            q: search.trim(),
            category:
              selectedCategory === "All"
                ? ""
                : selectedCategory,
          },
        });

        if (!mounted) return;

        setFoods(response.data?.items || []);
      } catch (err) {
        if (!mounted) return;

        setFoods([]);
        setError(
          apiError(
            err,
            "Unable to load food information."
          )
        );
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    const timer = setTimeout(loadFoods, 250);

    return () => {
      mounted = false;
      clearTimeout(timer);
    };
  }, [search, selectedCategory]);


  // =======================================================
  // FILTERED FOODS
  // =======================================================

  const visibleFoods = useMemo(() => {
    return foods;
  }, [foods]);


  // =======================================================
  // CALORIE CALCULATOR
  // =======================================================

  const handleCalorieChange = (field, value) => {
    setCalorieForm((previous) => ({
      ...previous,
      [field]: value,
    }));
  };


  async function calculateCalories(event) {
    event.preventDefault();

    setCalorieLoading(true);
    setCalorieError("");
    setCalorieResult(null);

    try {
      const response = await api.post(
        "/tools/calorie",
        {
          age: Number(calorieForm.age),
          weight: Number(calorieForm.weight),
          height: Number(calorieForm.height),
          gender: calorieForm.gender,
          activity: calorieForm.activity,
        }
      );

      setCalorieResult(response.data);
    } catch (err) {
      setCalorieError(
        apiError(
          err,
          "Unable to calculate calories."
        )
      );
    } finally {
      setCalorieLoading(false);
    }
  }


  // =======================================================
  // RENDER
  // =======================================================

  return (
    <div className="min-h-screen bg-background">

      {/* =================================================
          HERO
      ================================================= */}

      <section className="relative overflow-hidden border-b">

        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-background to-amber-50 dark:from-emerald-950/20 dark:via-background dark:to-amber-950/10" />

        <div className="relative mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">

          <div className="max-w-3xl">

            <div className="mb-5 inline-flex items-center gap-2 rounded-full border bg-background/80 px-4 py-2 text-sm font-medium backdrop-blur">

              <Leaf className="h-4 w-4 text-emerald-600" />

              Ahara • Nourishment

            </div>

            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">

              Food that supports
              <span className="text-emerald-600">
                {" "}your well-being.
              </span>

            </h1>

            <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">

              Explore nutritional information for everyday Indian foods
              and make more informed choices for your daily nourishment.

            </p>

          </div>

        </div>

      </section>


      {/* =================================================
          MAIN CONTENT
      ================================================= */}

      <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">

        {/* =================================================
            SEARCH + CATEGORIES
        ================================================= */}

        <section className="mb-10">

          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">

            {/* SEARCH */}

            <div className="relative w-full lg:max-w-md">

              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

              <Input
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
                placeholder="Search foods..."
                className="pl-10"
              />

            </div>


            {/* CATEGORY */}

            <div className="flex flex-wrap gap-2">

              {categories.map((category) => (

                <Button
                  key={category}
                  variant={
                    selectedCategory === category
                      ? "default"
                      : "outline"
                  }
                  size="sm"
                  onClick={() =>
                    setSelectedCategory(category)
                  }
                >
                  {category}
                </Button>

              ))}

            </div>

          </div>

        </section>


        {/* =================================================
            FOOD GRID
        ================================================= */}

        <section>

          <div className="mb-5 flex items-center justify-between">

            <div>

              <h2 className="text-2xl font-semibold">
                Explore foods
              </h2>

              <p className="mt-1 text-sm text-muted-foreground">
                {visibleFoods.length} foods available
              </p>

            </div>

            <div className="hidden items-center gap-2 text-sm text-muted-foreground sm:flex">

              <Apple className="h-4 w-4" />

              Nutritional guide

            </div>

          </div>


          {error && (
            <div className="mb-6 rounded-xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
              {error}
            </div>
          )}


          {loading ? (

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">

              {Array.from({ length: 8 }).map((_, index) => (

                <div
                  key={index}
                  className="overflow-hidden rounded-2xl border bg-card"
                >

                  <div className="aspect-[4/3] animate-pulse bg-muted" />

                  <div className="space-y-3 p-5">

                    <div className="h-5 w-2/3 animate-pulse rounded bg-muted" />

                    <div className="h-4 w-1/2 animate-pulse rounded bg-muted" />

                    <div className="h-4 w-full animate-pulse rounded bg-muted" />

                  </div>

                </div>

              ))}

            </div>

          ) : visibleFoods.length === 0 ? (

            <div className="rounded-2xl border bg-card p-12 text-center">

              <Utensils className="mx-auto h-10 w-10 text-muted-foreground" />

              <h3 className="mt-4 text-lg font-semibold">
                No foods found
              </h3>

              <p className="mt-2 text-sm text-muted-foreground">
                Try a different food name or category.
              </p>

            </div>

          ) : (

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">

              {visibleFoods.map((food) => (

                <article
                  key={food.id}
                  className="group overflow-hidden rounded-2xl border bg-card shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
                >

                  {/* IMAGE */}

                  <div className="relative aspect-[4/3] overflow-hidden bg-muted">

                    <FoodImage
                      name={food.name}
                      category={food.category}
                      imageUrl={food.image_url}
                    />


                    {/* CATEGORY */}

                    <div className="absolute left-3 top-3 rounded-full bg-background/90 px-3 py-1 text-xs font-medium shadow-sm backdrop-blur">

                      {food.category}

                    </div>


                    {/* PREMIUM */}

                    {food.premium && (

                      <div className="absolute right-3 top-3 inline-flex items-center gap-1 rounded-full bg-background/90 px-3 py-1 text-xs font-medium shadow-sm backdrop-blur">

                        <Sparkles className="h-3 w-3" />

                        Premium

                      </div>

                    )}

                  </div>


                  {/* CONTENT */}

                  <div className="p-5">

                    <div className="mb-3 flex items-start justify-between gap-3">

                      <h3 className="font-semibold leading-tight">
                        {food.name}
                      </h3>

                      {food.locked && (

                        <span className="shrink-0 text-xs text-muted-foreground">
                          Locked
                        </span>

                      )}

                    </div>


                    <div className="grid grid-cols-2 gap-2 text-xs">

                      <div className="rounded-lg bg-muted/60 p-2">

                        <div className="text-muted-foreground">
                          Calories
                        </div>

                        <div className="mt-1 font-semibold">
                          {food.calories ?? "—"} kcal
                        </div>

                      </div>


                      <div className="rounded-lg bg-muted/60 p-2">

                        <div className="text-muted-foreground">
                          Protein
                        </div>

                        <div className="mt-1 font-semibold">
                          {food.protein_g ?? "—"} g
                        </div>

                      </div>

                    </div>


                    {!food.locked && (

                      <Button
                        variant="ghost"
                        className="mt-4 w-full"
                        onClick={() =>
                          setSelectedFood(food)
                        }
                      >
                        View details
                      </Button>

                    )}

                  </div>

                </article>

              ))}

            </div>

          )}

        </section>


        {/* =================================================
            CALORIE CALCULATOR
        ================================================= */}

        <section className="mt-16">

          <div className="mb-6">

            <div className="mb-2 inline-flex items-center gap-2 rounded-full border bg-muted/40 px-3 py-1 text-xs font-medium">

              <Calculator className="h-3.5 w-3.5" />

              Personal tool

            </div>

            <h2 className="text-2xl font-semibold">
              Daily calorie calculator
            </h2>

            <p className="mt-1 text-sm text-muted-foreground">
              Estimate your daily calorie needs based on your profile.
            </p>

          </div>


          <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">

            {/* FORM */}

            <form
              onSubmit={calculateCalories}
              className="rounded-2xl border bg-card p-6 shadow-sm"
            >

              <div className="grid gap-5 sm:grid-cols-2">

                {/* AGE */}

                <div>

                  <label className="mb-2 block text-sm font-medium">
                    Age
                  </label>

                  <Input
                    type="number"
                    min="1"
                    value={calorieForm.age}
                    onChange={(event) =>
                      handleCalorieChange(
                        "age",
                        event.target.value
                      )
                    }
                    placeholder="Age"
                    required
                  />

                </div>


                {/* GENDER */}

                <div>

                  <label className="mb-2 block text-sm font-medium">
                    Gender
                  </label>

                  <select
                    value={calorieForm.gender}
                    onChange={(event) =>
                      handleCalorieChange(
                        "gender",
                        event.target.value
                      )
                    }
                    className="h-10 w-full rounded-md border bg-background px-3 text-sm"
                  >

                    <option value="female">
                      Female
                    </option>

                    <option value="male">
                      Male
                    </option>

                  </select>

                </div>


                {/* WEIGHT */}

                <div>

                  <label className="mb-2 block text-sm font-medium">
                    Weight (kg)
                  </label>

                  <Input
                    type="number"
                    min="1"
                    step="0.1"
                    value={calorieForm.weight}
                    onChange={(event) =>
                      handleCalorieChange(
                        "weight",
                        event.target.value
                      )
                    }
                    placeholder="Weight"
                    required
                  />

                </div>


                {/* HEIGHT */}

                <div>

                  <label className="mb-2 block text-sm font-medium">
                    Height (cm)
                  </label>

                  <Input
                    type="number"
                    min="1"
                    step="0.1"
                    value={calorieForm.height}
                    onChange={(event) =>
                      handleCalorieChange(
                        "height",
                        event.target.value
                      )
                    }
                    placeholder="Height"
                    required
                  />

                </div>


                {/* ACTIVITY */}

                <div className="sm:col-span-2">

                  <label className="mb-2 block text-sm font-medium">
                    Activity level
                  </label>

                  <select
                    value={calorieForm.activity}
                    onChange={(event) =>
                      handleCalorieChange(
                        "activity",
                        event.target.value
                      )
                    }
                    className="h-10 w-full rounded-md border bg-background px-3 text-sm"
                  >

                    <option value="sedentary">
                      Sedentary
                    </option>

                    <option value="light">
                      Lightly active
                    </option>

                    <option value="moderate">
                      Moderately active
                    </option>

                    <option value="active">
                      Very active
                    </option>

                    <option value="very_active">
                      Extremely active
                    </option>

                  </select>

                </div>

              </div>


              {calorieError && (

                <div className="mt-5 rounded-lg border border-destructive/30 bg-destructive/5 p-3 text-sm text-destructive">
                  {calorieError}
                </div>

              )}


              <Button
                type="submit"
                className="mt-6 w-full"
                disabled={calorieLoading}
              >

                <Calculator className="mr-2 h-4 w-4" />

                {calorieLoading
                  ? "Calculating..."
                  : "Calculate calories"}

              </Button>

            </form>


            {/* RESULT */}

            <div className="rounded-2xl border bg-gradient-to-br from-emerald-50 to-amber-50 p-6 dark:from-emerald-950/20 dark:to-amber-950/10">

              {calorieResult ? (

                <div>

                  <div className="mb-6 flex items-center gap-3">

                    <div className="rounded-xl bg-background p-3 shadow-sm">

                      <Flame className="h-6 w-6 text-orange-500" />

                    </div>

                    <div>

                      <h3 className="font-semibold">
                        Your estimate
                      </h3>

                      <p className="text-sm text-muted-foreground">
                        Daily energy requirement
                      </p>

                    </div>

                  </div>


                  <div className="rounded-2xl border bg-background/80 p-6 text-center">

                    <div className="text-4xl font-bold">
                      {calorieResult.calories ??
                        calorieResult.tdee ??
                        calorieResult.daily_calories ??
                        "—"}
                    </div>

                    <div className="mt-1 text-sm text-muted-foreground">
                      kcal / day
                    </div>

                  </div>


                  <p className="mt-5 text-sm leading-6 text-muted-foreground">
                    This is an estimate intended for general
                    informational use.
                  </p>

                </div>

              ) : (

                <div className="flex h-full min-h-[300px] flex-col items-center justify-center text-center">

                  <div className="rounded-2xl bg-background p-4 shadow-sm">

                    <Flame className="h-8 w-8 text-orange-500" />

                  </div>

                  <h3 className="mt-5 text-lg font-semibold">
                    Your calorie estimate will appear here
                  </h3>

                  <p className="mt-2 max-w-sm text-sm leading-6 text-muted-foreground">
                    Enter your details and activity level to
                    calculate an estimated daily requirement.
                  </p>

                </div>

              )}

            </div>

          </div>

        </section>


        {/* =================================================
            AHARA GALLERY
        ================================================= */}

        {GALLERIES?.ahara && (

          <section className="mt-16">

            <div className="mb-6">

              <div className="mb-2 inline-flex items-center gap-2 rounded-full border bg-muted/40 px-3 py-1 text-xs font-medium">

                <Sparkles className="h-3.5 w-3.5" />

                Ahara

              </div>

              <h2 className="text-2xl font-semibold">
                Nourishment in practice
              </h2>

            </div>


            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

              {GALLERIES.ahara.map((image, index) => {

                const imageSrc =
                  typeof image === "string"
                    ? image
                    : image?.url ||
                      image?.image ||
                      image?.src;

                return (

                  <div
                    key={index}
                    className="overflow-hidden rounded-2xl border bg-card"
                  >

                    <img
                      src={imageSrc}
                      alt={
                        typeof image === "object"
                          ? image?.alt || "Ahara"
                          : "Ahara"
                      }
                      loading="lazy"
                      className="aspect-[4/3] h-full w-full object-cover transition-transform duration-700 hover:scale-105"
                    />

                  </div>

                );

              })}

            </div>

          </section>

        )}

      </main>


      {/* =================================================
          FOOD DETAILS MODAL
      ================================================= */}

      {selectedFood && (

        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm"
          onClick={() => setSelectedFood(null)}
        >

          <div
            className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border bg-background shadow-2xl"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            {/* IMAGE */}

            <div className="relative aspect-[16/8] overflow-hidden">

              <FoodImage
                name={selectedFood.name}
                category={selectedFood.category}
                imageUrl={selectedFood.image_url}
              />

              <button
                type="button"
                onClick={() =>
                  setSelectedFood(null)
                }
                className="absolute right-4 top-4 rounded-full bg-background/90 px-3 py-2 text-sm font-medium shadow"
              >
                Close
              </button>

            </div>


            {/* DETAILS */}

            <div className="p-6">

              <div className="flex items-start justify-between gap-4">

                <div>

                  <div className="mb-2 text-xs font-medium text-emerald-600">
                    {selectedFood.category}
                  </div>

                  <h2 className="text-2xl font-bold">
                    {selectedFood.name}
                  </h2>

                </div>

                <div className="rounded-xl bg-muted px-3 py-2 text-center">

                  <div className="text-lg font-bold">
                    {selectedFood.calories ?? "—"}
                  </div>

                  <div className="text-xs text-muted-foreground">
                    kcal
                  </div>

                </div>

              </div>


              {/* MACROS */}

              <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">

                <div className="rounded-xl border p-4">

                  <div className="text-xs text-muted-foreground">
                    Protein
                  </div>

                  <div className="mt-1 font-semibold">
                    {selectedFood.protein_g ?? "—"} g
                  </div>

                </div>


                <div className="rounded-xl border p-4">

                  <div className="text-xs text-muted-foreground">
                    Carbs
                  </div>

                  <div className="mt-1 font-semibold">
                    {selectedFood.carbs_g ?? "—"} g
                  </div>

                </div>


                <div className="rounded-xl border p-4">

                  <div className="text-xs text-muted-foreground">
                    Fat
                  </div>

                  <div className="mt-1 font-semibold">
                    {selectedFood.fat_g ?? "—"} g
                  </div>

                </div>


                <div className="rounded-xl border p-4">

                  <div className="text-xs text-muted-foreground">
                    Fiber
                  </div>

                  <div className="mt-1 font-semibold">
                    {selectedFood.fiber_g ?? "—"} g
                  </div>

                </div>

              </div>


              {/* SERVING */}

              {selectedFood.serving_size && (

                <div className="mt-6 flex items-center gap-2 text-sm text-muted-foreground">

                  <Utensils className="h-4 w-4" />

                  Serving size:{" "}
                  <span className="font-medium text-foreground">
                    {selectedFood.serving_size}
                  </span>

                </div>

              )}


              {/* MICRONUTRIENTS */}

              {selectedFood.micronutrients && (

                <div className="mt-6">

                  <h3 className="font-semibold">
                    Micronutrients
                  </h3>

                  <p className="mt-2 leading-7 text-muted-foreground">
                    {selectedFood.micronutrients}
                  </p>

                </div>

              )}


              {/* NOTE */}

              {selectedFood.note && (

                <div className="mt-6 rounded-xl bg-muted/60 p-4">

                  <div className="mb-1 flex items-center gap-2 font-medium">

                    <Sparkles className="h-4 w-4" />

                    Deha Veda note

                  </div>

                  <p className="text-sm leading-6 text-muted-foreground">
                    {selectedFood.note}
                  </p>

                </div>

              )}

            </div>

          </div>

        </div>

      )}

    </div>
  );
}