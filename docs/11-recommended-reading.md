<img src="images/four-audiences.png" alt="Recommended reading organized by seat: board, C-suite, leadership, the firm" width="100%">

# Recommended reading

**The sources behind this guide, curated by seat. Not a bibliography to admire — a short, annotated list where every entry earns its place, tagged with who should read it and why.**

There is an enormous amount written about AI. Most of it is either too technical for a board or too breathless for a practitioner. What follows is a deliberately short list, chosen because each item changes how a specific person at the firm should think or act. Each entry says *who it's for* and *why it's here.* Read the two or three that match your seat before you read broadly. All of it is public; none of it is a substitute for your own Legal and Compliance teams reading the primary regulation for your firm's footprint.

Two standing caveats. First, regulatory dates and even document numbers move — treat every "as of" here as a prompt to confirm the current version, not a citation to trust blindly. Second, the most useful reading a leadership team can do is not on this list: it is the firm's own honest answers to the questions in [chapter 01](01-for-the-board.md), written down.

---

## For the Board — oversight, duty, and the right questions

**Federal Reserve *Guidance on Model Risk Management*, as recently modernized.** *For directors and the risk committee.* The foundation of how regulated financial firms govern models — owner, independent validation, monitoring, documentation, three lines of defense. The recent modernization refines it; the discipline is what matters, and the fact that **generative and agentic AI sit outside its scope** is the single most important thing a board can know. → [federalreserve.gov · SR letters](https://www.federalreserve.gov/supervisionreg/srletters/srletters.htm)

**NACD, *Director Essentials: Implementing AI Governance* and the Governance Outlook.** *For every director.* The National Association of Corporate Directors' practical guidance on treating AI governance as distinct from IT oversight, assigning clear ownership, recalibrating risk appetite, and building director competency. The closest thing to a board-level playbook for the oversight role. → [nacdonline.org · AI governance](https://www.nacdonline.org/all-governance/governance-resources/trending-oversight-topics/artificial-intelligence/)

**Harvard Law School Forum on Corporate Governance — AI oversight and fiduciary duty.** *For directors and the general counsel.* An ongoing, high-quality stream on how *Caremark* oversight duties and the business-judgment rule apply to AI. This is the intellectual backing for the guide's central claim that **AI governance is now a fiduciary matter**, not an IT preference. → [corpgov.law.harvard.edu](https://corpgov.law.harvard.edu/)

---

## For the CEO & C-suite — strategy, evidence, and what separates leaders

**McKinsey, *The State of AI* (annual).** *For the CEO and executive team.* The most-cited running survey of enterprise AI adoption and value. The finding to internalize is the recurring one: most firms adopt, few capture real value, and the differy is not technology but organization, ownership, and workflow redesign — exactly this guide's thesis. → [mckinsey.com · The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

**Marco Iansiti & Karim Lakhani, *Competing in the Age of AI* (Harvard Business Review Press).** *For the CEO and strategy leads.* The clearest articulation of why AI reshapes the operating model, not just the product — the "AI factory" and the removal of the old limits on scale, scope, and learning. Read it for the argument that this is an organizational transformation that happens to use technology. → *Book.*

**Ethan Mollick, *Co-Intelligence: Living and Working with AI* (Portfolio).** *For every executive, and the fastest single read here.* A grounded, non-hyped account of what it is actually like to work alongside these tools, and why leaders who have not personally used them govern them badly. The antidote to managing AI by anecdote. → *Book.*

---

## For Leadership & the org — people, roles, and the augmented workforce

**Paul Daugherty & H. James Wilson, *Human + Machine: Reimagining Work in the Age of AI* (HBR Press).** *For operating leaders and HR.* The definitive treatment of the "missing middle" — the collaborative roles that appear when humans and machines work together — and the source discipline behind this guide's personas. Read it before you tell your people that "augmented" means augmented. → *Book.*

**Ajay Agrawal, Joshua Gans & Avi Goldfarb, *Prediction Machines* (HBR Press).** *For anyone deciding where to apply AI.* Reframes AI as a drop in the cost of prediction, which cleanly separates what the machine does (prediction) from what stays human (judgment) — the exact line this guide draws through every persona. The most useful mental model on the list for choosing use cases. → *Book.*

**CFA Institute, *Ethics and Artificial Intelligence in Investment Management: A Framework for Professionals*, and *AI in Investment Management*.** *For investment, advisory, and compliance leaders.* Industry-specific, ethics-first guidance written for exactly this sector — the responsibilities that attach when AI touches client outcomes and fiduciary advice. → [CFA Institute · AI framework](https://rpc.cfainstitute.org/research/reports/2022/ethics-and-artificial-intelligence-in-investment-management-a-framework-for-professionals)

---

## For the technical spine — governance, agents, and the frameworks to anchor on

**NIST AI Risk Management Framework (AI RMF 1.0) and the Generative AI Profile (NIST-AI-600-1).** *For the AI owner, risk, and compliance.* The voluntary framework this guide anchors to — Govern, Map, Measure, Manage — plus the companion profile that adapts it specifically to generative AI. The framework a board can point to when asked what the firm's controls are built on. → [nist.gov · AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

**European Commission, the EU AI Act — official regulatory framework and timeline.** *For Legal, Compliance, and any firm with EU exposure.* The primary source, not a tracker. Risk tiers, general-purpose-model obligations, and fines up to 7% of global turnover, still phasing in (some transparency obligations have already landed; parts of the schedule have been adjusted — confirm current dates here). → [digital-strategy.ec.europa.eu · AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

**Anthropic — *Building Effective Agents* and responsible-deployment guidance.** *For builders and the agentic-AI governance owner.* Practical, current engineering guidance on how agents are actually constructed and where they fail — useful for the people writing the bespoke agent layer this guide insists the firm must build itself. → [anthropic.com · engineering](https://www.anthropic.com/engineering/building-effective-agents)

---

## The applied companion — this series, in code

The guide you are reading is the *why and the who.* The *how* is buildable, and it lives in the companion repositories — the best "further reading" is running them:

- [**agents-are-easy-governance-is-hard**](https://github.com/steviebuchicago/agents-are-easy-governance-is-hard) — the five governance gates as working code: the same agent built twice, once as a demo and once accountable.
- [**claude-agents-for-wealth-management**](https://github.com/steviebuchicago/claude-agents-for-wealth-management) — four production-shaped examples for a regulated firm.
- [**crewai-for-beginners**](https://github.com/steviebuchicago/crewai-for-beginners) — a first multi-agent system, from zero.
- [**getting-started-with-openclaw**](https://github.com/steviebuchicago/getting-started-with-openclaw) — a personal-agent on-ramp for the individual builder.

---

*A reading list is a snapshot. Regulations are revised, reports are re-issued annually, and books get new editions — verify the current version of anything before you cite it to your board.*

---

**Next:** [← Back to the guide](../README.md) — or start where the decision lives, with [01 — For the Board](01-for-the-board.md).
