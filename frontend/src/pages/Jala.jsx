import React, {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  AlertTriangle,
  Beaker,
  ChevronRight,
  CircleGauge,
  CloudRain,
  Droplets,
  FlaskConical,
  GlassWater,
  House,
  Mountain,
  ShieldCheck,
  Waves,
} from "lucide-react";

import { api, apiError } from "@/lib/api";

import {
  ErrorState,
  Loading,
  SectionHeading,
  Reveal,
} from "@/components/States";

import { Seo } from "@/components/Seo";

/* =========================================================
   WATER JOURNEY
========================================================= */

const JOURNEY_ASSETS = [
  {
    title: "Rain",
    subtitle: "Where the journey begins",
    image: "/images/jala-rain.mp4",
    icon: CloudRain,
  },
  {
    title: "Soil",
    subtitle: "Water meets the ground",
    image: "/images/jala-river.mp4",
    icon: Mountain,
  },
  {
    title: "Groundwater",
    subtitle: "A hidden underground journey",
    image: "/images/jala-well.jpg",
    icon: Droplets,
  },
  {
    title: "Collection",
    subtitle: "Water is drawn from its source",
    image: "/images/jala-borewell.jpg",
    icon: Waves,
  },
  {
    title: "Treatment",
    subtitle: "Water is prepared for use",
    image: "/images/jala-treatment.mp4",
    icon: FlaskConical,
  },
  {
    title: "Storage",
    subtitle: "Water waits before distribution",
    image: "/images/jala-storage.jpg",
    icon: CircleGauge,
  },
  {
    title: "Distribution",
    subtitle: "The journey moves toward us",
    image: "/images/jala-handpump.jpg",
    icon: Waves,
  },
  {
    title: "Home",
    subtitle: "Water enters everyday life",
    image: "/images/jala-home.jpeg",
    icon: House,
  },
  {
    title: "Drinking",
    subtitle: "The journey reaches the glass",
    image: "/images/jala-drinking.jpg",
    icon: GlassWater,
  },
];

/* =========================================================
   WATER TYPES
========================================================= */

const WATER_TYPES = [
  {
    title: "Drinking Water",
    image: "/images/jala/drinking-water.jpg",
    description:
      "Water intended for human consumption and everyday hydration.",
  },
  {
    title: "Groundwater",
    image: "/images/jala/groundwater..jpeg",
    description:
      "Water stored beneath the Earth's surface in soil and rock formations.",
  },
  {
    title: "Surface Water",
    image: "/images/jala/surface-water.jpeg",
    description:
      "Water found on the Earth's surface, including rivers, lakes and reservoirs.",
  },
  {
    title: "Rainwater",
    image: "/images/jala/rainwater.jpg",
    description:
      "Water collected directly from atmospheric precipitation.",
  },
  {
    title: "Mineral Water",
    image: "/images/jala/mineral-water.jpg",
    description:
      "Water containing naturally occurring dissolved minerals.",
  },
  {
    title: "Spring Water",
    image: "/images/jala/spring-water.jpg",
    description:
      "Groundwater that naturally emerges at the Earth's surface.",
  },
  {
    title: "Filtered Water",
    image: "/images/jala/filtered-water.webp",
    description:
      "Water passed through a filtration process to remove selected impurities.",
  },
  {
    title: "Purified Water",
    image: "/images/jala/purified-water.png",
    description:
      "Water treated through purification processes to reduce contaminants.",
  },
  {
    title: "RO Water",
    image: "/images/jala/ro-water.jpg",
    description:
      "Water treated using reverse osmosis to reduce dissolved substances.",
  },
  {
    title: "Distilled Water",
    image: "/images/jala/distilled-water.jpg",
    description:
      "Water purified through evaporation and condensation.",
  },
  {
    title: "Bottled Water",
    image: "/images/jala/bottled-water.png",
    description:
      "Water packaged for storage, transport and consumption.",
  },
];

/* =========================================================
   CONTAMINATION
========================================================= */

