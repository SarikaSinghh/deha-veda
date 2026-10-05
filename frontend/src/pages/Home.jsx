import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowRight, Calculator, Droplets, Brain, Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { api, apiError, PILLARS } from "@/lib/api";
import { AutoCarousel } from "@/components/AutoCarousel";
import { Reveal, SectionHeading, ErrorState } from "@/components/States";
import { Seo } from "@/components/Seo";

const HIGHLIGHTS = [
  { icon: Calculator, title: "Calorie Calculator", text: "Estimate BMR and daily energy needs with the Mifflin-St Jeor equation.", to: "/ahara#calculator" },
  { icon: Droplets, title: "Water Knowledge", text: "Follow water from rain to your glass and read every quality parameter.", to: "/jala" },
  { icon: Brain, title: "3D Brain", text: "Rotate an interactive brain model and tap regions to learn what they do.", to: "/manas#brain" },
  { icon: Sparkles, title: "AI Assistant", text: "Ask questions about any of the three pillars and get plain-language answers.", to: "/#ai-assistant" },
];

const GALLERY = [
  { url: "/images/ahara-board.jpg", caption: "Ahara — whole foods across categories", alt: "Wooden board with sliced fruits, vegetables and nuts" },
  { url: "/images/jala-borewell.jpg", caption: "Jala — groundwater reaching the surface", alt: "Water gushing from a borewell pipe" },
  { url: "/images/manas-deck.jpg", caption: "Manas — attention, memory and calm", alt: "Woman sitting cross-legged on a wooden deck at sunrise" },
  { url: "/images/jala-treatment.jpg", caption: "Treatment — where water is made safe", alt: "Aerial view of a circular water treatment clarifier" },
];

function Counter({ value, testid }) {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    if (typeof value !== "number") return undefined;
    let raf;
    const start = performance.now();
    const tick = (t) => {
      const p = Math.min(1, (t - start) / 900);
      setShown(Math.round(value * (1 - (1 - p) ** 3)));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [value]);
  return (
    <span data-testid={testid} className="font-display text-4xl font-bold text-slate-900 sm:text-5xl">
      {shown.toLocaleString()}
    </span>
  );
}

