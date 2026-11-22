# Resume Pipeline AI

**Enterprise-grade AI workflow system for ATS-optimized resume generation**

An intelligent, multi-stage pipeline that uses 11 specialized AI agents to transform your background into FAANG-level, ATS-optimized resumes with automatic quality improvement and feedback loops.

---

## Features

- **11-Stage AI Workflow** - Orchestrated pipeline with feedback loops and quality gates
- **ATS Optimization** - Simulates real ATS scoring (Greenhouse, Lever, Workday)
- **Provenance Tracking** - Every resume bullet traces back to source facts
- **Surgical Refinement** - Targeted improvements without full regeneration
- **Truth-Bounded Scoring** - Honest assessment of maximum achievable scores
- **Enterprise Architecture** - Modular, scalable, production-ready structure

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
├── input/                        # Pipeline inputs
│   ├── job_description.txt
│   └── raw_background.txt
│
└── output/                       # Pipeline outputs
    ├── resume.pdf
    ├── resume.txt
    ├── PIPELINE_EXECUTION_REPORT.md
    └── resume_metadata.json
```

---

## Quick Start

### 1. Prepare Inputs

Create two files in the `input/` directory:

**`input/raw_background.txt`** - Your resume, LinkedIn profile, or career history

**`input/job_description.txt`** - Target job posting

### 2. Run the Pipeline

```bash
# Using the workflow command (recommended)
/resume-pipeline

# Or via Python script
python scripts/run_pipeline.py
```

### 3. Review Outputs

The pipeline generates:
- `output/resume.pdf` - Final optimized resume
- `output/resume.txt` - Plain text version
- `output/PIPELINE_EXECUTION_REPORT.md` - Detailed 11+ page report
- `output/resume_metadata.json` - Provenance and statistics

---

## Pipeline Workflow Stages

### Stage 1: Intake
Extracts atomic facts with immutable provenance (fact_id) and bounded skill inference.

### Stage 2: Validate Context
Performs completeness check, detects knockout criteria mismatches, generates targeted questions.

### Stage 3: Analyze Alignment
Maps facts to requirements with semantic matching, prerequisite inference, and recency weighting.

### Stage 4: Validate Alignment
Validates alignment matrix, calculates truth-bounded ATS ceiling, decides PASS/FAIL.

### Stage 5: Generate Content
Generates ATS-optimized bullets using X-Y-Z formula with character budget enforcement.

### Stage 6: Validate Content
Detects AI-generated slop ("delved", "seamlessly") and validates X-Y-Z formula compliance.

### Stage 7: Score ATS
Simulates real ATS scoring (keyword matching, skill density, metrics coverage, format compliance).

### Stage 8: ATS Gatekeeper
Quality gate using ATS score - triggers surgical refinement or fails with actionable feedback.

### Stage 9: Format Output
Transforms content into ATS-friendly PDF with character budget enforcement and orphan wrap prevention.

### Stage 10: Validate Format
Final format quality gate - validates character budgets, page limits, ATS compliance.

### Stage 11: Finalize
Assembles final package with provenance tracking, comprehensive report, and actionable next steps.

---

## Key Innovations

### 1. Immutable Provenance Tracking
Every fact gets a unique `fact_id` (F001, F002...), and every resume bullet cites its source facts - preventing hallucination through source verification.

### 2. Surgical Delta Patching
Refinements modify specific `bullet_ids`, not the entire resume, avoiding LLM drift from full regeneration.

### 3. Truth-Bounded Ceiling
Calculates maximum achievable ATS score based on alignment - no false hope, honest assessment.

### 4. Bounded Skill Inference
Only infers skills logically entailed by explicit skills (Kubernetes → Docker ✅, Spring Boot → Kubernetes ❌).

### 5. Feedback Loop Mechanisms
ATS Gatekeeper validates score and triggers refinement - up to 3 automatic iterations with surgical changes.

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
