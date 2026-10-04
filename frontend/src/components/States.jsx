import { useEffect, useRef, useState } from "react";
import { AlertTriangle, Loader2, Inbox } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Loading = ({ label = "Loading…", testid = "loading-state" }) => (
  <div data-testid={testid} className="flex items-center gap-3 py-14 text-slate-600">
    <Loader2 className="h-5 w-5 animate-spin text-emerald-600" />
    <span className="text-sm">{label}</span>
  </div>
);

export const ErrorState = ({ message, onRetry, testid = "error-state" }) => (
  <div data-testid={testid} className="dv-surface rounded-2xl p-8 text-center">
    <AlertTriangle className="mx-auto mb-3 h-7 w-7 text-amber-600" />
    <p className="text-sm text-slate-700">{message}</p>
    {onRetry && (
      <Button data-testid="retry-button" onClick={onRetry} variant="secondary" className="mt-5 rounded-full">
        Try again
      </Button>
    )}
  </div>
);

export const EmptyState = ({ message, testid = "empty-state" }) => (
  <div data-testid={testid} className="dv-surface rounded-2xl p-10 text-center">
    <Inbox className="mx-auto mb-3 h-7 w-7 text-slate-500" />
    <p className="text-sm text-slate-600">{message}</p>
  </div>
);

export function Reveal({ children, delay = 0, className = "" }) {
  const ref = useRef(null);
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return undefined;
    const obs = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setShown(true);
          obs.disconnect();
        }
      },
      { threshold: 0.12 },
    );
    obs.observe(node);
    return () => obs.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={className}
      style={{
        opacity: shown ? 1 : 0,
        transform: shown ? "none" : "translateY(24px)",
        transition: `opacity .7s cubic-bezier(.22,1,.36,1) ${delay}ms, transform .7s cubic-bezier(.22,1,.36,1) ${delay}ms`,
      }}
    >
      {children}
    </div>
  );
}

export function SectionHeading({ eyebrow, title, subtitle, id }) {
  return (
    <div id={id} className="max-w-3xl">
      {eyebrow && (
        <p className="font-data mb-3 text-xs uppercase tracking-[0.28em] text-emerald-600">{eyebrow}</p>
      )}
      <h2 className="font-display text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl lg:text-4xl">
        {title}
      </h2>
      {subtitle && <p className="mt-4 text-sm leading-relaxed text-slate-600 sm:text-base">{subtitle}</p>}
    </div>
  );
}
