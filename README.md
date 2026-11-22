# Resume Pipeline AI

**Enterprise-grade AI workflow system for ATS-optimized resume generation**

An intelligent, **dual-mode** pipeline that uses specialized AI agents to transform your background into professional resumes:
- **JD-Aligned Mode** (11 stages): Target specific jobs with ATS optimization
- **Standalone Mode** (9 stages): Create best general-purpose resume without job description

---

## Features

- **🎯 Dual-Mode Operation** - JD-aligned OR standalone resume generation
- **🤖 Intelligent Workflow** - 9-11 AI stages with feedback loops and quality gates
- **📊 ATS Optimization** - Simulates real ATS scoring (JD-aligned mode)
- **💪 Strength Analysis** - Identifies competitive advantages (standalone mode)
- **🔍 Provenance Tracking** - Every resume bullet traces back to source facts
- **⚡ Surgical Refinement** - Targeted improvements without full regeneration
- **✅ Truth-Bounded Scoring** - Honest assessment of maximum achievable scores
- **🏗️ Enterprise Architecture** - Modular, scalable, production-ready structure

---

## Project Structure

```
resume-pipeline-ai/
├── src/                          # Core library code
│   └── resume_pipeline/
│       ├── parsers/              # Resume/JD parsing logic
│       ├── analyzers/            # ATS scoring, alignment analysis
│       ├── generators/           # Content generation utilities
│       ├── formatters/           # PDF/DOCX generation
│       └── utils/                # Shared utilities
│
├── workflows/                    # AI workflow orchestrations
│   ├── commands/                 # Workflow commands
│   └── skills/
│       └── resume-pipeline/      # 11-stage pipeline
│           ├── orchestrator/     # Pipeline orchestration
│           ├── intake/           # Data extraction
│           ├── validate-context/ # Completeness checking
│           ├── analyze-alignment/# Keyword analysis
│           ├── validate-alignment/# Alignment validation
│           ├── generate-content/ # Resume writing
│           ├── validate-content/ # Quality checking
│           ├── score-ats/        # ATS simulation
│           ├── ats-gatekeeper/   # Quality gate
│           ├── format-output/    # PDF generation
│           ├── validate-format/  # Format validation
│           └── finalize/         # Package assembly
│
├── scripts/                      # Standalone scripts
│   └── run_pipeline.py
│
├── tests/                        # Test suites
├── docs/                         # Documentation
├── input/                        # Pipeline inputs (shared)
│   ├── job_description.txt
│   └── raw_background.txt
│
└── output/                       # Execution-scoped outputs
    ├── run-20261123-003045-jd-microsoft/     # JD-aligned run
    │   ├── pipeline_state.json
    │   ├── resume.pdf
    │   ├── resume.txt
    │   ├── alignment_matrix.json
    │   ├── ats_score.json
    │   └── EXECUTION_REPORT.md
    │
    ├── run-20261123-003512-standalone/        # Standalone run
    │   ├── pipeline_state.json
    │   ├── resume.pdf
    │   ├── strength_analysis.json
    │   └── EXECUTION_REPORT.md
    │
    └── latest -> run-20261123-003512-standalone/  # Symlink to latest
```

---

## Quick Start

### Mode 1: JD-Aligned (Target Specific Job)

**1. Prepare Inputs:**
```
input/
├── job_description.txt    # Copy-paste job posting
└── raw_background.txt     # Your resume/LinkedIn/career history
```

**2. Run Pipeline:**
```bash
/resume-pipeline
```

**3. Output:**
- Targeted resume optimized for the specific job
- ATS score report (target: ≥75/100)
- Keyword alignment analysis
- `output/[Name]_[Company]_[Role]_2026.pdf`

### Mode 2: Standalone (General-Purpose Resume)

**1. Prepare Input:**
```
input/
└── raw_background.txt     # Your resume/LinkedIn/career history only
```

**2. Run Pipeline:**
```bash
/resume-pipeline
```

**3. Output:**
- Best possible general-purpose resume
- Strength analysis report
- Competitive advantages identified
- `output/[Name]_Resume_2026.pdf`

### Execution-Scoped Outputs

**Each run creates its own isolated directory:**

```
output/run-{TIMESTAMP}-{MODE}-{TARGET}/
├── pipeline_state.json           # Execution state
├── resume.pdf                     # Final resume
├── resume.txt                     # Plain text version
├── EXECUTION_REPORT.md            # Detailed report
└── [mode-specific files]          # alignment_matrix.json, strength_analysis.json, etc.
```

**Benefits:**
- ✅ Run multiple jobs simultaneously
- ✅ Keep history of all executions
- ✅ Easy comparison of different versions
- ✅ Clean isolated state per run
- ✅ Symlink `output/latest/` points to most recent

