import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogOut, User, ShieldCheck, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { Loading, SectionHeading } from "@/components/States";
import { Seo } from "@/components/Seo";

export default function Profile() {
  const { user, checking, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!checking && !user) navigate("/login");
  }, [checking, user, navigate]);

  if (checking || !user) return <div className="mx-auto max-w-7xl px-4 py-20"><Loading /></div>;

  return (
    <>
      <Seo title="My Profile" description="Your Deha Veda account." path="/profile" />
      <section className="mx-auto max-w-7xl px-4 py-16 lg:px-8">
        <SectionHeading eyebrow="My Account" title={user.name} subtitle={user.email} />

        <div className="mt-10 grid gap-5 sm:grid-cols-3">
          <div className="dv-surface rounded-2xl p-6">
            <User className="mb-4 h-5 w-5 text-emerald-600" />
            <p data-testid="profile-name" className="font-display text-xl text-slate-900">{user.name}</p>
            <p className="font-data mt-2 text-[10px] uppercase tracking-[0.16em] text-slate-500">Name</p>
          </div>
          <div className="dv-surface rounded-2xl p-6">
            <p data-testid="profile-email" className="font-display text-lg break-all text-slate-900">{user.email}</p>
            <p className="font-data mt-2 text-[10px] uppercase tracking-[0.16em] text-slate-500">Email</p>
          </div>
          <div className="dv-surface rounded-2xl p-6">
            <p data-testid="profile-role" className="font-display text-xl capitalize text-slate-900">{user.role}</p>
            <p className="font-data mt-2 text-[10px] uppercase tracking-[0.16em] text-slate-500">Account type</p>
          </div>
        </div>

        <div className="mt-8 dv-surface rounded-2xl p-6">
          <p className="font-data mb-4 text-[10px] uppercase tracking-[0.2em] text-slate-500">Quick links</p>
          <div className="flex flex-wrap gap-3">
            <Link to="/health">
              <Button size="sm" variant="secondary" className="rounded-full" data-testid="profile-health-link">
                <FileText className="mr-1.5 h-3.5 w-3.5" /> Health Reports
              </Button>
            </Link>
            {user.role === "admin" && (
              <Link to="/admin">
                <Button size="sm" className="rounded-full bg-sky-600 text-white" data-testid="profile-admin-link">
                  <ShieldCheck className="mr-1.5 h-3.5 w-3.5" /> Admin dashboard
                </Button>
              </Link>
            )}
            <Button
              size="sm"
              variant="ghost"
              data-testid="profile-logout-button"
              className="rounded-full text-slate-600"
              onClick={async () => {
                await logout();
                navigate("/");
              }}
            >
              <LogOut className="mr-1.5 h-3.5 w-3.5" /> Log out
            </Button>
          </div>
        </div>
      </section>
    </>
  );
}
