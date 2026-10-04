import { useEffect, useState } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import { Menu, X, LogOut, User as UserIcon, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";

const LINKS = [
  { label: "Home", path: "/", testid: "nav-link-home" },
  { label: "Ahara", path: "/ahara", testid: "nav-link-ahara" },
  { label: "Jala", path: "/jala", testid: "nav-link-jala" },
  { label: "Manas", path: "/manas", testid: "nav-link-manas" },
  { label: "Health Reports", path: "/health", testid: "nav-link-health" },
  { label: "About", path: "/about", testid: "nav-link-about" },
  { label: "Contact", path: "/contact", testid: "nav-link-contact" },
];

export const Navbar = () => {
  const [open, setOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => setOpen(false), [location.pathname]);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 lg:px-8">
        <Link to="/" data-testid="brand-logo" className="flex items-center gap-3">
          <span className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-sky-500 font-display text-lg font-bold text-white">
            द
          </span>
          <span className="leading-none">
            <span className="font-display block text-[17px] font-bold tracking-tight text-slate-900">
              DEHA VEDA
            </span>
            <span className="font-data block text-[9px] uppercase tracking-[0.32em] text-emerald-600/80">
              Ecosystem
            </span>
          </span>
        </Link>

        <nav className="hidden items-center gap-1 xl:flex">
          {LINKS.map((l) => (
            <NavLink
              key={l.path}
              to={l.path}
              data-testid={l.testid}
              className={({ isActive }) =>
                `rounded-full px-3 py-2 text-[13px] font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-400 ${
                  isActive ? "bg-emerald-600/12 text-emerald-700" : "text-slate-600 hover:text-slate-900"
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          {user && user.role === "admin" && (
            <Link to="/admin" className="hidden sm:block">
              <Button data-testid="nav-admin-button" size="sm" variant="ghost" className="rounded-full text-sky-700">
                <ShieldCheck className="mr-1.5 h-4 w-4" /> Admin
              </Button>
            </Link>
          )}
          {user ? (
            <>
              <Link to="/profile">
                <Button data-testid="nav-profile-button" size="sm" variant="secondary" className="rounded-full">
                  <UserIcon className="mr-1.5 h-4 w-4" />
                  <span className="hidden sm:inline">{user.name?.split(" ")[0] || "Profile"}</span>
                </Button>
              </Link>
              <Button
                data-testid="nav-logout-button"
                size="sm"
                variant="ghost"
                className="rounded-full text-slate-600"
                onClick={async () => {
                  await logout();
                  navigate("/");
                }}
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </>
          ) : (
            <>
              <Link to="/login" className="hidden sm:block">
                <Button data-testid="nav-login-button" size="sm" variant="ghost" className="rounded-full text-slate-700">
                  Login
                </Button>
              </Link>
              <Link to="/register">
                <Button
                  data-testid="nav-cta-register"
                  size="sm"
                  className="rounded-full bg-emerald-600 text-white hover:bg-emerald-700"
                >
                  <span className="hidden sm:inline">Get started</span>
                  <span className="sm:hidden">Join</span>
                </Button>
              </Link>
            </>
          )}
          <button
            data-testid="mobile-menu-toggle"
            aria-label="Toggle navigation menu"
            className="rounded-lg p-2 text-slate-700 xl:hidden"
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {open && (
        <nav data-testid="mobile-nav-panel" className="border-t border-slate-200 bg-white px-4 py-3 xl:hidden">
          <div className="grid grid-cols-2 gap-1">
            {LINKS.map((l) => (
              <NavLink
                key={l.path}
                to={l.path}
                data-testid={`m-${l.testid}`}
                className="rounded-lg px-3 py-2.5 text-sm text-slate-700 hover:bg-slate-100"
              >
                {l.label}
              </NavLink>
            ))}
            {!user && (
              <NavLink to="/login" data-testid="m-nav-link-login" className="rounded-lg px-3 py-2.5 text-sm text-emerald-700">
                Login
              </NavLink>
            )}
            {user?.role === "admin" && (
              <NavLink to="/admin" data-testid="m-nav-link-admin" className="rounded-lg px-3 py-2.5 text-sm text-sky-700">
                Admin
              </NavLink>
            )}
          </div>
        </nav>
      )}
    </header>
  );
};
