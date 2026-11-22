# Resume Pipeline Command

Execute the HireEngine v2.0 **dual-mode** pipeline with feedback loops and quality gates.

Load and execute the orchestrator workflow from `workflows/skills/resume-pipeline/orchestrator-v2/WORKFLOW.md`

## Dual-Mode Support

The pipeline automatically detects which mode to use:

### 🎯 JD-Aligned Mode (11 stages)
**Activated when:** `input/job_description.txt` exists
**Goal:** Create targeted resume matching specific job requirements

Stages:
1. Intake - Extract background + job description
2. Validate Context - Check completeness
3. Analyze Alignment - Map skills to JD requirements
4. Validate Alignment - Challenge assumptions
5. Generate Content - Write JD-targeted resume
6. Validate Content - Quality check
7. Score ATS - Simulate ATS scoring
8. ATS Gatekeeper - Enforce ATS ≥ 75 threshold
9. Format Output - Generate PDF/DOCX
10. Validate Format - Ensure 1-page
11. Finalize - Package with alignment report

### ✨ Standalone Mode (9 stages)
**Activated when:** No job description provided
**Goal:** Create best possible general-purpose resume

Stages:
1. Intake Standalone - Extract comprehensive background
2. Validate Context - Check completeness
3. Analyze Strengths - Identify competitive advantages
4. Generate Content - Write maximum-impact resume
5. Validate Content - Quality check
6. Enhance Impact - Final amplifications
7. Format Output - Generate professional PDF
8. Validate Format - Check length constraints
9. Finalize - Package with strength analysis

## Pipeline Features

- **Automatic mode detection** based on input files
- **Automatic refinement loops** (up to 3 iterations per stage)
- **Quality gates** (content >= 85/100, ATS >= 75/100 for JD mode)
- **User escalation** when automated fixes fail
- **Comprehensive execution report** with mode-specific metrics

## Usage

**JD-Aligned Mode:**
```
input/
├── job_description.txt    # Provide this
└── raw_background.txt     # Required
```

**Standalone Mode:**
```
input/
└── raw_background.txt     # Only this required
```

Execute the orchestrator prompt and begin pipeline execution.
