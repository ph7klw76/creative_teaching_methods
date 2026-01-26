# Embedding Artificial Intelligence in Undergraduate Physics to Improve Student Outcomes: Evidence, Design Patterns, and Implementation Guidelines

## Abstract

Artificial intelligence (AI) is rapidly reshaping how undergraduate physics can be taught, practiced, and assessed. This review synthesizes evidence from research on intelligent tutoring systems (ITS), AI-supported active learning, and generative AI (large language models; LLMs) to identify approaches most likely to improve student learning outcomes across the undergraduate physics curriculum. Evidence from meta-analyses suggests that well designed ITS frequently produce learning gains above conventional instruction and can approach the effectiveness of human tutoring under some conditions. Physics-specific systems (e.g., step-based problem-solving tutors) show that “making reasoning visible” and providing immediate, step-level feedback can improve problem-solving performance without requiring major curricular overhaul. Recent randomized controlled evidence also indicates that AI tutoring can outperform in-class active learning in an authentic educational setting, though generalization and implementation details matter. In parallel, LLMs offer scalable conversational support but introduce risks: over-trust, persuasive but incorrect explanations, and inconsistent performance especially on conceptual and visual-representation tasks requiring explicit AI literacy and verification workflows. We conclude with a practical, outcomes-aligned framework for embedding AI across lectures, tutorials, homework, laboratories, and assessment, emphasizing guardrails, equity, and rigorous evaluation.

# 1. Introduction

Undergraduate physics learning outcomes commonly include (i) conceptual understanding, (ii) quantitative problem solving, (iii) representational competence (graphs, free-body diagrams, field maps), (iv) experimental reasoning and uncertainty analysis, and (v) computational/data competencies. AI can support these outcomes through at least four distinct roles:

- Step-based tutoring and feedback (ITS/digital tutors) for structured problem solving.
- Adaptive practice and learning analytics for targeted remediation and pacing.
- Generative AI (LLMs) for conversational explanations, feedback on reasoning, and writing/code support.
- AI-enabled data science workflows (e.g., machine learning, automation) as both content and tooling for modern physics practice.

The central question is not whether AI is “powerful,” but whether a given AI integration improves measurable learning outcomes under real instructional constraints without undermining academic integrity, equity, or student agency.

# 2. Evidence base: what tends to improve outcomes?

## 2.1 Intelligent tutoring systems and digital tutors

Meta-analytic research across domains generally finds positive effects of ITS compared with conventional instruction, with effect sizes varying by tutor design, comparison condition, and alignment of assessments to what the tutor teaches. Fletcher and Kulik’s meta-analytic review reports substantial performance gains for digital tutors across controlled evaluations (with typical median effects reported as meaningfully above conventional classes).

A complementary synthesis of meta-reviews highlights that step-based ITS systems that respond to each step of a learner’s solution rather than only the final answer—can approach the effectiveness of average human tutors, while still exceeding “content-only” conditions.  
**Interpretation:** the instructional mechanism most consistently linked to gains is not “AI magic,” but timely, specific feedback tied to learner actions.

## 2.2 Physics-specific tutoring: step-level feedback and representational practices

A canonical physics example is the Andes Physics Tutoring System, designed to be “minimally invasive” (students do the same homework problems, but inside a tutor that provides immediate feedback). Andes emphasizes entering a full derivation—drawing diagrams, defining variables, and writing equations—then provides feedback at the step level. The authors report multi-year evidence of improved learning in authentic course settings and argue that step granularity and feedback timing are key design features.  
**Interpretation:** physics benefits when AI enforces expert-like habits (units, diagrams, variable definitions), because these habits reduce downstream errors and strengthen transfer.

## 2.3 Randomized field evidence: AI tutoring vs active learning

A recent randomized controlled trial in an authentic educational setting reports that AI tutoring outperformed in-class active learning on measured outcomes, positioning AI tutoring as a potentially high-impact intervention when well aligned to learning goals and embedded into real course workflows.  
**Interpretation:** AI can be more than “study help” if it is engineered as instruction yet replication across institutions, topics, and student populations remains crucial.

