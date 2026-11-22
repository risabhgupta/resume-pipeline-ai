# Resume Pipeline - AI Workflow Architecture

**11 independent AI agents working together to optimize your resume**

This directory contains the **HireEngine v2.0 Multi-Stage Resume Pipeline** - a collection of AI workflow stages that collaborate to generate ATS-optimized, FAANG-level resumes with automatic quality improvement.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [What Makes This Pipeline Special](#what-makes-this-pipeline-special)
3. [Each Skill's Superpower](#each-skills-superpower)
4. [Component-Based Architecture](#component-based-architecture)
5. [Pipeline Stages](#pipeline-stages)
6. [Feedback Loop Mechanism](#feedback-loop-mechanism)
7. [How to Use](#how-to-use)
8. [Enhancement Status](#enhancement-status)
9. [Design Principles](#design-principles)
10. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

The pipeline consists of **11 AI workflow stages** organized in a sequential flow with **feedback loops** and **quality gates**. Each stage is an autonomous AI agent with specific instructions and validation criteria.

**Think of it as:** 11 expert consultants, each with a specialized role, reviewing and improving your resume in sequence.

### Why AI Workflows Instead of Python Scripts?

**Previous Approach:** Python scripts handling everything (parsing, generation, validation)

**New Approach:** AI workflow stages with specialized prompts for each stage

**Benefits:**
1. **Intelligent Decision-Making:** Each skill can reason about its task
2. **Natural Language Understanding:** Better at parsing resumes and job descriptions
3. **Adaptive Optimization:** Can reframe experience creatively while staying truthful
4. **Feedback Loops:** Skills can challenge each other's outputs
5. **Transparency:** Clear prompts show exactly what each stage does
6. **Extensibility:** Easy to add new skills or modify existing ones

---

## What Makes This Pipeline Special

### 1. Immutable Provenance Tracking
- Every fact gets **fact_id** (F001, F002...)
- Every requirement gets **req_id** (R001, R002...)
- Generated bullets cite fact_ids for traceability
- **Prevents hallucination** through source verification

**Example:**
```json
{
  "bullet_id": "B001",
  "text": "Architected Kubernetes-based microservices platform handling 10K+ transactions/day",
  "source_facts": ["F001", "F005"],
  "F001": "Built microservices platform on Kubernetes",
  "F005": "Platform handles 10,000+ transactions per day"
}
```

### 2. Surgical Delta Patching
- Refinements modify specific **bullet_ids**, not entire resume
- Avoids LLM drift from full regeneration
- Precise instructions: "Change bullet B005 to add metric from fact F012"
- Preserves stable content while fixing issues

### 3. Truth-Bounded Ceiling
- Calculates maximum achievable ATS score based on alignment
- Prevents false hope ("you can get 95 with perfect writing")
- Honest assessment: "With 60% alignment, ceiling is ~65"

### 4. Bounded Skill Inference
- Only infers skills logically entailed by explicit skills
- Kubernetes → Docker (required): confidence 0.95 ✅
- Spring Boot → Kubernetes: NO inference ❌
- Prevents over-claiming skills not truly possessed

**Example:**
```yaml
Kubernetes:
  requires:
    - skill: "Docker"
      confidence: 0.95
      reasoning: "Kubernetes orchestrates Docker containers"

  implies:
    - skill: "YAML"
      confidence: 0.90
      reasoning: "Kubernetes config files are YAML"
```

### 5. Feedback Loop Mechanisms
- **ATS Gatekeeper** validates score and triggers refinement
- Up to 3 automatic refinement iterations
- Surgical changes target specific issues
- Fails gracefully if fundamental gaps exist

---

## Each Workflow Stage's Superpower

### 🔍 Stage 1: Intake - **The Data Detective**

**Superpower:** Extracts atomic facts with immutable provenance (fact_id) and bounded skill inference

**Enhanced With:**
- `config.yaml` - Extraction rules, skill inference settings
- `schemas/fact.schema.json` - Atomic fact structure with fact_id
- `schemas/requirement.schema.json` - JD requirement with req_id
- `knowledge/skill_taxonomy.yaml` - 30+ skills with inference rules
- `knowledge/seniority_keywords.yaml` - Verb → seniority mapping

**Key Features:**
- Extracts facts as **immutable atomic units**
- Each fact gets unique fact_id (F001, F002...)
- Infers related skills only if confidence ≥ 0.70
- Maps action verbs to seniority levels (Architected = Senior, Assisted = Junior)

---

### ✅ Stage 2: Validate Context - **The Completeness Checker**

**Superpower:** Performs completeness check, detects knockout criteria mismatches, generates targeted questions

**Enhanced With:**
- `config.yaml` - Completeness thresholds, knockout criteria settings
- `schemas/validation_result.schema.json` - Validation output structure
- `knowledge/knockout_criteria.yaml` - Security clearances, YOE requirements, licenses
- `knowledge/elicitation_templates.yaml` - Smart question generation (not generic)
- `knowledge/red_flags.yaml` - Chronology issues, gap detection

**Key Features:**
- Detects **knockout criteria** (security clearance, 10+ years required)
- Generates **targeted questions** (not "tell me about your experience")
- Flags chronology issues (inverted dates, concurrent full-time roles)
- Calculates completeness score with weighted components

---

### 📊 Stage 3: Analyze Alignment - **The Keyword Strategist**

**Superpower:** Maps facts to requirements with semantic matching, prerequisite inference, and recency weighting

**Enhanced With:**
- `config.yaml` - Matching settings, recency decay, priority weighting
- `schemas/alignment_matrix.schema.json` - Fact-to-requirement mappings
- `knowledge/semantic_synonyms.yaml` - K8s = Kubernetes, Docker ≈ containerization
- `knowledge/skill_prerequisites.yaml` - Kubernetes → requires Docker (0.95 confidence)
- `knowledge/recency_decay.yaml` - Time-based weighting (current: 1.0, 6+ years: 0.3)

**Key Features:**
- **Semantic matching:** "Docker" matches "containerization" (0.85 score)
- **Prerequisite inference:** Kubernetes experience → implies Docker knowledge
- **Recency weighting:** Recent experience weighted higher (current: 1.0, 6+ years: 0.3)
- **Priority weighting:** MUST_HAVE × 3.0, SHOULD_HAVE × 2.0, NICE_TO_HAVE × 1.0

---

### 🛡️ Stage 4: Validate Alignment - **The Devil's Advocate**

**Superpower:** Validates alignment matrix, calculates truth-bounded ATS ceiling, decides PASS/FAIL

**Enhanced With:**
- `config.yaml` - Validation thresholds, decision logic
- `schemas/validation_result.schema.json` - Validation output with ATS ceiling
- `knowledge/coverage_benchmarks.yaml` - What different coverage levels mean

**Key Features:**
- Validates coverage calculations independently
- Calculates **truth-bounded ATS ceiling** (max achievable score given alignment)
- Detects red flags (no MUST_HAVE matches, all old experience)
- Honest assessment: "With 42% coverage, don't apply - fundamental gap"

**Coverage Tiers:**
- **Excellent (80%+):** Estimated ATS 85-95, strong fit
- **Good (65-79%):** Estimated ATS 70-84, solid candidate
- **Acceptable (50-64%):** Estimated ATS 55-69, worth applying
- **Weak (35-49%):** Estimated ATS 40-54, low interview chance
- **Poor (<35%):** Estimated ATS <40, do not apply

---

### ✍️ Stage 5: Generate Content - **The Resume Writer**

**Superpower:** Generates ATS-optimized bullets using X-Y-Z formula with character budget enforcement

**Enhanced With:**
- `config.yaml` - Writing rules, character budgets
- `knowledge/xyz_templates.yaml` - X-Y-Z formula variations
- `knowledge/action_verbs.yaml` - Seniority-calibrated verbs
- `knowledge/character_budgets.yaml` - Orphan wrap prevention

**Key Features:**
- **X-Y-Z Formula:** "Accomplished [X], as measured by [Y], by doing [Z]"
- **Character Budgets:** One-line (85-105), Two-line (175-210), Forbidden zone (110-145)
- **Orphan Wrap Prevention:** Never create bullets in forbidden zone (creates 1-3 word wrap)
- **Seniority-Calibrated Verbs:** Senior uses "Architected", Junior uses "Assisted"

---

### 🔬 Stage 6: Validate Content - **The Quality Inspector**

**Superpower:** Detects AI-generated slop ("delved", "seamlessly") and validates X-Y-Z formula compliance

**Enhanced With:**
- `config.yaml` - Quality thresholds
- `knowledge/ai_slop_blacklist.yaml` - LLM cliché detector (60+ banned phrases)
- `knowledge/xyz_checker.yaml` - Formula compliance rules

**Key Features:**
- **AI Slop Detection:** Hard-fail on "delved", "testament to", "synergy", "seamlessly"
- **X-Y-Z Validation:** Ensures every bullet has action + measurement + method
- **Weak Verb Detection:** Flags "worked on", "responsible for", "helped with"
- **Summary Fluff Detection:** No "passionate", "results-driven", "team player"

**Banned Phrases (60+):**
```yaml
- "delved"
- "testament to"
- "synergy"
- "seamlessly"
- "cutting-edge"
- "game-changing"
```

---

### 📈 Stage 7: Score ATS - **The ATS Simulator**

**Superpower:** Simulates real ATS scoring (keyword matching, skill density, metrics coverage, format compliance)

**Enhanced With:**
- `config.yaml` - Scoring model weights, keyword matching, penalties
- `schemas/ats_score.schema.json` - Score breakdown structure
- `knowledge/ats_algorithms.yaml` - How real ATS systems work (Greenhouse, Lever, Workday)

**Key Features:**
- **Keyword Matching (40%):** Exact, synonym, partial matches
- **Skill Density (25%):** Optimal 2-3 mentions per skill
- **Metrics Presence (20%):** % of bullets with numbers
- **Format Compliance (10%):** No tables, images, fancy fonts
- **Experience Relevance (5%):** Recency bonuses

**Scoring Example:**
```
Keyword matching:   28/40 (70% match rate)
Skill density:      20/25 (avg 2.5 mentions)
Metrics presence:   16/20 (50% coverage)
Format compliance:  10/10 (ATS-friendly)
Experience:          4/5  (recent relevant)
Total:              78/100 (Good - likely to pass)
```

---

### 🚪 Stage 8: ATS Gatekeeper - **The Auto-Fixer**

**Superpower:** Quality gate using ATS score - triggers surgical refinement or fails with actionable feedback

**Enhanced With:**
- `config.yaml` - Decision thresholds, refinement settings
- `schemas/gatekeeper_decision.schema.json` - Decision structure (PASS/REFINE/FAIL)
- `knowledge/refinement_strategies.yaml` - How to fix each issue type surgically

**Key Features:**
- **Decision Thresholds:** PASS (≥75), REFINE (50-74), FAIL (<50)
- **Surgical Refinement:** "Change bullet B005 to add metric from fact F012"
- **Auto-Fix Strategies:** Missing keywords, low metrics, keyword stuffing, typos
- **Feedback Loop:** Up to 3 iterations with surgical changes

**Example Refinement:**
```json
{
  "iteration": 1,
  "surgical_changes": [
    {
      "target": "bullet_id: B002",
      "instruction": "Add 'Kubernetes' naturally. Original: 'Architected microservices platform'. Suggested: 'Architected Kubernetes-based microservices platform'.",
      "expected_impact": "+2-3 points"
    }
  ]
}
```

---

### 🎨 Stage 9: Format Output - **The PDF Artist**

**Superpower:** Transforms content into ATS-friendly PDF with character budget enforcement and orphan wrap prevention

**Enhanced With:**
- `config.yaml` - PDF settings, ATS compliance rules
- `schemas/formatted_resume.schema.json` - Structured resume representation
- `knowledge/layout_templates.yaml` - ATS-friendly formatting patterns

**Key Features:**
- **Single-Column Layout:** No tables, no text boxes (ATS can't parse)
- **Standard Fonts:** Arial, Calibri, Helvetica (10pt body, 16pt name)
- **Character Budget Enforcement:** Prevents orphan wraps (110-145 char forbidden zone)
- **Page Limit:** Strict 1-2 page limit based on experience

---

### ✔️ Stage 10: Validate Format - **The Final Inspector**

**Superpower:** Final format quality gate - validates character budgets, page limits, ATS compliance

**Enhanced With:**
- `config.yaml` - Format validation rules, auto-fix settings
- `schemas/format_validation.schema.json` - Validation result structure

**Key Features:**
- **Character Budget Check:** All bullets within limits or auto-fixed
- **Orphan Wrap Detection:** Flags bullets in forbidden zone (110-145 chars)
- **Page Limit Enforcement:** Hard fail if > 2 pages
- **ATS Compliance:** No tables, images, non-standard section names

---

### 🎁 Stage 11: Finalize - **The Packager**

**Superpower:** Assembles final package with provenance tracking, comprehensive report, and actionable next steps

**Enhanced With:**
- `config.yaml` - Output file settings, report configuration
- `schemas/final_output.schema.json` - Complete package structure
- `knowledge/report_templates.yaml` - Pipeline report templates

**Key Features:**
- **Provenance Tracking:** Maps every bullet → source fact_ids
- **Pipeline Report:** 11+ page markdown with scores, alignment, refinements
- **Metadata File:** JSON with complete execution history
- **Success Message:** Clear next steps for user

---

## Component-Based Architecture

### Before Enhancement
```
workflow-stage/
  ├── WORKFLOW.md     # Basic description
  └── prompt.md       # Basic instructions
```

### After Enhancement ✅
```
workflow-stage/
  ├── WORKFLOW.md            # Stage definition
  ├── prompt_enhanced.md     # Comprehensive documentation
  ├── config.yaml            # Tunable parameters
  ├── schemas/
  │   ├── input.schema.json
  │   └── output.schema.json
  └── knowledge/
      ├── domain_expertise.yaml
      └── quality_rules.yaml
```

### Total Files Created: 45+

**Breakdown:**
- **11 config.yaml files** - Tunable parameters for each skill
- **15 JSON schemas** - Input/output validation structures
- **18 YAML knowledge bases** - Domain expertise and rules
- **11 prompt_enhanced.md files** - Comprehensive documentation

### Key Knowledge Bases

**Domain Expertise:**
1. `skill_taxonomy.yaml` - 30+ technologies with inference rules
2. `semantic_synonyms.yaml` - Kubernetes = K8s, Docker ≈ containerization
3. `skill_prerequisites.yaml` - Kubernetes → Docker (required)
4. `recency_decay.yaml` - Time-based relevance weighting
5. `ats_algorithms.yaml` - How real ATS systems work

**Quality Rules:**
1. `xyz_templates.yaml` - "Accomplished [X] as measured by [Y] by doing [Z]"
2. `action_verbs.yaml` - Seniority-calibrated verbs
3. `character_budgets.yaml` - One-line, two-line, forbidden zone
4. `knockout_criteria.yaml` - Security clearances, licenses
5. `ai_slop_blacklist.yaml` - 60+ LLM clichés to avoid

---

## Pipeline Stages

### Stage 1: Intake
**Workflow:** `workflows/skills/resume-pipeline/intake/`
**Purpose:** Extract candidate data and job requirements
**Outputs:** Structured facts (F001, F002...) and requirements (R001, R002...)

### Stage 2: Validate Context
**Workflow:** `workflows/skills/resume-pipeline/validate-context/`
**Purpose:** Check completeness, detect knockout criteria
**Outputs:** Completeness score, decision (PASS/FAIL), targeted questions

### Stage 3: Analyze Alignment
**Workflow:** `workflows/skills/resume-pipeline/analyze-alignment/`
**Purpose:** Map facts to requirements with semantic matching
**Outputs:** Alignment matrix with match scores, coverage stats

### Stage 4: Validate Alignment
**Workflow:** `workflows/skills/resume-pipeline/validate-alignment/`
**Purpose:** Validate alignment, calculate truth-bounded ceiling
**Outputs:** ATS ceiling, decision (PASS/FAIL), recommendations

### Stage 5: Generate Content
**Workflow:** `workflows/skills/resume-pipeline/generate-content/`
**Purpose:** Write ATS-optimized bullets using X-Y-Z formula
**Outputs:** Resume bullets with provenance tracking

### Stage 6: Validate Content
**Workflow:** `workflows/skills/resume-pipeline/validate-content/`
**Purpose:** Detect AI slop, validate formula compliance
**Outputs:** Quality score, detected issues

### Stage 7: Score ATS
**Workflow:** `workflows/skills/resume-pipeline/score-ats/`
**Purpose:** Simulate ATS scoring
**Outputs:** ATS score /100, breakdown, improvement suggestions

### Stage 8: ATS Gatekeeper
**Workflow:** `workflows/skills/resume-pipeline/ats-gatekeeper/`
**Purpose:** Quality gate with surgical refinement
**Outputs:** Decision (PASS/REFINE/FAIL), refinement plan
**Feedback Loop:** Can send back to Stage 5 for iteration

### Stage 9: Format Output
**Workflow:** `workflows/skills/resume-pipeline/format-output/`
**Purpose:** Generate ATS-friendly PDF
**Outputs:** resume.pdf, resume.txt

### Stage 10: Validate Format
**Workflow:** `workflows/skills/resume-pipeline/validate-format/`
**Purpose:** Validate format quality
**Outputs:** Validation results, decision (PASS/FAIL)

### Stage 11: Finalize
**Workflow:** `workflows/skills/resume-pipeline/finalize/`
**Purpose:** Create final package with report
**Outputs:** All deliverables, PIPELINE_EXECUTION_REPORT.md

---

## Feedback Loop Mechanism

### How Validators Challenge Generators

```
Stage 3: Analyze Alignment (Generator)
   ↓ produces alignment matrix
Stage 4: Validate Alignment (Validator)
   ↓ challenges assumptions
   ├─ If APPROVED → Continue
   ├─ If CHANGES_NEEDED → Send feedback to Stage 3
   └─ If iteration >= 3 → Escalate to user

Stage 5: Generate Content
   ↓ produces resume bullets (score: 67/100)
Stage 6: Validate Content
   ↓ detects AI slop, missing metrics
   → Sends surgical fixes to Stage 5

Stage 5: Generate Content (iteration 2)
   ↓ applies fixes (score: 91/100)
Stage 6: Validate Content
   → PASS ✅

Stage 7: Score ATS
   ↓ calculates score: 58/100
Stage 8: ATS Gatekeeper
   ↓ below threshold (60)
   → Surgical refinement: Add 'Kubernetes' to bullet B002

Stage 7: Score ATS (rescore)
   → New score: 74/100
   → PASS ✅
```

---

## How to Use

### Running the Full Pipeline

```bash
# Option 1: Use the command (recommended)
/resume-pipeline

# Option 2: Direct execution
# The orchestrator will execute all 11 stages sequentially
```

### Inputs Required

```
input/raw_background.txt       # Your resume, LinkedIn, experience
input/job_description.txt      # Target job posting
```

### Outputs Generated

```
output/resume.pdf                        # Final optimized resume
output/resume.txt                        # Plain text version
output/PIPELINE_EXECUTION_REPORT.md     # Detailed 11+ page report
output/resume_metadata.json             # Provenance + stats
output/pipeline_state.json              # Full execution state
```

### Example Execution

```
User: /resume-pipeline

Stage 1: Intake ✅
  → Extracted 25 facts (F001-F025)
  → Extracted 8 requirements (R001-R008)
  → Completeness: 85%

Stage 2: Validate Context ✅
  → Decision: PASS_WITH_WARNINGS
  → Warning: Career gap (8 months)

Stage 3: Analyze Alignment ✅
  → Overall coverage: 68%
  → MUST_HAVE coverage: 75%

Stage 4: Validate Alignment ✅
  → ATS Ceiling: 74
  → Decision: PASS (good alignment)

Stage 5: Generate Content ✅
  → 12 bullets generated
  → All cite fact_ids

Stage 6: Validate Content ✅
  → No AI slop detected
  → X-Y-Z compliance: 100%

Stage 7: Score ATS ✅
  → Score: 67/100

Stage 8: ATS Gatekeeper 🔧
  → Below threshold, refining...
  → Iteration 1: +7 points
  → New score: 74/100 ✅

Stage 9: Format Output ✅
  → Generated PDF (1.8 pages)

Stage 10: Validate Format ✅
  → All checks passed

Stage 11: Finalize ✅
  → Package complete

🎉 SUCCESS: Resume ready at output/resume.pdf
```

---

## Enhancement Status

**✅ ALL 11 WORKFLOW STAGES FULLY ENHANCED**

Each workflow stage now has:
- ✅ Comprehensive `prompt_enhanced.md` documentation
- ✅ Tunable `config.yaml` parameters
- ✅ JSON schemas for validation
- ✅ YAML knowledge bases with domain expertise
- ✅ Individual enhancement capability

**Total Enhancement Time:** ~2 hours
**Workflow Stages Enhanced:** 11/11 (100%)

---

## Design Principles

### 1. Single Responsibility
Each skill has one clear purpose. Stage 3 analyzes, Stage 4 validates. No overlap.

### 2. Transparent Communication
Every skill reports what it did, why, and what happens next. User always knows pipeline state.

### 3. Fail-Safe Iteration
Auto-fix up to 3 times before escalating. Never silently fail or proceed with bad output.

### 4. Truthfulness Above Optimization
Validators ensure we never fabricate experience. Keyword injection only if related to background.

### 5. Progressive Enhancement
Each stage builds on previous stages. State carries forward. No redundant work.

---

## Troubleshooting

### Pipeline Gets Stuck in Loop

**Symptom:** Same skill regenerating repeatedly

**Cause:** Feedback not specific enough

**Fix:** Validator needs more specific guidance in surgical changes

### ATS Score Never Reaches Threshold

**Symptom:** Iteration count hits 3, still below 60

**Cause:** Fundamental alignment gap (candidate lacks required skills)

**Fix:** Pipeline will FAIL with honest assessment - do not apply to this role

### Character Budget Violations

**Symptom:** Bullets in forbidden zone (110-145 chars)

**Cause:** Generator not respecting character limits

**Fix:** Auto-fixed by validate-format skill (shortens to <105 or expands to >175)

### Missing Provenance

**Symptom:** Bullet doesn't cite fact_ids

**Cause:** Generator hallucinated achievement

**Fix:** Validator will catch and request regeneration with proper fact citation

---

## Future Enhancements

- [ ] Add skill for LinkedIn profile generation
- [ ] Add skill for detecting and removing bias
- [ ] Add skill for tailoring to company culture
- [ ] Add skill for generating interview prep questions
- [ ] Add skill for A/B testing multiple resume versions

---

## Credits

**HireEngine v2.0 Multi-Stage Pipeline**
- Architecture: AI skill-based with feedback loops
- Enhancements: Component-based with knowledge bases
- Quality Gates: Content, ATS, Format
- Powered by: Claude Code CLI
- Created: October 2026
- Enhanced: January 2025

**Each skill is now a superpowered, individually-enhanceable module with deep domain knowledge, tunable parameters, and comprehensive documentation!**