const CONTAMINATION_TYPES = [
  {
    title: "Biological Contamination",
    image: "/images/jala/biological-contamination.jpg",
    description:
      "Microorganisms such as bacteria, viruses and parasites can affect water quality.",
  },
  {
    title: "Chemical Contamination",
    image: "/images/jala/chemical-contamination.jpg",
    description:
      "Chemical substances can enter water through natural processes or human activity.",
  },
  {
    title: "Heavy Metals",
    image: "/images/jala/heavy-metals.webp",
    description:
      "Metals such as lead, arsenic and mercury can contaminate water sources.",
  },
  {
    title: "Agricultural Contamination",
    image: "/images/jala/agricultural-contamination.webp",
    description:
      "Fertilisers, pesticides and agricultural runoff can reach water systems.",
  },
  {
    title: "Industrial Contamination",
    image: "/images/jala/industrial-contamination.png",
    description:
      "Industrial activities can introduce chemicals and other pollutants into water.",
  },
  {
    title: "Microplastics and Emerging Contaminants",
    image: "/images/jala/microplastics.jpg",
    description:
      "Small plastic particles and emerging contaminants are increasingly studied in aquatic environments.",
  },
  {
    title: "Storage Contamination",
    image: "/images/jala/storage-contamination.jpg",
    description:
      "Poor storage conditions can introduce contaminants after water has been collected or treated.",
  },
];

/* =========================================================
   WATER QUALITY PARAMETERS
========================================================= */

const WATER_PARAMETERS = [
  {
    title: "pH",
    description:
      "A measure of how acidic or alkaline water is.",
    why:
      "pH affects taste, corrosion, scaling and the effectiveness of water treatment.",
    measured:
      "Measured using a calibrated pH meter or suitable indicator method.",
    high:
      "Alkaline water, possible taste changes and scaling tendency.",
    low:
      "Acidic water, greater corrosion tendency and possible metallic taste.",
    reference:
      "BIS IS 10500:2012 reference range: 6.5–8.5.",
  },
  {
    title: "TDS",
    description:
      "Total Dissolved Solids represent the concentration of dissolved substances in water.",
    why:
      "TDS can influence taste, scaling and the overall mineral character of water.",
    measured:
      "Measured using conductivity-based instruments or laboratory methods.",
    high:
      "May produce an undesirable taste and contribute to scaling.",
    low:
      "Very low dissolved mineral content may affect taste.",
    reference:
      "BIS IS 10500:2012: 500 mg/L acceptable; 2000 mg/L permissible in the absence of an alternate source.",
  },
  {
    title: "Total Hardness",
    description:
      "Hardness mainly reflects dissolved calcium and magnesium salts.",
    why:
      "Hardness influences scaling, soap consumption and water treatment requirements.",
    measured:
      "Usually measured through EDTA titration.",
    high:
      "Scaling, deposits and reduced soap efficiency.",
    low:
      "Very soft water may have different taste and corrosion characteristics.",
    reference:
      "BIS IS 10500:2012: 200 mg/L acceptable; 600 mg/L permissible as CaCO₃.",
  },
  {
    title: "Turbidity",
    description:
      "Turbidity indicates how much suspended material scatters light in water.",
    why:
      "High turbidity can affect appearance and may interfere with treatment and disinfection.",
    measured:
      "Measured using a nephelometric turbidity meter.",
    high:
      "Cloudy appearance and potentially greater treatment difficulty.",
    low:
      "Clearer water.",
    reference:
      "BIS IS 10500:2012 reference limit: 1 NTU acceptable; 5 NTU permissible.",
  },
  {
    title: "Chloride",
    description:
      "Chloride is a naturally occurring dissolved ion found in many water sources.",
    why:
      "High chloride concentrations can affect taste and contribute to corrosion.",
    measured:
      "Commonly measured using titration or instrumental laboratory methods.",
    high:
      "Salty taste and increased corrosion potential.",
    low:
      "Generally not a concern at ordinary concentrations.",
    reference:
      "BIS IS 10500:2012: 250 mg/L acceptable; 1000 mg/L permissible.",
  },
  {
    title: "Fluoride",
    description:
      "Fluoride occurs naturally in many groundwater sources.",
    why:
      "The concentration of fluoride matters because both deficiency and excess can have health implications.",
    measured:
      "Measured using ion-selective electrode or suitable analytical methods.",
    high:
      "Excessive long-term exposure can contribute to dental or skeletal fluorosis.",
    low:
      "Low fluoride does not provide the same exposure level as fluoridated water.",
    reference:
      "BIS IS 10500:2012: 1.0 mg/L acceptable; 1.5 mg/L permissible.",
  },
  {
    title: "Nitrate",
    description:
      "Nitrate is a nitrogen-containing compound that can occur naturally or enter water through human activities.",
    why:
      "Elevated nitrate can indicate contamination from agricultural or wastewater sources.",
    measured:
      "Measured using spectrophotometric, ion-selective or chromatographic methods.",
    high:
      "Elevated concentrations require attention, particularly for infants.",
    low:
      "Generally not a concern.",
    reference:
      "BIS IS 10500:2012: 45 mg/L maximum permissible limit.",
  },
  {
    title: "Iron",
    description:
      "Iron is a naturally occurring mineral that can dissolve into groundwater.",
    why:
      "Iron affects colour, taste, staining and can create deposits in plumbing.",
    measured:
      "Measured through laboratory colorimetric or instrumental methods.",
    high:
      "Metallic taste, staining and deposits.",
    low:
      "Generally not a concern.",
    reference:
      "BIS IS 10500:2012: 0.3 mg/L maximum permissible limit.",
  },
  {
    title: "Alkalinity",
    description:
      "The capacity of water to neutralise acid, mostly from bicarbonate and carbonate.",
    why:
      "Buffers pH swings and influences corrosion control and treatment chemistry.",
    measured:
      "Acid titration to defined pH endpoints.",
    high:
      "Bitter taste, scaling tendency.",
    low:
      "Poor pH buffering, water becomes corrosive more easily.",
    reference:
      "BIS IS 10500:2012: 200 mg/L acceptable; 600 mg/L permissible as CaCO₃.",
  },
  {
    title: "Microbial Contamination",
    description:
      "The presence of microorganisms in water that may indicate contamination.",
    why:
      "Microbiological safety is fundamental for drinking-water quality.",
    measured:
      "Laboratory microbiological analysis using established culture or analytical methods.",
    high:
      "May indicate contamination and require investigation and appropriate treatment.",
    low:
      "Absence of detected indicator organisms is the desired condition for drinking water.",
    reference:
      "Drinking-water microbiological requirements are assessed using established public-health standards.",
  },
];