## 2.4 Generative AI (LLMs): scalable dialogue, new risks

A rapid review in The Physics Teacher synthesizes emerging uses of GPT-style tools in physics education, reflecting rapid adoption and diverse classroom experiments.  
However, physics-specific scholarship also cautions that LLM outputs can be confidently wrong and that effective use requires understanding how the model generates text, not “truth.” In European Journal of Physics, Polverini and Gregorcic argue that knowing core LLM behaviors (pattern-based generation, sensitivity to prompting, and failure modes) should inform pedagogy and guardrails when using ChatGPT in physics learning.

Crucially, students may over-trust LLM answers. In an undergraduate physics-class study, Ding et al. report that many students trusted ChatGPT’s correctness despite answer inaccuracies, and that trust was associated with students’ perceptions—highlighting the need for explicit AI literacy and verification practices.  
**Interpretation:** LLMs can scale feedback and dialogue, but without structured verification they may amplify misconceptions (because a fluent explanation feels like understanding).

## 2.5 AI and data science as a “fourth pillar” in undergraduate physics

Physics curricula increasingly incorporate data science and computation as core competencies. Shah et al. describe lessons from a community of practice focused on data science education in undergraduate physics, emphasizing practical integration strategies, instructor support, and curriculum design grounded in real departmental constraints.  
**Interpretation:** “Embedding AI” is not only about tutors—teaching students to use modern computational/ML methods can itself be an outcome that improves employability and authentic scientific practice, while reinforcing physics concepts through modeling and data.

# 3. Design principles for embedding AI in undergraduate physics

The evidence suggests a few high-leverage principles that translate across course types (introductory to advanced):

- **Outcome alignment first, tools second.** Decide which outcome you are improving (conceptual change, problem-solving transfer, representational fluency, lab reasoning, computational thinking). Then pick an AI role that directly targets it.

- **Make reasoning observable.** Prefer systems that require students to externalize intermediate reasoning (steps, diagrams, assumptions). Step-based feedback is repeatedly implicated in stronger gains than “final answer only” feedback.

- **Use AI as a coach, not an oracle.** In practice: hinting, error diagnosis, and “next-step prompts” outperform direct solution dumping for long-term learning.

- **Build verification into the workflow.** Require students to check claims against principles (units, limiting cases, conservation laws), not just accept fluent text. This directly addresses LLM over-trust.

- **Treat AI literacy as physics literacy.** Students should learn what the model optimizes (likely text, not truth), typical failure modes, and how to interrogate outputs.

# 4. Course-level integration patterns (ready to implement)

## 4.1 Lectures and active learning sessions

- **Pre-class AI micro-tutoring:** short guided dialogues that elicit misconceptions before class (concept checks + “explain your reasoning” prompts).

- **In-class AI as “feedback amplifier”:** during peer instruction, AI can generate alternative explanations after students commit to an answer, then students critique the AI explanation using course principles (turning AI into a foil rather than an authority).

## 4.2 Tutorials / recitations (problem-solving core)

- Adopt step-based homework support (commercial, open, or locally built) that enforces: diagram → variable definitions → governing principles → algebra → numeric substitution. This mirrors what Andes demonstrated as a high-impact interaction grain size.

- If using an LLM, constrain it: require it to ask a diagnostic question, then provide a hint, then request the next student step (instead of providing full solutions). This mimics ITS pedagogy without pretending the LLM is perfectly reliable.

## 5.3 Homework and formative assessment

- **Two-channel submission:** (i) student solution, (ii) “AI audit trail” (what was asked, what was received, what was accepted/rejected, and why). This converts integrity risk into metacognitive practice.

- **Rubrics that reward verification:** points for dimensional analysis, limiting-case checks, and explaining why an AI suggestion is correct/incorrect.

## 4.4 Laboratories and computational physics

- **Use AI tools to speed mechanics, not replace thinking:** automated curve fitting, uncertainty propagation templates, code scaffolds for analysis pipelines.

