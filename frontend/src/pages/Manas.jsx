import { Suspense, useEffect, useState } from "react";

import { SketchfabBrain } from "@/components/SketchfabBrain";

import {
  Brain,
  ChevronDown,
  ChevronRight,
  Focus,
  Heart,
  Info,
  Leaf,
  Moon,
  Sparkles,
  Wind,
} from "lucide-react";

import { api, apiError, GALLERIES } from "@/lib/api";
import { AutoCarousel } from "@/components/AutoCarousel";

import {
  ErrorState,
  Loading,
  SectionHeading,
  Reveal,
} from "@/components/States";

import { Seo } from "@/components/Seo";


const TOPIC_ICONS = [
  Focus,
  Sparkles,
  Brain,
  Heart,
  Focus,
  Sparkles,
  Wind,
  Leaf,
  Moon,
  Focus,
  Moon,
  Focus,
];


const TOPIC_IMAGES = [
  "/images/manas-what-is-mind.jpeg",
  "/images/manas-brain-vs-mind.jpg",
  "/images/manas-thoughts.webp",
  "/images/manas-attention.jpg",
  "/images/manas-memory.jpg",
  "/images/manas-emotions.jpeg",
  "/images/manas-perception.jpg",
  "/images/manas-habits.jpg",
  "/images/manas-stress.webp",
  "/images/manas-relaxation.webp",
  "/images/manas-sleep.jpeg",
  "/images/manas-focus.webp",
];


const PEACEFUL_IMAGES = [
  "/images/manas-calm.jpg",
  "/images/manas-deck.jpg",
  "/images/manas-night.jpg",
  "/images/manas-rock.jpg",
];


const PEACEFUL_ICONS = [
  Focus,
  Moon,
  Leaf,
  Wind,
  Sparkles,
  Leaf,
  Focus,
  Heart,
  Wind,
];