export default function Home() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  const load = async () => {
    setError("");
    try {
      const { data } = await api.get("/stats/community");
      setStats(data);
    } catch (err) {
      setError(apiError(err, "Community information could not be loaded."));
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <>
      <Seo
        title="Explore. Understand. Improve."
        description="Deha Veda Ecosystem brings food, water and mind into one interactive educational platform."
        path="/"
      />

      {/* Hero */}
      <section className="dv-grain dv-aurora relative overflow-hidden border-b border-slate-200">
        <div className="relative mx-auto grid max-w-7xl gap-12 px-4 py-20 lg:grid-cols-12 lg:gap-8 lg:px-8 lg:py-28">
          <div className="dv-rise lg:col-span-7">
            <p className="font-data mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-600/8 px-3.5 py-1.5 text-[10px] uppercase tracking-[0.28em] text-emerald-700">
              Three Pillars · One Ecosystem
            </p>
            <h1 className="font-display text-4xl font-bold leading-[1.05] tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
              Explore three pillars of{" "}
              <span className="bg-gradient-to-r from-emerald-600 via-sky-600 to-purple-600 bg-clip-text text-transparent">
                Deha Veda
              </span>
            </h1>
            <p className="mt-3 font-data text-xs uppercase tracking-[0.35em] text-slate-500">
              Explore. Understand. Improve.
            </p>
            <p className="mt-7 max-w-xl text-sm leading-relaxed text-slate-600 sm:text-base">
              Explore food, water and mind through interactive experiences built on
              reliable sources — WHO, BIS drinking-water standards and USDA nutrition data.
            </p>
            <div className="mt-10 flex flex-wrap gap-3">
              <a href="#pillars">
                <Button data-testid="hero-explore-button" size="lg" className="rounded-full bg-emerald-600 px-7 text-white hover:bg-emerald-700">
                  Explore the Ecosystem <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </a>
              <Link to="/ahara">
                <Button data-testid="hero-learn-button" size="lg" variant="secondary" className="rounded-full px-7">
                  Start Learning
                </Button>
              </Link>
            </div>
          </div>

          <div className="dv-rise lg:col-span-5" style={{ animationDelay: "160ms" }}>
            <div className="relative overflow-hidden rounded-[28px] border border-slate-200">
              <img
                src="/images/hero-dv.jpg"
                alt="A woman in a green saree standing at a temple water tank at sunrise, representing the Deha Veda ecosystem"
                className="h-[280px] w-full object-cover sm:h-[420px]"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/55 via-transparent to-transparent" />
             
            </div>
          </div>
        </div>
      </section>

      {/* Three pillars */}
      <section id="pillars" className="mx-auto max-w-7xl px-4 py-20 lg:px-8 lg:py-28">
        <SectionHeading
          eyebrow="The Dashboard"
          title="Three pillars of the ecosystem"
          subtitle="Each pillar is a full learning space with its own tools, visuals and interactive experiences."
        />
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PILLARS.map((p, i) => (
            <Reveal key={p.code} delay={i * 80}>
              <Link
                to={p.path}
                data-testid={`pillar-card-${p.code}`}
                className="group relative flex h-full flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white transition-all duration-500 hover:-translate-y-1.5 hover:border-slate-300"
              >
                <div className="relative h-44 overflow-hidden">
                  <img
                    src={p.image}
                    alt={`${p.name} — ${p.subtitle}`}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-[1.07]"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-white/95 via-white/10 to-transparent" />
                  <span className="font-data absolute left-5 top-5 text-[11px] tracking-[0.3em]" style={{ color: p.accent }}>
                    {p.index}
                  </span>
                </div>
                <div className="flex flex-1 flex-col p-6">
                  <h3 className="font-display text-2xl font-bold tracking-tight text-slate-900">{p.name}</h3>
                  <p className="mt-1 text-xs font-semibold" style={{ color: p.accentText }}>
                    {p.subtitle}
                  </p>
                  <p className="mt-4 flex-1 text-sm leading-relaxed text-slate-600">{p.blurb}</p>
                  <span className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-slate-800 transition-colors group-hover:text-emerald-700">
                    Explore <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </span>
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Interactive highlights */}
      <section className="border-y border-slate-200 bg-[#F6F5F1]">
        <div className="mx-auto max-w-7xl px-4 py-20 lg:px-8">
          <SectionHeading
            eyebrow="Interactive Highlights"
            title="Tools you can actually use"
            subtitle="Nothing here is a static page. Every highlight is a working tool inside the ecosystem."
          />
          <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {HIGHLIGHTS.map((h, i) => (
              <Reveal key={h.title} delay={i * 60}>
                <Link
                  to={h.to}
                  data-testid={`highlight-${h.title.toLowerCase().replace(/\W+/g, "-")}`}
                  className="dv-surface group flex h-full flex-col rounded-2xl p-6 transition-colors hover:border-emerald-500/40"
                >
                  <h.icon className="mb-4 h-5 w-5 text-emerald-600" />
                  <p className="font-display text-lg font-semibold text-slate-900">{h.title}</p>
                  <p className="mt-2 text-sm leading-relaxed text-slate-600">{h.text}</p>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Community */}
      <section className="mx-auto max-w-7xl px-4 py-20 lg:px-8">
        <SectionHeading eyebrow="Growing Together" title="Our community, counted live" subtitle="These numbers are queried from the database on every visit." />
        {error ? (
          <div className="mt-10 max-w-lg">
            <ErrorState message={error} onRetry={load} />
          </div>
        ) : (
          <div className="mt-12 grid gap-5 sm:grid-cols-2">
            {[
  { label: "Foods Catalogued", key: "foods_catalogued", testid: "stat-foods", icon: Calculator },
].map((s, i) => (
              <Reveal key={s.key} delay={i * 70}>
                <div className="dv-surface rounded-2xl p-7">
                  <s.icon className="mb-5 h-5 w-5 text-emerald-600" />
                  {stats ? <Counter value={stats[s.key]} testid={s.testid} /> : <span className="font-display text-4xl text-slate-300">—</span>}
                  <p className="font-data mt-3 text-[10px] uppercase tracking-[0.2em] text-slate-500">{s.label}</p>
                </div>
              </Reveal>
            ))}
          </div>
        )}
      </section>

      {/* AI assistant */}
      <section id="ai-assistant" className="mx-auto max-w-7xl px-4 py-20 lg:px-8">
        <div className="dv-glass dv-grain relative overflow-hidden rounded-3xl p-8 sm:p-14">
          <Sparkles className="mb-6 h-6 w-6 text-emerald-600" />
          <h2 className="font-display max-w-2xl text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl lg:text-4xl">
            Ask Deha Veda AI anything about the three pillars
          </h2>
          <p className="mt-5 max-w-2xl text-sm leading-relaxed text-slate-600">
            The assistant explains nutrition figures, water-quality terms and mind topics in plain
            language. It is not a doctor and will always point you to a qualified professional for personal health
            questions.
          </p>
          <div className="mt-8 flex flex-wrap gap-2">
            {["How many calories are in an apple?", "What is groundwater?", "How can I improve my focus?"].map((q) => (
              <span key={q} className="font-data rounded-full border border-slate-300 px-3.5 py-2 text-[11px] text-slate-600">
                {q}
              </span>
            ))}
          </div>
          <p className="mt-8 text-xs text-slate-500">
            Open the assistant using the circular button at the bottom-right of any page.
          </p>
        </div>
      </section>

      {/* Gallery */}
      <section className="mx-auto max-w-7xl px-4 pb-24 lg:px-8">
        <SectionHeading eyebrow="Gallery" title="Visuals that explain, not decorate" />
        <div className="mt-10">
          <AutoCarousel slides={GALLERY} testid="home-gallery" />
        </div>
      </section>
    </>
  );
}
