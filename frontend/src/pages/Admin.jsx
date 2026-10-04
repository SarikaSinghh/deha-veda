import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart, Bar, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid, LineChart, Line,
} from "recharts";
import { Plus, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { api, apiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { ErrorState, Loading, SectionHeading } from "@/components/States";
import { Seo } from "@/components/Seo";

const COLORS = ["#10B981", "#38BDF8", "#A855F7", "#F59E0B", "#6366F1"];
const TABS = ["Overview", "Users", "Food Content", "Messages"];

export default function Admin() {
  const { user, checking } = useAuth();
  const navigate = useNavigate();
  const [tab, setTab] = useState("Overview");
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [newFood, setNewFood] = useState({
    name: "", category: "Fruits", calories: 0, protein_g: 0, carbs_g: 0, fat_g: 0, fiber_g: 0,
    micronutrients: "", note: "", serving_size: "100 g",
  });

  useEffect(() => {
    if (!checking && (!user || user.role !== "admin")) navigate("/login");
  }, [checking, user, navigate]);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [s, u, m] = await Promise.all([
        api.get("/admin/stats"),
        api.get("/admin/users"),
        api.get("/admin/contact"),
      ]);
      setStats(s.data);
      setUsers(u.data.users);
      setMessages(m.data.messages);
    } catch (err) {
      setError(apiError(err, "Admin data could not be loaded."));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.role === "admin") load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const addFood = async (e) => {
    e.preventDefault();
    try {
      await api.post("/admin/foods", {
        ...newFood,
        calories: Number(newFood.calories),
        protein_g: Number(newFood.protein_g),
        carbs_g: Number(newFood.carbs_g),
        fat_g: Number(newFood.fat_g),
        fiber_g: Number(newFood.fiber_g),
      });
      toast.success(`${newFood.name} added to the food database`);
      setNewFood({ ...newFood, name: "", micronutrients: "", note: "" });
      load();
    } catch (err) {
      toast.error(apiError(err));
    }
  };

  if (checking || !user || user.role !== "admin") {
    return <div className="mx-auto max-w-7xl px-4 py-20"><Loading label="Checking access…" /></div>;
  }

  return (
    <>
      <Seo title="Admin Dashboard" description="Administration for Deha Veda Ecosystem." path="/admin" />
      <section className="mx-auto max-w-7xl px-4 py-14 lg:px-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <SectionHeading eyebrow="Administration" title="Admin dashboard" />
          <Button data-testid="admin-refresh" size="sm" variant="secondary" className="rounded-full" onClick={load}>
            <RefreshCw className="mr-1.5 h-3.5 w-3.5" /> Refresh
          </Button>
        </div>

        <div className="mt-8 flex flex-wrap gap-2">
          {TABS.map((t) => (
            <button
              key={t}
              data-testid={`admin-tab-${t.toLowerCase().replace(/\W+/g, "-")}`}
              onClick={() => setTab(t)}
              className={`rounded-full border px-4 py-2 text-xs transition-colors ${
                tab === t ? "border-sky-500/60 bg-sky-500/12 text-sky-700" : "border-slate-200 text-slate-600 hover:text-slate-800"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {loading && <Loading label="Loading admin data…" />}
        {!loading && error && <div className="mt-8"><ErrorState message={error} onRetry={load} /></div>}

        {!loading && !error && stats && (
          <div className="mt-10">
            {tab === "Overview" && (
              <>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <Metric label="Total users" value={stats.total_users} testid="admin-total-users" />
                  <Metric label="New in 7 days" value={stats.new_registrations_7d} testid="admin-new-7d" />
                  <Metric label="AI messages" value={stats.ai_messages} testid="admin-ai-messages" />
                  <Metric label="Contact messages" value={stats.contact_messages} testid="admin-contact-count" />
                </div>

                <div className="mt-8 grid gap-5 lg:grid-cols-2">
                  <Panel title="Registrations, last 7 days" testid="chart-registrations">
                    <ResponsiveContainer width="100%" height={240}>
                      <LineChart data={stats.registrations_7d}>
                        <CartesianGrid stroke="#1e293b" vertical={false} />
                        <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
                        <YAxis stroke="#64748b" fontSize={11} allowDecimals={false} />
                        <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12 }} />
                        <Line type="monotone" dataKey="users" stroke="#10B981" strokeWidth={2.5} dot={{ r: 3 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Panel>

                  <Panel title="Popular pages" testid="popular-pages">
                    {stats.popular_pages.length === 0 ? (
                      <p className="py-16 text-center text-sm text-slate-500">No page views recorded yet.</p>
                    ) : (
                      <ul className="space-y-2">
                        {stats.popular_pages.map((p) => (
                          <li key={p.path} className="flex justify-between text-xs text-slate-600">
                            <span className="font-data">{p.path}</span>
                            <span>{p.views}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </Panel>
                </div>
              </>
            )}

            {tab === "Users" && (
              <Panel title={`Users (${users.length})`} testid="admin-users">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead className="text-slate-500">
                      <tr>
                        {["Name", "Email", "Role", "Joined"].map((h) => (
                          <th key={h} className="pb-3 pr-4 font-medium uppercase tracking-wider">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="text-slate-700">
                      {users.map((u) => (
                        <tr key={u.id} className="border-t border-slate-200">
                          <td className="py-3 pr-4">{u.name}</td>
                          <td className="py-3 pr-4">{u.email}</td>
                          <td className="py-3 pr-4">{u.role}</td>
                          <td className="py-3">{new Date(u.created_at).toLocaleDateString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Panel>
            )}

            {tab === "Food Content" && (
              <Panel title="Add a food entry" testid="admin-food-form">
                <form onSubmit={addFood} className="grid gap-4 sm:grid-cols-3">
                  {[
                    ["name", "Name", "text"],
                    ["category", "Category", "text"],
                    ["serving_size", "Serving size", "text"],
                    ["calories", "Calories", "number"],
                    ["protein_g", "Protein (g)", "number"],
                    ["carbs_g", "Carbs (g)", "number"],
                    ["fat_g", "Fat (g)", "number"],
                    ["fiber_g", "Fibre (g)", "number"],
                    ["micronutrients", "Micronutrients", "text"],
                  ].map(([key, label, type]) => (
                    <label key={key} className="text-xs text-slate-600">
                      {label}
                      <Input
                        data-testid={`food-input-${key}`}
                        type={type}
                        step="any"
                        value={newFood[key]}
                        onChange={(e) => setNewFood((f) => ({ ...f, [key]: e.target.value }))}
                        required={key === "name" || key === "category"}
                        className="mt-2 bg-white"
                      />
                    </label>
                  ))}
                  <label className="text-xs text-slate-600 sm:col-span-2">
                    Note
                    <Input
                      data-testid="food-input-note"
                      value={newFood.note}
                      onChange={(e) => setNewFood((f) => ({ ...f, note: e.target.value }))}
                      className="mt-2 bg-white"
                    />
                  </label>
                  <Button data-testid="food-add-submit" type="submit" className="rounded-full bg-emerald-600 text-white sm:col-span-3">
                    <Plus className="mr-1.5 h-4 w-4" /> Add food
                  </Button>
                </form>
              </Panel>
            )}

            {tab === "Messages" && (
              <Panel title={`Contact messages (${messages.length})`} testid="admin-messages">
                {messages.length === 0 ? (
                  <p className="py-10 text-center text-sm text-slate-500">No messages yet.</p>
                ) : (
                  <ul className="space-y-4">
                    {messages.map((m) => (
                      <li key={m.id} className="rounded-xl border border-slate-200 p-4">
                        <p className="text-sm font-semibold text-slate-900">{m.subject}</p>
                        <p className="font-data mt-1 text-[10px] text-slate-500">
                          {m.name} · {m.email} · {new Date(m.created_at).toLocaleString()}
                        </p>
                        <p className="mt-3 text-sm text-slate-600">{m.message}</p>
                      </li>
                    ))}
                  </ul>
                )}
              </Panel>
            )}
          </div>
        )}
      </section>
    </>
  );
}

function Metric({ label, value, testid }) {
  return (
    <div className="dv-surface rounded-2xl p-6">
      <p data-testid={testid} className="font-display text-3xl font-bold text-slate-900">{value}</p>
      <p className="font-data mt-2 text-[10px] uppercase tracking-[0.18em] text-slate-500">{label}</p>
    </div>
  );
}

function Panel({ title, children, testid }) {
  return (
    <div data-testid={testid} className="dv-surface rounded-3xl p-6">
      <p className="font-data mb-5 text-[10px] uppercase tracking-[0.2em] text-slate-500">{title}</p>
      {children}
    </div>
  );
}