export default function Manas() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [expandedTopic, setExpandedTopic] = useState(null);
  const [selectedPeaceful, setSelectedPeaceful] = useState(0);


  const load = async () => {
    setLoading(true);
    setError("");

    try {
      const { data: d } = await api.get("/manas");

      setData(d);
    } catch (err) {
      setError(
        apiError(
          err,
          "Mind content could not be loaded. Please try again.",
        ),
      );
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    load();
  }, []);


  return (
    <>
      <Seo
        title="Manas — Mind"
        description="Explore the mind, brain regions, attention, memory, emotion, sleep and practices associated with a calmer mental state."
        path="/manas"
      />


      {/* =========================================================
          HERO
      ========================================================= */}

      <header className="relative overflow-hidden border-b border-slate-200 bg-[#F7F5EF]">
        <div className="absolute -right-32 -top-32 h-96 w-96 rounded-full bg-emerald-200/20 blur-3xl" />

        <div className="absolute -bottom-40 left-1/3 h-96 w-96 rounded-full bg-sky-200/20 blur-3xl" />

        <div className="relative mx-auto grid max-w-7xl gap-12 px-4 py-16 lg:grid-cols-12 lg:px-8 lg:py-24">
          <div className="flex flex-col justify-center lg:col-span-7">
            <p className="font-data mb-5 text-[11px] uppercase tracking-[0.3em] text-emerald-700">
              04 — Manas
            </p>

            <h1 className="font-display max-w-3xl text-5xl font-bold leading-[0.95] tracking-tight text-slate-900 sm:text-6xl lg:text-7xl">
              The mind,
              <br />
              <span className="text-emerald-700">
                explored.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
              The brain is an organ. The mind is the set of
              functions we experience through it. Explore
              attention, memory, emotions, perception, habits,
              sleep and the brain regions associated with them.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <a
                href="#foundations"
                className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 text-sm font-medium text-white transition hover:-translate-y-0.5 hover:bg-slate-800"
              >
                Begin exploring
                <ChevronRight className="h-4 w-4" />
              </a>

              <span className="inline-flex items-center rounded-full border border-slate-300 bg-white/70 px-5 py-3 text-sm text-slate-600">
                Brain · Mind · Attention · Emotion
              </span>
            </div>
          </div>


          <div className="relative lg:col-span-5">
            <div className="relative overflow-hidden rounded-[2rem] border border-white/70 bg-white/60 p-2 shadow-xl shadow-slate-900/10">
              <img
                src="/images/pillar-manas.jpg"
                alt="Illustration representing the human brain and mind"
                className="h-[360px] w-full rounded-[1.5rem] object-cover sm:h-[430px]"
              />

              <div className="absolute bottom-7 left-7 right-7 rounded-2xl border border-white/40 bg-white/80 p-4 backdrop-blur-md">
                <p className="font-data text-[10px] uppercase tracking-[0.25em] text-emerald-700">
                  MANAS
                </p>

                <p className="mt-1 font-display text-lg font-semibold text-slate-900">
                  Understanding what happens within
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>


      {loading && (
        <div className="mx-auto max-w-7xl px-4 lg:px-8">
          <Loading label="Loading mind content…" />
        </div>
      )}


      {!loading && error && (
        <div className="mx-auto max-w-2xl px-4 py-16">
          <ErrorState message={error} onRetry={load} />
        </div>
      )}


      {!loading && data && (
        <>
          {/* =========================================================
              FOUNDATIONS
          ========================================================= */}

          <section
            id="foundations"
            className="mx-auto max-w-7xl px-4 py-20 lg:px-8"
          >
            <SectionHeading
              eyebrow="Foundations"
              title="How the mind is described"
              subtitle="Start with the building blocks of attention, thought, memory, emotion and behaviour."
            />

            <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {data.topics.map((topic, index) => {
                const Icon =
                  TOPIC_ICONS[index % TOPIC_ICONS.length];

                const image =
                  TOPIC_IMAGES[index % TOPIC_IMAGES.length];

                const expanded =
                  expandedTopic === index;

                return (
                  <Reveal
                    key={topic.title}
                    delay={Math.min(index, 8) * 40}
                  >
                    <article
                      data-testid={`manas-topic-${index}`}
                      className={`group h-full overflow-hidden rounded-[1.5rem] border bg-white shadow-sm transition-all duration-300 ${
                        expanded
                          ? "border-emerald-400 shadow-xl shadow-emerald-900/10"
                          : "border-slate-200 hover:-translate-y-1 hover:border-emerald-200 hover:shadow-lg"
                      }`}
                    >
                      <div className="relative h-48 overflow-hidden">
                        <img
                          src={image}
                          alt=""
                          className="h-full w-full object-cover transition duration-700 group-hover:scale-105"
                        />

                        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/65 via-transparent to-transparent" />

                        <div className="absolute left-5 top-5 flex h-10 w-10 items-center justify-center rounded-xl border border-white/30 bg-white/80 text-emerald-700 backdrop-blur-md">
                          <Icon className="h-5 w-5" />
                        </div>

                        <span className="absolute bottom-4 left-5 font-data text-[10px] uppercase tracking-[0.25em] text-white/80">
                          0{index + 1}
                        </span>
                      </div>


                      <div className="p-6">
                        <h3 className="font-display text-xl font-semibold text-slate-900">
                          {topic.title}
                        </h3>

                        <p
                          className={`mt-3 text-sm leading-6 text-slate-600 ${
                            expanded ? "" : "line-clamp-3"
                          }`}
                        >
                          {topic.detail}
                        </p>

                        <button
                          type="button"
                          onClick={() =>
                            setExpandedTopic(
                              expanded ? null : index,
                            )
                          }
                          className="mt-5 inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.15em] text-emerald-700"
                          aria-expanded={expanded}
                        >
                          {expanded ? "Show less" : "Explore"}

                          <ChevronDown
                            className={`h-4 w-4 transition-transform ${
                              expanded ? "rotate-180" : ""
                            }`}
                          />
                        </button>
                      </div>
                    </article>
                  </Reveal>
                );
              })}
            </div>
          </section>


          {/* =========================================================
              INTERACTIVE BRAIN
          ========================================================= */}

          <section
            id="brain"
            className="relative overflow-hidden border-y border-slate-800 bg-[#121615] text-white"
          >
            <div className="pointer-events-none absolute left-1/2 top-0 h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-emerald-500/10 blur-[120px]" />

            <div className="relative mx-auto max-w-7xl px-4 py-20 lg:px-8">
              <div className="max-w-3xl">
                <p className="font-data text-[11px] uppercase tracking-[0.3em] text-emerald-400">
                  Interactive brain
                </p>

                <h2 className="font-display mt-3 text-4xl font-bold tracking-tight sm:text-5xl">
                  Meet the regions behind the experience.
                </h2>

                <p className="mt-5 text-sm leading-7 text-slate-400 sm:text-base">
                  Rotate the model, zoom in, and explore the
                  major regions of the brain through an
                  interactive 3D view.
                </p>
              </div>


              <div className="mt-12 grid gap-8 lg:grid-cols-12">

                {/* =================================================
                    3D MODEL
                ================================================= */}

                <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-[#171d1b] shadow-2xl lg:col-span-7">
                  <div className="absolute left-6 top-6 z-10 rounded-full border border-white/10 bg-black/30 px-4 py-2 text-[10px] uppercase tracking-[0.2em] text-slate-300 backdrop-blur-md">
                    Interactive 3D
                  </div>

                  <Suspense
                    fallback={
                      <div className="flex h-[520px] items-center justify-center">
                        <Loading label="Loading 3D brain…" />
                      </div>
                    }
                  >
                    <SketchfabBrain />
                  </Suspense>

                  <div className="absolute bottom-5 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-full border border-white/10 bg-black/40 px-4 py-2 text-[10px] text-slate-400 backdrop-blur-md">
                    Drag to rotate · Scroll to zoom · Explore the brain
                  </div>
                </div>


                {/* =================================================
                    BRAIN EXPLORATION GUIDE
                ================================================= */}

                <div className="lg:col-span-5">
                  <div className="rounded-[2rem] border border-white/10 bg-white/[0.04] p-7 shadow-xl">
                    <p className="font-data text-[10px] uppercase tracking-[0.25em] text-emerald-400">
                      Explore the brain
                    </p>

                    <h3 className="font-display mt-4 text-3xl font-bold">
                      A map of the mind
                    </h3>

                    <p className="mt-5 text-sm leading-7 text-slate-400">
                      The brain is made up of interconnected
                      regions that work together rather than
                      functioning as isolated compartments.
                      This model offers a visual introduction
                      to some of its major anatomical regions.
                    </p>


                    <div className="mt-7 space-y-4">

                      <div className="border-t border-white/10 pt-4">
                        <p className="font-display text-sm font-semibold text-white">
                          Frontal Lobe
                        </p>

                        <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
                          Associated with planning, reasoning,
                          decision-making, voluntary movement
                          and aspects of behaviour.
                        </p>
                      </div>


                      <div className="border-t border-white/10 pt-4">
                        <p className="font-display text-sm font-semibold text-white">
                          Parietal Lobe
                        </p>

                        <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
                          Helps process touch, body position,
                          spatial information and aspects of
                          attention.
                        </p>
                      </div>


                      <div className="border-t border-white/10 pt-4">
                        <p className="font-display text-sm font-semibold text-white">
                          Temporal Lobe
                        </p>

                        <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
                          Involved in auditory processing,
                          language-related functions, memory
                          and aspects of emotional processing.
                        </p>
                      </div>


                      <div className="border-t border-white/10 pt-4">
                        <p className="font-display text-sm font-semibold text-white">
                          Occipital Lobe
                        </p>

                        <p className="mt-1.5 text-xs leading-relaxed text-slate-400">
                          Primarily involved in processing and
                          interpreting visual information.
                        </p>
                      </div>
                    </div>
                  </div>


                  {/* HOW TO EXPLORE */}

                  <div className="mt-5 rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                    <p className="font-data text-[9px] uppercase tracking-[0.22em] text-slate-500">
                      How to explore
                    </p>

                    <div className="mt-4 grid grid-cols-3 gap-3 text-center">

                      <div>
                        <div className="font-display text-lg font-semibold text-white">
                          01
                        </div>

                        <p className="mt-1 text-[11px] leading-relaxed text-slate-500">
                          Drag to rotate
                        </p>
                      </div>


                      <div>
                        <div className="font-display text-lg font-semibold text-white">
                          02
                        </div>

                        <p className="mt-1 text-[11px] leading-relaxed text-slate-500">
                          Scroll to zoom
                        </p>
                      </div>


                      <div>
                        <div className="font-display text-lg font-semibold text-white">
                          03
                        </div>

                        <p className="mt-1 text-[11px] leading-relaxed text-slate-500">
                          Inspect the regions
                        </p>
                      </div>

                    </div>
                  </div>


                  {/* EDUCATIONAL NOTE */}

                  <div className="mt-5 flex gap-3 rounded-2xl border border-sky-400/10 bg-sky-400/5 p-5 text-xs leading-6 text-sky-200/80">
                    <Info className="mt-0.5 h-4 w-4 shrink-0 text-sky-300" />

                    <span>{data.note}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>


          {/* =========================================================
              PEACEFUL MIND
          ========================================================= */}

          <section className="mx-auto max-w-7xl px-4 py-20 lg:px-8">
            <SectionHeading
              eyebrow="Peaceful Mind"
              title="What contributes to a calmer mental state"
              subtitle="General wellbeing factors associated with mental wellbeing. They are not treatments and do not replace professional care."
            />

            <div className="mt-12 grid gap-8 lg:grid-cols-12">

              <div className="relative overflow-hidden rounded-[2rem] lg:col-span-5">
                <img
                  src={
                    PEACEFUL_IMAGES[
                      selectedPeaceful %
                        PEACEFUL_IMAGES.length
                    ]
                  }
                  alt="Peaceful mindfulness practice"
                  className="h-full min-h-[480px] w-full object-cover transition-all duration-700"
                />

                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

                <div className="absolute bottom-7 left-7 right-7">
                  <p className="font-data text-[10px] uppercase tracking-[0.25em] text-white/70">
                    A quieter mind
                  </p>

                  <p className="font-display mt-2 text-2xl font-semibold text-white">
                    Small conditions can shape the way we
                    experience a day.
                  </p>
                </div>
              </div>


              <div className="grid gap-3 sm:grid-cols-2 lg:col-span-7">
                {data.peaceful_mind.map((item, index) => {
                  const Icon =
                    PEACEFUL_ICONS[
                      index % PEACEFUL_ICONS.length
                    ];

                  const selected =
                    selectedPeaceful === index;

                  return (
                    <Reveal
                      key={item.title}
                      delay={Math.min(index, 8) * 40}
                    >
                      <button
                        type="button"
                        onClick={() =>
                          setSelectedPeaceful(index)
                        }
                        className={`h-full w-full rounded-2xl border p-5 text-left transition-all ${
                          selected
                            ? "border-emerald-300 bg-emerald-50 shadow-md"
                            : "border-slate-200 bg-white hover:border-emerald-200 hover:shadow-sm"
                        }`}
                      >
                        <Icon
                          className={`mb-4 h-5 w-5 ${
                            selected
                              ? "text-emerald-700"
                              : "text-emerald-600"
                          }`}
                        />

                        <h3 className="font-display text-lg font-semibold text-slate-900">
                          {item.title}
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-600">
                          {item.detail}
                        </p>
                      </button>
                    </Reveal>
                  );
                })}
              </div>
            </div>


            <div className="mt-14">
              <AutoCarousel
                slides={GALLERIES.manas}
                testid="manas-gallery"
                interval={6500}
              />
            </div>
          </section>
        </>
      )}
    </>
  );
}