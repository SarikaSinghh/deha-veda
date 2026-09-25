import { useEffect, useRef, useState } from "react";

const SKETCHFAB_UID =
  "c1518abfd4d64539b0cf093716e25d4c";

const SKETCHFAB_API =
  "https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js";

function loadSketchfabScript() {
  return new Promise((resolve, reject) => {
    // Script already loaded
    if (window.Sketchfab) {
      resolve(window.Sketchfab);
      return;
    }

    // Script is already being loaded
    const existingScript = document.querySelector(
      `script[src="${SKETCHFAB_API}"]`,
    );

    if (existingScript) {
      existingScript.addEventListener("load", () => {
        if (window.Sketchfab) {
          resolve(window.Sketchfab);
        } else {
          reject(
            new Error(
              "Sketchfab API loaded but was not found.",
            ),
          );
        }
      });

      existingScript.addEventListener("error", () => {
        reject(
          new Error(
            "Could not load the Sketchfab Viewer API.",
          ),
        );
      });

      return;
    }

    // Load Sketchfab API
    const script = document.createElement("script");

    script.src = SKETCHFAB_API;
    script.async = true;

    script.onload = () => {
      if (window.Sketchfab) {
        resolve(window.Sketchfab);
      } else {
        reject(
          new Error(
            "Sketchfab API loaded but was not found.",
          ),
        );
      }
    };

    script.onerror = () => {
      reject(
        new Error(
          "Could not load the Sketchfab Viewer API.",
        ),
      );
    };

    document.head.appendChild(script);
  });
}

export function SketchfabBrain() {
  const iframeRef = useRef(null);
  const apiRef = useRef(null);

  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function initializeViewer() {
      try {
        setStatus("loading");
        setError("");

        const Sketchfab = await loadSketchfabScript();

        if (cancelled || !iframeRef.current) {
          return;
        }

        const client = new Sketchfab(iframeRef.current);

        client.init(SKETCHFAB_UID, {
          autostart: 1,

          transparent: 0,

          ui_controls: 1,
          ui_infos: 0,
          ui_stop: 0,
          ui_watermark: 1,
          ui_watermark_link: 1,

          success: (api) => {
            if (cancelled) {
              return;
            }

            apiRef.current = api;

            api.start();

            api.addEventListener("viewerready", () => {
              if (cancelled) {
                return;
              }

              setStatus("ready");
            });
          },

          error: (apiError) => {
            console.error(
              "Sketchfab Viewer initialization error:",
              apiError,
            );

            if (!cancelled) {
              setStatus("error");

              setError(
                "The 3D brain could not be loaded. Please refresh the page and try again.",
              );
            }
          },
        });
      } catch (err) {
        console.error(
          "Sketchfab initialization failed:",
          err,
        );

        if (!cancelled) {
          setStatus("error");

          setError(
            err?.message ||
              "The Sketchfab viewer could not be initialized.",
          );
        }
      }
    }

    initializeViewer();

    return () => {
      cancelled = true;
      apiRef.current = null;
    };
  }, []);

  return (
    <div className="relative overflow-hidden rounded-[28px] border border-slate-200 bg-[#F6F5F1] shadow-sm">
      <div className="relative aspect-[4/3] min-h-[420px] w-full">
        <iframe
          ref={iframeRef}
          title="Interactive 3D Lobes of the Brain"
          className="absolute inset-0 h-full w-full border-0"
          allow="autoplay; fullscreen; xr-spatial-tracking"
          allowFullScreen
          sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
        />

        {status === "loading" && (
          <div className="pointer-events-none absolute inset-0 flex items-center justify-center bg-[#F6F5F1]/90">
            <div className="text-center">
              <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-slate-300 border-t-emerald-600" />

              <p className="mt-4 font-data text-[10px] uppercase tracking-[0.25em] text-slate-500">
                Loading brain model
              </p>
            </div>
          </div>
        )}

        {status === "error" && (
          <div className="absolute inset-0 flex items-center justify-center bg-[#F6F5F1] p-8">
            <div className="max-w-md text-center">
              <p className="font-display text-xl font-semibold text-slate-900">
                3D model unavailable
              </p>

              <p className="mt-3 text-sm leading-relaxed text-slate-600">
                {error}
              </p>

              <button
                type="button"
                onClick={() => window.location.reload()}
                className="mt-6 rounded-full bg-slate-900 px-5 py-2.5 text-xs font-semibold text-white transition hover:bg-slate-800"
              >
                Reload viewer
              </button>
            </div>
          </div>
        )}

        {status === "ready" && (
          <div className="pointer-events-none absolute left-4 top-4 rounded-full border border-white/70 bg-white/80 px-3 py-1.5 shadow-sm backdrop-blur">
            <span className="font-data text-[9px] uppercase tracking-[0.22em] text-slate-600">
              Interactive brain
            </span>
          </div>
        )}
      </div>

      <div className="border-t border-slate-200 bg-white/70 px-5 py-4">
        <p className="text-xs leading-relaxed text-slate-500">
          Drag to rotate · Scroll to zoom · Explore the brain
          in three dimensions
        </p>
      </div>
    </div>
  );
}