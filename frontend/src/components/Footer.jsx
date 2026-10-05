import { Link } from "react-router-dom";

const COLS = [
  {
    title: "Ecosystem",
    links: [
      ["Home", "/"],
      ["Ahara — Food", "/ahara"],
      ["Jala — Water", "/jala"],
      ["Manas — Mind", "/manas"],
    ],
  },
  {
    title: "Platform",
    links: [
      ["AI Assistant", "/#ai-assistant"],
      
      ["About", "/about"],
      ["Contact", "/contact"],
    ],
  },
  {
    title: "Legal",
    links: [
      ["Privacy Policy", "/privacy"],
      ["Terms of Use", "/terms"],
    ],
  },
];

export const Footer = () => (
  <footer className="relative mt-24 border-t border-slate-200 bg-[#F1F0EB]">
    <div className="mx-auto max-w-7xl px-4 py-14 lg:px-8">
      <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
        <div>
          <p className="font-display text-xl font-bold tracking-tight text-slate-900">DEHA VEDA ECOSYSTEM</p>
          <p className="font-data mt-2 text-[10px] uppercase tracking-[0.3em] text-emerald-600/80">
            Explore. Understand. Improve.
          </p>
          <p className="mt-5 max-w-xs text-sm leading-relaxed text-slate-500">
            An educational platform bringing food, water and mind into one interactive learning experience.
            Educational content only — not medical advice.
          </p>
        </div>
        {COLS.map((col) => (
          <div key={col.title}>
            <p className="font-data mb-4 text-[11px] uppercase tracking-[0.22em] text-slate-500">{col.title}</p>
            <ul className="space-y-2.5">
              {col.links.map(([label, path]) => (
                <li key={label}>
                  <Link
                    to={path}
                    data-testid={`footer-link-${label.toLowerCase().replace(/[^a-z]+/g, "-")}`}
                    className="dv-link-underline text-sm text-slate-600 transition-colors hover:text-emerald-700"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="dv-hairline my-10" />
      <div className="flex flex-col gap-3 text-xs text-slate-400 sm:flex-row sm:items-center sm:justify-between">
        <p>© {new Date().getFullYear()} Deha Veda Ecosystem. All rights reserved.</p>
        <p>
          Reference sources include WHO, BIS IS 10500:2012 and USDA FoodData Central.
        </p>
      </div>
    </div>
  </footer>
);
