import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/context/AuthContext";
import { Seo } from "@/components/Seo";

export default function Auth({ mode }) {
  const isLogin = mode === "login";
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    const res = isLogin
      ? await login(form.email, form.password)
      : await register(form.name, form.email, form.password);
    setBusy(false);
    if (res.ok) navigate(res.user.role === "admin" ? "/admin" : "/profile");
    else setError(res.error);
  };

  return (
    <>
      <Seo
        title={isLogin ? "Login" : "Create account"}
        description="Access your Deha Veda Ecosystem account and explore food, water and mind."
        path={isLogin ? "/login" : "/register"}
      />
      <section className="dv-aurora flex min-h-[80vh] items-center justify-center px-4 py-16">
        <div className="dv-glass w-full max-w-md rounded-3xl p-8 sm:p-10">
          <p className="font-data mb-3 text-[10px] uppercase tracking-[0.28em] text-emerald-600">
            {isLogin ? "Welcome back" : "Join the ecosystem"}
          </p>
          <h1 className="font-display text-3xl font-bold tracking-tight text-slate-900">
            {isLogin ? "Log in" : "Create your free account"}
          </h1>

          <form onSubmit={submit} data-testid="auth-form" className="mt-8 space-y-4">
            {!isLogin && (
              <label className="block text-xs text-slate-600">
                Full name
                <Input data-testid="auth-name-input" value={form.name} onChange={set("name")} required minLength={2} className="mt-2 bg-white" />
              </label>
            )}
            <label className="block text-xs text-slate-600">
              Email
              <Input data-testid="auth-email-input" type="email" value={form.email} onChange={set("email")} required className="mt-2 bg-white" />
            </label>
            <label className="block text-xs text-slate-600">
              Password
              <Input
                data-testid="auth-password-input"
                type="password"
                value={form.password}
                onChange={set("password")}
                required
                minLength={isLogin ? 1 : 8}
                className="mt-2 bg-white"
              />
              {!isLogin && <span className="mt-1.5 block text-[10px] text-slate-400">At least 8 characters.</span>}
            </label>

            {error && (
              <p data-testid="auth-error" className="rounded-xl bg-red-500/10 px-4 py-3 text-xs text-red-600">
                {error}
              </p>
            )}

            <Button data-testid="auth-submit-button" type="submit" disabled={busy} className="w-full rounded-full bg-emerald-600 text-white hover:bg-emerald-700">
              {busy ? "Please wait…" : isLogin ? "Log in" : "Create account"}
            </Button>
          </form>

          <p className="mt-6 text-center text-xs text-slate-500">
            {isLogin ? "New here? " : "Already have an account? "}
            <Link
              data-testid="auth-switch-link"
              to={isLogin ? "/register" : "/login"}
              className="text-emerald-700 underline"
            >
              {isLogin ? "Create an account" : "Log in"}
            </Link>
          </p>
        </div>
      </section>
    </>
  );
}