**Example:**
```bash
# First run (Microsoft)
/resume-pipeline
# Creates: output/run-20261123-120000-jd-microsoft/

# Second run (Google) - doesn't interfere!
/resume-pipeline
# Creates: output/run-20261123-120530-jd-google/

# Access latest
ls output/latest/resume.pdf
```

---

## Pipeline Workflow Stages

### JD-Aligned Mode (11 Stages)

**Stage 1: Intake** - Extract background + job description with fact IDs
**Stage 2: Validate Context** - Check completeness, detect knockout criteria
**Stage 3: Analyze Alignment** - Map skills to JD requirements with semantic matching
**Stage 4: Validate Alignment** - Calculate truth-bounded ATS ceiling
**Stage 5: Generate Content** - Write JD-targeted resume with X-Y-Z formula
**Stage 6: Validate Content** - Detect AI slop, validate quality
**Stage 7: Score ATS** - Simulate real ATS scoring
**Stage 8: ATS Gatekeeper** - Quality gate (require ≥75 score)
**Stage 9: Format Output** - Generate ATS-friendly PDF
**Stage 10: Validate Format** - Check page limits and formatting
**Stage 11: Finalize** - Package with alignment report

### Standalone Mode (9 Stages)

**Stage 1: Intake Standalone** - Extract comprehensive background and seniority
**Stage 2: Validate Context** - Check completeness
**Stage 3: Analyze Strengths** - Identify competitive advantages with impact scoring
**Stage 4: Generate Content Standalone** - Write maximum-impact resume
**Stage 5: Validate Content** - Quality check with X-Y-Z validation
**Stage 6: Enhance Impact** - Apply final metric amplifications
**Stage 7: Format Output** - Generate professional PDF
**Stage 8: Validate Format** - Check length constraints
**Stage 9: Finalize Standalone** - Package with strength analysis report

---

## Key Innovations

### 1. Dual-Mode Operation
Automatically detects whether to optimize for a specific job (JD-aligned) or create the best general resume (standalone) based on input files.

### 2. Strength Analysis (Standalone Mode)
Scores every achievement on scale (1-10), complexity (1-10), and business value (1-10) to identify top accomplishments and competitive advantages.

### 3. Immutable Provenance Tracking
Every fact gets a unique `fact_id` (F001, F002...), and every resume bullet cites its source facts - preventing hallucination through source verification.

### 4. Surgical Delta Patching
Refinements modify specific `bullet_ids`, not the entire resume, avoiding LLM drift from full regeneration.

### 5. Truth-Bounded Ceiling (JD-Aligned Mode)
Calculates maximum achievable ATS score based on alignment - no false hope, honest assessment.

### 6. Impact Maximization (Standalone Mode)
Prioritizes achievements by impact score, recency, hot technologies, and uniqueness to create the most compelling resume.

### 7. Feedback Loop Mechanisms
Quality gates validate content and trigger refinement - up to 3 automatic iterations with surgical changes.

---

## Enterprise Design Principles

### Separation of Concerns
- **`src/`** - Reusable library code
- **`workflows/`** - AI orchestration stages
- **`scripts/`** - Standalone executables
- **`tests/`** - Automated test suites

### Modular Architecture
Each workflow stage is independently enhanceable with:
- `WORKFLOW.md` - Stage definition
- `config.yaml` - Tunable parameters
- `schemas/` - Input/output validation
- `knowledge/` - Domain expertise

### Production-Ready
- Comprehensive error handling
- State management and recovery
- Detailed execution logging
- Quality gates at every stage

---

## Technology Stack

- **AI Orchestration**: Claude Code / AI Agents
- **Language**: Python 3.8+
- **Document Processing**: PDF/DOCX generation
- **Data Format**: YAML, JSON, Markdown
- **Workflow Engine**: Multi-stage pipeline with feedback loops

---

## Documentation

- [Workflow Architecture](workflows/skills/resume-pipeline/README.md) - Detailed pipeline documentation
- [Validation Framework](workflows/skills/resume-pipeline/VALIDATION_FRAMEWORK.md) - Quality gates and thresholds
- [Quality Thresholds](workflows/skills/resume-pipeline/QUALITY_THRESHOLDS.md) - Scoring criteria

---

## Contributing

This is an enterprise-grade project following best practices:
- Use `src/` layout for library code
- Use `workflows/` for orchestration stages
- Follow the modular architecture pattern
- Add tests for new functionality

---

## License

Proprietary - HireEngine v2.0

---

## Credits

**HireEngine v2.0 Multi-Stage Pipeline**
- Architecture: AI workflow-based with feedback loops
- Structure: Enterprise Python best practices
- Quality Gates: Content, ATS, Format validation
- Created: October 2026
- Enhanced: January 2025

**Built with:** Claude Code CLI, following enterprise automation framework patterns
