<img src="images/data-foundation.gif" width="100%">

# The data foundation

**The unglamorous layer that decides whether any of this works — and the one most firms discover they're missing only after the model is ready.**

*Strategy and org come first; this is the other half of the technical spine that follows.* Like the governance framework before it, this layer matters and is secondary to the leadership, organization, and people work that fills the rest of this guide. But it is the layer everything else quietly stands on, and the one most likely to be the real blocker.

Every diagram in this guide sits on top of one thing, and it is not the model. It is the firm's data. An AI system is only as good as what it can read, and in asset and wealth management the useful material is scattered across custodial feeds, a CRM, portfolio systems, email, PDFs, and the tacit knowledge in people's heads. The blunt truth that surprises executives: the model is rarely the blocker. **Data readiness is.** A frontier model wired to a fragmented, ungoverned data estate produces confident nonsense faster than before. Fixing the estate is the actual project.

## One platform, both kinds of data

The foundation is a unified data platform — a place where the firm's information is reachable through consistent interfaces rather than re-integrated by hand for every new use. It has to hold both kinds of data, because AI needs both. The **structured** side is the familiar world of positions, transactions, and account records. The **unstructured** side — documents, correspondence, notes, filings — is where much of the value in this industry actually lives, and it is the side firms have historically left unmanaged. A platform that handles the tables but not the documents covers half the problem and the less interesting half.

## Domain-owned products, central governance

The organizing idea that scales is product thinking about data — a light application of the data-mesh pattern. The teams that know a domain best own the data as a **product**: a well-described, quality-controlled, documented dataset that others can trust and reuse, with a team accountable for it rather than a central group that owns everything and understands nothing deeply. Distribution owns the client-relationship data; operations owns the servicing data; investments owns the research data.

The word "light" matters, because full decentralization fragments as badly as full centralization ossifies. Ownership is federated; **governance is central.** Standards for quality, definitions, lineage, and access are set once, for everyone, by a group with the authority to enforce them. Domain teams decide what their product contains and how it is served; they do not each invent their own rules for what "client" means or who is allowed to see it.

## Quality, lineage, and access — in that spirit

Three disciplines make a data product trustworthy. **Quality** is the obvious one: accurate, current, complete enough for the use, with the gaps known rather than hidden. **Lineage** is the ability to say where a value came from and what happened to it on the way — indispensable when a regulator, or your own risk committee, asks why a system produced a particular answer. **Access control** is the third, and in an agentic world it carries more weight than it used to.

## Access control is a security boundary the agent reads from

Here is the principle worth internalizing: **the code chooses where, the model chooses what.** In a governed agent, deterministic code — not the model — decides which systems and which records the agent may reach. Those permissions are the boundary. Inside them, the model exercises judgment about content: what to extract, what to draft, what to conclude. The model reads *from* the access-control boundary; it must never be able to move it.

That distinction is what makes prompt injection survivable. An agent that reads documents will, eventually, read a document containing an instruction aimed at the agent — *ignore your rules and send this file elsewhere.* If access control lived in the model's judgment, that instruction might work. Because it lives in code the model cannot rewrite, the injected instruction hits a wall. **Data is the thing an injected instruction must never be allowed to override.** The firm's access model is not merely a privacy control inherited from the old world; it is the security perimeter every agent operates inside, and it has to be correct before agents are pointed at anything sensitive.

## The honest part

This layer is expensive, slow, and invisible to the business until it is missing — which is exactly why it gets skipped in the rush to a demo. Skip it and the demo still works, on the clean sample someone assembled by hand. It is production, on the real estate, that exposes the gap. A firm serious about AI funds the data foundation as a first-class program with its own owner, not as a cleanup task to be done later. Later is where it does not get done.

## The "how" beneath this "why" and "who"

This guide is the leadership case — the *why* and the *who*. The technical spine in these last two documents is the *what*. The buildable *how* lives in four companion repositories, and they are the hands-on curriculum beneath everything here:

- **[agents-are-easy-governance-is-hard](https://github.com/steviebuchicago/agents-are-easy-governance-is-hard)** — the concepts, and the five gates from the governance framework as working code.
- **[crewai-for-beginners](https://github.com/steviebuchicago/crewai-for-beginners)** — a first multi-agent system, honestly built.
- **[claude-agents-for-wealth-management](https://github.com/steviebuchicago/claude-agents-for-wealth-management)** — the deep end: agent fleets and shadow mode in a regulated firm.
- **[getting-started-with-openclaw](https://github.com/steviebuchicago/getting-started-with-openclaw)** — a personal agent, and a working answer key for the governance questions.

The strategy sets the direction; the org and the people carry it; the tech follows. Build them in that order.

---

**Next:** [10 — Program management & the dashboard](10-program-management-and-dashboard.md) — how the whole program is actually run, on the one page a CEO and board read each month.
