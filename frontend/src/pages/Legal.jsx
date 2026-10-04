import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { SectionHeading } from "@/components/States";
import { Seo } from "@/components/Seo";

const DOCS = {
  privacy: {
    title: "Privacy Policy",
    path: "/privacy",
    body: [
      ["What we collect", "When you create an account we store your name, email address and a bcrypt hash of your password. We never store your password in readable form. If you use the AI assistant we store the messages of that conversation so the assistant can follow context."],
      ["Cookies", "We set an httpOnly session cookie for authentication. We do not use advertising cookies."],
      ["Sharing", "We do not sell personal data. Messages you send to the AI assistant are processed by our AI provider in order to generate a reply."],
      ["Your choices", "You may request deletion of your account and associated data by writing to us through the contact page."],
    ],
  },
  terms: {
    title: "Terms of Use",
    path: "/terms",
    body: [
      ["Educational purpose only", "All content on Deha Veda Ecosystem is educational. It is not medical, dietary, psychological or laboratory advice, and it must not be used to diagnose or treat any condition. Always consult a qualified professional for personal health decisions."],
      ["Accuracy", "We reference WHO, BIS IS 10500:2012, USDA FoodData Central and comparable sources, and we correct errors when they are reported. Values are approximations that vary with serving size, variety, region and preparation."],
      ["Accounts", "You are responsible for keeping your login credentials safe and for the activity on your account. We may suspend accounts used for abuse, scraping or attempts to break platform security."],
      ["Changes", "We may update these terms as the platform grows. Continued use after an update means you accept the revised terms."],
    ],
  },
  notfound: {
    title: "Page not found",
    path: "/",
    body: [["We could not find that page", "The link may be out of date. Use the navigation above, or return to the homepage to explore the three pillars."]],
  },
};

export default function Legal({ doc }) {
  const d = DOCS[doc] || DOCS.notfound;
  return (
    <>
      <Seo title={d.title} description={`${d.title} for Deha Veda Ecosystem.`} path={d.path} />
      <section className="mx-auto max-w-3xl px-4 py-16 lg:px-8">
        <SectionHeading eyebrow="Legal" title={d.title} />
        <div className="mt-10 space-y-8">
          {d.body.map(([heading, text]) => (
            <div key={heading}>
              <h2 className="font-display text-xl font-semibold text-slate-900">{heading}</h2>
              <p className="mt-3 text-sm leading-relaxed text-slate-600">{text}</p>
            </div>
          ))}
        </div>
        {doc === "notfound" && (
          <Link to="/">
            <Button data-testid="notfound-home-button" className="mt-10 rounded-full bg-emerald-600 text-white">
              Back to homepage
            </Button>
          </Link>
        )}
      </section>
    </>
  );
}