- **Require “interpretation checkpoints”:** students must justify model choice, noise assumptions, and whether outputs are physically plausible.

## 4.5 Summative assessment (exams/projects)

- **Keep high-stakes tests human-verifiable:** oral mini-vivas, in-class derivations, or practical lab exams reduce the incentive and feasibility of unproductive AI use.

- **For AI-allowed projects, grade the scientific process:** hypothesis → method → validation → limitations → reproducibility.

# 5. Evaluation: proving the AI actually helped

A serious implementation should measure impact rather than assume it:

- Concept inventories / validated instruments where available (or carefully designed common exams).
- Transfer tasks (novel contexts) to check whether AI improved real understanding rather than pattern matching.
- Equity audits: check whether gains differ by prior preparation (ITS can help, but effects can vary by subgroup; monitor, don’t guess).
- Process metrics: error types, time-on-task, hint usage, and student reflections on verification.

# 6. Risks, ethics, and governance

- **Over-trust and anthropomorphism:** students may treat fluent AI as authoritative; explicit instruction and verification rubrics are non-optional.

- **Accuracy and hallucinations:** LLMs can generate plausible but incorrect physics; design activities where students must detect and correct AI errors.

- **Privacy and data policy:** adopt institution-approved tools and minimize sensitive data exposure.

- **Access and equity:** ensure all students have comparable access; otherwise AI becomes a hidden prerequisite.

# 7. Conclusion

Embedding AI into undergraduate physics can improve outcomes when AI is designed as instruction: step-level feedback, enforced expert practices, and structured verification. The strongest evidence supports tutoring-style interventions and carefully engineered feedback loops, including physics-specific step-based approaches and recent randomized evidence showing substantial gains in authentic settings. Generative AI expands scalability but raises unique epistemic risks especially student over-trust making AI literacy and verification workflows integral to physics learning rather than optional add-ons. The practical path forward is outcome-aligned integration, guardrails that keep students cognitively in charge, and rigorous evaluation of learning gains and equity impacts.

# References

[1] Kestin G, Miller K, Klales A, Milbourne T, Ponti G. AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting. Scientific Reports. 2025;15:17458. doi:10.1038/s41598-025-97652-6.  
[2] Fletcher JD, Kulik JA. Effectiveness of intelligent tutoring systems: A meta-analytic review. Review of Educational Research. 2016. doi:10.3102/0034654315581420.  
[3] Ma W, Adesope OO, Nesbit JC, Liu Q. Intelligent tutoring systems and learning outcomes: A meta-analysis. Journal of Educational Psychology. 2014;106(4):901–918. doi:10.1037/a0037123.  
[4] VanLehn K, Lynch C, Schulze K, et al. The Andes Physics Tutoring System: Lessons Learned. International Journal of Artificial Intelligence in Education. 2005;15(3).  
[5] Shah R, VanderPlas S, Risser M, et al. Data science education in undergraduate physics: lessons learned from a community of practice. American Journal of Physics. 2024. doi:10.1119/5.0203846.  
[6] Wu H, Tong D, Li Z, Tao Y, Deng S, Ren H. GPT’s Application in Physics Education: A Rapid Review. The Physics Teacher. 2025;63(9):786. doi:10.1119/5.0259592.  
[7] Polverini G, Gregorcic B. How understanding large language models can inform the use of ChatGPT in physics education. European Journal of Physics. 2024;45(2):025701. doi:10.1088/1361-6404/ad1420.  
[8] Polverini G, Gregorcic B. Multimodal large language models and physics visual tasks: comparative analysis of performance and costs. European Journal of Physics. 2025;46(5). doi:10.1088/1361-6404/ae03f8.  
[9] Ding L, Li T, Jiang S, Gapud A. Students’ perceptions of using ChatGPT in a physics class as a virtual tutor. International Journal of Educational Technology in Higher Education. 2023;20:63. doi:10.1186/s41239-023-00434-1.  
[10] du Boulay B. Recent meta-reviews and meta-analyses of AIED systems. 2016.

