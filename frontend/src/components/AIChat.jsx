import { useEffect, useRef, useState } from "react";
import { MessageCircle, X, Send, Sparkles } from "lucide-react";
import { API, TOKEN_KEY } from "@/lib/api";

const SUGGESTIONS = [
  "How many calories are in an apple?",
  "What is groundwater?",
  "How can I improve my focus?",
  "What is the safe TDS level for drinking water?",
];

const GREETING = {
  role: "assistant",
  text:
    "Namaste. I am the Deha Veda AI Assistant. Ask me about food and nutrition, water and water quality, or the mind. I share general educational information only \u2014 not medical advice.",
};

export function AIChat() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([GREETING]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const sessionRef = useRef(
    localStorage.getItem("dv_chat_session") ||
      (() => {
        const id = `s_${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;
        localStorage.setItem("dv_chat_session", id);
        return id;
      })(),
  );
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, open]);

  const send = async (text) => {
    const question = (text ?? input).trim();
    if (!question || busy) return;
    setInput("");
    setError("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", text: question }, { role: "assistant", text: "" }]);

    try {
      const token = localStorage.getItem(TOKEN_KEY);
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        credentials: "include",
        body: JSON.stringify({ message: question, session_id: sessionRef.current }),
      });

      if (!res.ok) {
        let detail = "The assistant is unavailable right now.";
        try {
          const body = await res.json();
          if (typeof body.detail === "string") detail = body.detail;
        } catch {
          /* ignore */
        }
        setMessages((m) => m.slice(0, -1));
        setError(detail);
        setBusy(false);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let answer = "";

      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";
        for (const part of parts) {
          const line = part.trim();
          if (!line.startsWith("data:")) continue;
          try {
            const payload = JSON.parse(line.slice(5).trim());
            if (payload.delta) {
              answer += payload.delta;
              setMessages((m) => [...m.slice(0, -1), { role: "assistant", text: answer }]);
            } else if (payload.error) {
              setError(payload.error);
            }
          } catch {
            /* skip malformed chunk */
          }
        }
      }
      if (!answer) {
        setMessages((m) => m.slice(0, -1));
        setError("The assistant did not return an answer. Please try again.");
      }
    } catch (err) {
      setMessages((m) => m.slice(0, -1));
      setError("Network problem while contacting the assistant. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <button
        data-testid="ai-chat-toggle"
        aria-label="Open Deha Veda AI Assistant"
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-5 right-5 z-[60] flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-sky-500 text-white shadow-2xl shadow-emerald-500/25 transition-transform hover:scale-105 active:scale-95"
      >
        {open ? <X className="h-6 w-6" /> : <MessageCircle className="h-6 w-6" />}
      </button>

      {open && (
        <div
          data-testid="ai-chat-panel"
          className="dv-glass fixed bottom-24 right-3 z-[60] flex h-[70vh] w-[calc(100vw-1.5rem)] max-w-[400px] flex-col overflow-hidden rounded-3xl shadow-2xl sm:right-5"
        >
          <div className="flex items-center gap-3 border-b border-slate-300/60 px-5 py-4">
            <Sparkles className="h-4 w-4 text-emerald-600" />
            <div>
              <p className="font-display text-base font-semibold text-slate-900">Deha Veda AI Assistant</p>
              <p className="text-[10px] text-slate-500">Educational information, not medical advice</p>
            </div>
          </div>

          <div ref={scrollRef} data-testid="ai-chat-messages" className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
            {messages.map((m, i) => (
              <div
                key={i}
                data-testid={`ai-message-${m.role}-${i}`}
                className={`max-w-[88%] whitespace-pre-wrap rounded-2xl px-3.5 py-2.5 text-[13px] leading-relaxed ${
                  m.role === "user"
                    ? "ml-auto bg-emerald-600/15 text-emerald-900"
                    : "bg-slate-200/70 text-slate-800"
                }`}
              >
                {m.text || (busy && i === messages.length - 1 ? "…" : "")}
              </div>
            ))}
            {error && (
              <p data-testid="ai-chat-error" className="rounded-xl bg-red-500/10 px-3 py-2 text-xs text-red-600">
                {error}
              </p>
            )}
            {messages.length === 1 && (
              <div className="pt-2">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    data-testid={`ai-suggestion-${s.slice(0, 10).toLowerCase().replace(/\W+/g, "-")}`}
                    onClick={() => send(s)}
                    className="mb-2 mr-2 rounded-full border border-slate-300 px-3 py-1.5 text-[11px] text-slate-700 transition-colors hover:border-emerald-500/60 hover:text-emerald-700"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}
          </div>

          <form
            className="flex items-center gap-2 border-t border-slate-300/60 px-3 py-3"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              data-testid="ai-chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about food, water or mind…"
              className="flex-1 rounded-full border border-slate-300 bg-white px-4 py-2.5 text-[13px] text-slate-900 outline-none placeholder:text-slate-400 focus:ring-2 focus:ring-emerald-400"
            />
            <button
              data-testid="ai-chat-send"
              type="submit"
              disabled={busy}
              className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-600 text-white disabled:opacity-50"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
}
