import { lazy, Suspense, useEffect } from "react";
import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { AuthProvider } from "@/context/AuthContext";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { AIChat } from "@/components/AIChat";
import { Loading } from "@/components/States";
import { api } from "@/lib/api";
import Home from "@/pages/Home";

const Ahara = lazy(() => import("@/pages/Ahara"));
const Jala = lazy(() => import("@/pages/Jala"));
const Manas = lazy(() => import("@/pages/Manas"));
const About = lazy(() => import("@/pages/About"));
const Contact = lazy(() => import("@/pages/Contact"));
const Auth = lazy(() => import("@/pages/Auth"));
const Profile = lazy(() => import("@/pages/Profile"));
const Admin = lazy(() => import("@/pages/Admin"));
const Legal = lazy(() => import("@/pages/Legal"));


function RouteTracker() {
  const location = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
    api.post("/track", { path: location.pathname }).catch(() => {});
  }, [location.pathname]);
  return null;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-white">
          <RouteTracker />
          <Navbar />
          <main>
            <Suspense fallback={<div className="mx-auto max-w-7xl px-4 py-20"><Loading label="Loading section…" /></div>}>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/ahara" element={<Ahara />} />
                <Route path="/jala" element={<Jala />} />
                <Route path="/manas" element={<Manas />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/login" element={<Auth mode="login" />} />
                <Route path="/register" element={<Auth mode="register" />} />
                <Route path="/profile" element={<Profile />} />
               
                <Route path="/admin" element={<Admin />} />
                <Route path="/privacy" element={<Legal doc="privacy" />} />
                <Route path="/terms" element={<Legal doc="terms" />} />
                <Route path="*" element={<Legal doc="notfound" />} />
              </Routes>
            </Suspense>
          </main>
          <Footer />
          <AIChat />
          <Toaster position="top-center" />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