/* =========================================================
   JOURNEY STAGE
========================================================= */

function JourneyStage({
  journey,
  index,
  active,
  onActivate,
}) {
  const [showInfo, setShowInfo] = useState(false);

  const asset =
    JOURNEY_ASSETS[index] ||
    JOURNEY_ASSETS[JOURNEY_ASSETS.length - 1];

  const Icon = asset.icon;

  const title = journey?.title || asset.title;

  const description =
    journey?.description ||
    journey?.details ||
    `This is stage ${index + 1} of the water journey.`;

  const risk =
    journey?.risk ||
    journey?.contamination ||
    journey?.warning ||
    "";

  const isVideo =
    typeof asset.image === "string" &&
    asset.image.toLowerCase().endsWith(".mp4");

  return (
    <article
      id={`journey-step-${index}`}
      data-testid={`journey-step-${index}`}
      className={[
        "relative min-h-[78vh] scroll-mt-24 py-8 transition-all duration-700 sm:min-h-[82vh] sm:py-12",
        active ? "opacity-100" : "opacity-[0.55]",
      ].join(" ")}
    >
      <div className="mx-auto flex h-full max-w-6xl items-center px-4 lg:px-8">
        <div className="grid w-full gap-6 lg:grid-cols-[110px_minmax(0,1fr)] lg:gap-8">

          {/* STEP NUMBER / ICON */}

          <div className="hidden lg:flex lg:flex-col lg:items-center lg:pt-8">
            <div
              className={[
                "flex h-16 w-16 items-center justify-center rounded-full border transition-all duration-500",
                active
                  ? "border-sky-300 bg-sky-50 text-sky-700 shadow-sm"
                  : "border-slate-200 bg-white text-slate-400",
              ].join(" ")}
            >
              <Icon
                size={25}
                strokeWidth={1.7}
              />
            </div>

            <div className="mt-4 font-data text-[10px] uppercase tracking-[0.25em] text-slate-400">
              {String(index + 1).padStart(2, "0")}
            </div>

            {index < JOURNEY_ASSETS.length - 1 && (
              <div className="mt-6 h-24 w-px bg-gradient-to-b from-slate-300 to-transparent" />
            )}
          </div>

          {/* MAIN STAGE */}

          <div
            className={[
              "relative overflow-hidden rounded-[2rem] border bg-white shadow-sm transition-all duration-700",
              active
                ? "border-slate-200 shadow-[0_25px_70px_rgba(15,23,42,0.10)]"
                : "border-slate-200/70",
            ].join(" ")}
          >

            {/* IMAGE / VIDEO */}

            <button
              type="button"
              onClick={() =>
                setShowInfo((value) => !value)
              }
              onFocus={() => onActivate(index)}
              className="group relative block w-full cursor-pointer text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 focus-visible:ring-offset-2"
              aria-expanded={showInfo}
              aria-label={`View information about ${title}`}
            >
              <div
                className={[
                  "relative aspect-[4/3] overflow-hidden bg-slate-100 transition-all duration-700 sm:aspect-[16/8]",
                  active
                    ? "scale-100"
                    : "scale-[0.99]",
                ].join(" ")}
              >
                {isVideo ? (
                  <video
                    className="h-full w-full object-cover"
                    autoPlay
                    muted
                    loop
                    playsInline
                    preload="metadata"
                    aria-label={`${title} water journey visual`}
                  >
                    <source
                      src={asset.image}
                      type="video/mp4"
                    />
                  </video>
                ) : (
                  <img
                    src={asset.image}
                    alt={`${title} stage of the water journey`}
                    className="h-full w-full object-cover transition duration-1000 group-hover:scale-[1.035]"
                  />
                )}

                {/* IMAGE OVERLAY */}

                <div className="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-slate-950/10 to-transparent" />

                {/* MOBILE STEP */}

                <div className="absolute left-4 top-4 flex items-center gap-2 rounded-full border border-white/30 bg-white/15 px-3 py-1.5 text-white backdrop-blur-md lg:hidden">
                  <Icon size={14} />

                  <span className="font-data text-[10px] uppercase tracking-[0.2em]">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                </div>

                {/* TOP RIGHT ACTION */}

                <div className="absolute right-4 top-4 rounded-full border border-white/30 bg-black/15 px-3 py-1.5 text-[10px] font-medium uppercase tracking-[0.16em] text-white backdrop-blur-md">
                  {showInfo ? "Close" : "Explore"}
                </div>

                {/* IMAGE TEXT */}

                <div className="absolute bottom-0 left-0 right-0 p-5 sm:p-8">
                  <div className="mb-2 flex items-center gap-2 text-white/75">
                    <Icon
                      size={16}
                      strokeWidth={1.7}
                    />

                    <span className="font-data text-[10px] uppercase tracking-[0.28em]">
                      {asset.subtitle}
                    </span>
                  </div>

                  <h3 className="font-display text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
                    {title}
                  </h3>

                  <p className="mt-3 max-w-xl text-sm leading-7 text-white/80 sm:text-base">
                    Click the image to understand this stage.
                  </p>
                </div>
              </div>
            </button>

            {/* INFORMATION PANEL */}

            <div
              className={[
                "grid transition-all duration-500 ease-out",
                showInfo
                  ? "grid-rows-[1fr] opacity-100"
                  : "grid-rows-[0fr] opacity-0",
              ].join(" ")}
            >
              <div className="overflow-hidden">
                <div
                  id={`journey-detail-${index}`}
                  data-testid="journey-detail"
                  className="border-t border-slate-200 bg-[#FAF9F5] p-5 sm:p-8"
                >
                  <div className="grid gap-7 lg:grid-cols-[1fr_280px]">

                    <div>
                      <p className="font-data text-[10px] uppercase tracking-[0.28em] text-sky-700">
                        Stage {String(index + 1).padStart(2, "0")}
                      </p>

                      <h4 className="mt-2 font-display text-2xl font-semibold text-slate-900 sm:text-3xl">
                        {title}
                      </h4>

                      <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
                        {description}
                      </p>
                    </div>

                    {risk && (
                      <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
                        <div className="flex items-center gap-2 text-amber-800">
                          <AlertTriangle size={17} />

                          <span className="font-data text-[10px] uppercase tracking-[0.2em]">
                            What to notice
                          </span>
                        </div>

                        <p className="mt-3 text-sm leading-6 text-amber-900/80">
                          {risk}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="mt-7 flex items-center justify-between border-t border-slate-200 pt-5">
                    <span className="text-xs text-slate-400">
                      {index < JOURNEY_ASSETS.length - 1
                        ? "Scroll to continue the journey"
                        : "The journey reaches the glass"}
                    </span>

                    <button
                      type="button"
                      onClick={() =>
                        setShowInfo(false)
                      }
                      className="text-xs font-medium text-slate-600 transition hover:text-slate-900"
                    >
                      Close information
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* NEXT STAGE HINT */}

            {index < JOURNEY_ASSETS.length - 1 && (
              <div className="flex items-center justify-center gap-2 border-t border-slate-100 px-4 py-3 text-slate-400">
                <span className="font-data text-[9px] uppercase tracking-[0.22em]">
                  Next stage
                </span>

                <ChevronRight size={13} />
              </div>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}

/* =========================================================
   JALA PAGE
========================================================= */

export default function Jala() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [step, setStep] = useState(0);
  const [selectedParameter, setSelectedParameter] =
    useState(0);

  const journeyRef = useRef(null);

  /* =======================================================
     LOAD JALA DATA
  ====================================================== */

  useEffect(() => {
    let mounted = true;

    async function loadJala() {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/jala");

        if (mounted) {
          setData(response.data);
        }
      } catch (err) {
        if (mounted) {
          setError(
            apiError(
              err,
              "Unable to load Jala."
            )
          );
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadJala();

    return () => {
      mounted = false;
    };
  }, []);

  /* =======================================================
     JOURNEY INTERSECTION OBSERVER
  ====================================================== */

  useEffect(() => {
  const node = journeyRef.current;

  if (!node) {
    return undefined;
  }

  const sections = node.querySelectorAll(
    "[data-journey-index]"
  );

  if (!sections.length) {
    return undefined;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort(
          (a, b) =>
            b.intersectionRatio - a.intersectionRatio
        );

      if (visible[0]) {
        const index = Number(
          visible[0].target.getAttribute(
            "data-journey-index"
          )
        );

        if (!Number.isNaN(index)) {
          setStep(index);
        }
      }
    },
    {
      root: null,
      rootMargin: "-20% 0px -20% 0px",
      threshold: [0.3, 0.5, 0.7],
    }
  );

  sections.forEach((section) =>
    observer.observe(section)
  );

  return () => observer.disconnect();
}, [data]);

  /* =======================================================
     LOADING / ERROR
  ====================================================== */

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  /* =======================================================
     DATA
  ====================================================== */

  const journey =
    Array.isArray(data?.journey) &&
    data.journey.length
      ? data.journey
      : JOURNEY_ASSETS;

  const activeParameter =
    WATER_PARAMETERS[selectedParameter] ||
    WATER_PARAMETERS[0];

  const localGallery = [
    {
      title: "Rain",
      image: "/images/jala-rain.mp4",
    },
    {
      title: "Groundwater",
      image: "/images/jala-well.jpg",
    },
    {
      title: "Treatment",
      image: "/images/jala-treatment.jpg",
    },
    {
      title: "Home",
      image: "/images/jala-home.jpeg",
    },
    {
      title: "Drinking",
      image: "/images/jala-drinking.jpg",
    },
  ];

  /* =======================================================
     RENDER
  ====================================================== */

  return (
    <>
      <Seo
        title="Jala — Water"
        description="Explore the journey, types, quality and contamination of water through Deha Veda."
      />

      <main className="overflow-hidden">

        {/* =================================================
            HERO
        ================================================== */}

        <header className="relative overflow-hidden border-b border-slate-200 bg-[#F7F6F1]">
          <div className="pointer-events-none absolute inset-0">

            <video
              className="h-full w-full object-cover opacity-20"
              autoPlay
              muted
              loop
              playsInline
              preload="metadata"
              aria-hidden="true"
            >
              <source
                src="/images/jala-water-flow.mp4"
                type="video/mp4"
              />
            </video>

            

            <div className="absolute inset-0 bg-gradient-to-r from-[#F7F6F1]/65 via-[#F7F6F1]/20 to-[#F7F6F1]/45" />
          </div>

          <div className="relative mx-auto max-w-7xl px-4 py-20 lg:px-8 lg:py-28">
            <div className="max-w-4xl">

              <p className="font-data mb-5 text-[11px] uppercase tracking-[0.3em] text-sky-700">
                02 — Jala
              </p>

              <h1 className="font-display max-w-4xl text-5xl font-bold tracking-tight text-slate-900 sm:text-6xl lg:text-7xl">
                What are we actually drinking?
              </h1>

              <p className="mt-7 max-w-2xl text-base leading-8 text-slate-600 sm:text-lg">
                Water is never just H₂O. It carries minerals,
                gases and sometimes contaminants picked up
                along its journey.
              </p>

              <div className="mt-10 flex flex-wrap gap-3">

                <div className="rounded-full border border-slate-200 bg-white/70 px-4 py-2 text-xs text-slate-600">
                  From rain
                </div>

                <div className="rounded-full border border-slate-200 bg-white/70 px-4 py-2 text-xs text-slate-600">
                  Through soil
                </div>

                <div className="rounded-full border border-slate-200 bg-white/70 px-4 py-2 text-xs text-slate-600">
                  Into the glass
                </div>

              </div>
            </div>
          </div>
        </header>

        {/* =================================================
            WHAT IS WATER
        ================================================== */}

        <section className="mx-auto max-w-7xl px-6 py-24 lg:px-10">

          <Reveal>
            <SectionHeading
              eyebrow="01 — Understanding water"
              title="What is water?"
              description="A simple molecule, but an enormous part of the systems that sustain life."
            />
          </Reveal>

          <div className="mt-14 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">

            <Reveal>
              <div className="overflow-hidden rounded-[2rem] bg-stone-100">
                <img
                  src="/images/jala/what-is-water.jpg"
                  alt="Water"
                  className="h-full min-h-[420px] w-full object-cover"
                />
              </div>
            </Reveal>

            <Reveal>
              <div className="flex h-full flex-col justify-center rounded-[2rem] bg-stone-100 p-8 md:p-12">

                <p className="text-lg leading-8 text-stone-600">
                  Water is a chemical compound made of hydrogen
                  and oxygen. Its movement through the environment
                  connects rainfall, soil, groundwater, rivers,
                  infrastructure, households and human health.
                </p>

                <div className="mt-10 grid gap-4 sm:grid-cols-2">

                  <div className="rounded-2xl bg-white p-5">
                    <Droplets
                      className="text-stone-500"
                      size={20}
                    />

                    <p className="mt-4 font-display text-xl">
                      H₂O
                    </p>

                    <p className="mt-1 text-sm text-stone-500">
                      Two hydrogen atoms and one oxygen atom.
                    </p>
                  </div>

                  <div className="rounded-2xl bg-white p-5">
                    <Waves
                      className="text-stone-500"
                      size={20}
                    />

                    <p className="mt-4 font-display text-xl">
                      A cycle
                    </p>

                    <p className="mt-1 text-sm text-stone-500">
                      Water continually moves through natural systems.
                    </p>
                  </div>

                </div>
              </div>
            </Reveal>

          </div>
        </section>

        {/* =================================================
            WATER TYPES
        ================================================== */}

        <section className="bg-[#e9e5dc]">

          <div className="mx-auto max-w-7xl px-6 py-24 lg:px-10">

            <Reveal>
              <SectionHeading
                eyebrow="02 — Water types"
                title="One word. Many forms."
                description="Water appears in different forms, sources and treatment states."
              />
            </Reveal>

            <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

              {WATER_TYPES.map(
                (water, index) => (
                  <Reveal key={water.title}>

                    <article className="group overflow-hidden rounded-[1.75rem] bg-white">

                      <div className="aspect-[4/3] overflow-hidden bg-stone-100">
                        <img
                          src={water.image}
                          alt={water.title}
                          className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                        />
                      </div>

                      <div className="p-6">

                        <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                          {String(index + 1).padStart(
                            2,
                            "0"
                          )}
                        </p>

                        <h3 className="mt-3 font-display text-2xl text-stone-900">
                          {water.title}
                        </h3>

                        <p className="mt-3 text-sm leading-6 text-stone-500">
                          {water.description}
                        </p>

                      </div>
                    </article>

                  </Reveal>
                )
              )}

            </div>
          </div>
        </section>

        {/* =================================================
            WATER JOURNEY
        ================================================== */}

        <section
          ref={journeyRef}
          className="mx-auto max-w-7xl px-6 py-24 lg:px-10"
        >

          <Reveal>
            <SectionHeading
              eyebrow="03 — The water journey"
              title="From rain to the glass."
              description="Follow the path water takes before it becomes part of everyday life."
            />
          </Reveal>

          <div className="mt-14 grid gap-10 lg:grid-cols-[0.28fr_0.72fr]">

            {/* JOURNEY NAVIGATION */}

            <div className="hidden lg:block">

              <div className="sticky top-28">

                <p className="font-data text-xs uppercase tracking-[0.2em] text-stone-400">
                  Journey
                </p>

                <div className="mt-6 space-y-3">

                  {journey.map((stage, index) => (
  <button
    key={`${stage.title}-${index}`}
    type="button"
    onClick={() => {
      setStep(index);

      const target =
        journeyRef.current?.querySelector(
          `[data-journey-index="${index}"]`
        );

      target?.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }}
    className={`block w-full rounded-xl px-4 py-3 text-left text-sm transition ${
      step === index
        ? "bg-stone-900 text-white"
        : "text-stone-500 hover:bg-stone-100"
    }`}
  >
    {String(index + 1).padStart(2, "0")} {stage.title}
  </button>
))}

                </div>
              </div>
            </div>

            {/* JOURNEY STAGES */}

            <div className="space-y-8">

              {journey.map(
                (stage, index) => (
                  <div
                    key={`${stage.title}-${index}`}
                    data-journey-index={index}
                  >
                    <JourneyStage
                      journey={stage}
                      index={index}
                      active={step === index}
                      onActivate={(stageIndex) =>
                        setStep(stageIndex)
                      }
                    />
                  </div>
                )
              )}

            </div>
          </div>
        </section>

        {/* =================================================
            WATER QUALITY
        ================================================== */}

        <section className="bg-[#e9e5dc]">

          <div className="mx-auto max-w-7xl px-6 py-24 lg:px-10">

            <Reveal>
              <SectionHeading
                eyebrow="04 — Water quality"
                title="Look inside the water"
                description="Water quality can be understood through measurable physical, chemical and microbiological parameters."
              />
            </Reveal>

            {/* PARAMETER NAVIGATION */}

            <Reveal>

              <div className="mt-12 flex flex-wrap gap-2">

                {WATER_PARAMETERS.map(
                  (parameter, index) => (
                    <button
                      key={parameter.title}
                      type="button"
                      onClick={() =>
                        setSelectedParameter(index)
                      }
                      className={`rounded-full border px-4 py-2 text-sm transition ${
                        selectedParameter === index
                          ? "border-stone-900 bg-stone-900 text-white"
                          : "border-stone-300 bg-white text-stone-600 hover:border-stone-500"
                      }`}
                    >
                      {parameter.title}
                    </button>
                  )
                )}

              </div>

            </Reveal>

            {/* SINGLE PARAMETER DETAIL */}

            <Reveal>

              <div className="mt-10 rounded-[2rem] bg-white p-8 md:p-12">

                <div className="flex items-start gap-5">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-stone-100">
                    <Beaker
                      size={21}
                      className="text-stone-600"
                    />
                  </div>

                  <div>

                    <p className="font-data text-xs uppercase tracking-[0.2em] text-stone-400">
                      Selected parameter
                    </p>

                    <h3 className="mt-2 font-display text-3xl text-stone-900 md:text-4xl">
                      {activeParameter.title}
                    </h3>

                  </div>
                </div>

                <div className="mt-10 grid gap-8 md:grid-cols-2">

                  <div>
                    <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                      What it means
                    </p>

                    <p className="mt-3 leading-7 text-stone-600">
                      {activeParameter.description}
                    </p>
                  </div>

                  <div>
                    <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                      Why it matters
                    </p>

                    <p className="mt-3 leading-7 text-stone-600">
                      {activeParameter.why}
                    </p>
                  </div>

                  <div>
                    <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                      How it is measured
                    </p>

                    <p className="mt-3 leading-7 text-stone-600">
                      {activeParameter.measured}
                    </p>
                  </div>

                  <div>
                    <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                      Reference
                    </p>

                    <p className="mt-3 leading-7 text-stone-600">
                      {activeParameter.reference}
                    </p>
                  </div>

                </div>

                <div className="mt-10 grid gap-4 md:grid-cols-2">

                  <div className="rounded-2xl bg-stone-50 p-5">

                    <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                      Higher values may indicate
                    </p>

                    <p className="mt-3 text-sm leading-6 text-stone-600">
                      {activeParameter.high}
                    </p>

                  </div>

                  <div className="rounded-2xl bg-stone-50 p-5">

                    <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                      Lower values may indicate
                    </p>

                    <p className="mt-3 text-sm leading-6 text-stone-600">
                      {activeParameter.low}
                    </p>

                  </div>

                </div>

              </div>

            </Reveal>
          </div>
        </section>

        {/* =================================================
            CONTAMINATION
        ================================================== */}

        <section className="mx-auto max-w-7xl px-6 py-24 lg:px-10">

          <Reveal>
            <SectionHeading
              eyebrow="05 — Contamination"
              title="What can interrupt the journey?"
              description="Water can encounter different forms of contamination before, during or after collection and treatment."
            />
          </Reveal>

          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {CONTAMINATION_TYPES.map(
              (item, index) => (
                <Reveal key={item.title}>

                  <article className="group overflow-hidden rounded-[1.75rem] border border-stone-200 bg-white">

                    <div className="aspect-[4/3] overflow-hidden bg-stone-100">

                      <img
                        src={item.image}
                        alt={item.title}
                        className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                      />

                    </div>

                    <div className="p-6">

                      <div className="flex items-center gap-3">

                        <AlertTriangle
                          size={18}
                          className="text-stone-500"
                        />

                        <p className="font-data text-xs uppercase tracking-[0.18em] text-stone-400">
                          {String(index + 1).padStart(
                            2,
                            "0"
                          )}
                        </p>

                      </div>

                      <h3 className="mt-4 font-display text-2xl text-stone-900">
                        {item.title}
                      </h3>

                      <p className="mt-3 text-sm leading-6 text-stone-500">
                        {item.description}
                      </p>

                    </div>
                  </article>

                </Reveal>
              )
            )}

          </div>
        </section>

        {/* =================================================
            GALLERY
        ================================================== */}

        <section className="bg-[#e9e5dc]">

          <div className="mx-auto max-w-7xl px-6 py-24 lg:px-10">

            <Reveal>
              <SectionHeading
                eyebrow="06 — Water in everyday life"
                title="A closer look"
                description="Different moments in the journey reveal how closely water is connected to everyday life."
              />
            </Reveal>

            <div className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-3">

              {localGallery.map(
                (item) => (
                  <Reveal key={item.title}>

                    <article className="group overflow-hidden rounded-[1.75rem] bg-white">

                      <div className="aspect-[4/3] overflow-hidden bg-stone-100">

                        {item.image
                          .toLowerCase()
                          .endsWith(".mp4") ? (
                          <video
                            className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                            autoPlay
                            muted
                            loop
                            playsInline
                            preload="metadata"
                          >
                            <source
                              src={item.image}
                              type="video/mp4"
                            />
                          </video>
                        ) : (
                          <img
                            src={item.image}
                            alt={item.title}
                            className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                          />
                        )}

                      </div>

                      <div className="p-5">

                        <h3 className="font-display text-xl text-stone-900">
                          {item.title}
                        </h3>

                      </div>

                    </article>

                  </Reveal>
                )
              )}

            </div>
          </div>
        </section>

        {/* =================================================
            CLOSING
        ================================================== */}

        <section className="mx-auto max-w-5xl px-6 py-32 text-center">

          <Reveal>

            <ShieldCheck
              size={34}
              strokeWidth={1.5}
              className="mx-auto text-stone-500"
            />

            <p className="mt-7 font-data text-xs uppercase tracking-[0.3em] text-stone-400">
              Deha Veda · Jala
            </p>

            <h2 className="mt-6 font-display text-5xl leading-tight text-stone-900 md:text-7xl">
              Know the water.
              <br />
              Understand the journey.
            </h2>

            <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-stone-500">
              Water reaches us through a long chain of natural,
              environmental and human systems. Understanding
              that journey helps us understand what we consume.
            </p>

          </Reveal>
        </section>

      </main>
    </>
  );
}