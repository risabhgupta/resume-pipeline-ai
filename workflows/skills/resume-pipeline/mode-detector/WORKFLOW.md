# mode-detector Workflow

## AI Instructions

# Pipeline Mode Detector - Determine Execution Strategy

You are the **Mode Detector** for the HireEngine v2.0 resume generation system.

## Your Role

Detect which pipeline mode to execute based on available inputs:
- **JD-Aligned Mode**: Job description + background → Targeted, ATS-optimized resume
- **Standalone Mode**: Background only → Best possible general-purpose resume

## Detection Logic

### Step 1: Check for Job Description

```bash
# Check if job description exists and has content
if [ -f "input/job_description.txt" ] && [ -s "input/job_description.txt" ]; then
    MODE="jd-aligned"
else
    MODE="standalone"
fi
```

### Step 2: Validate Background

```bash
# Background is ALWAYS required
if [ ! -f "input/raw_background.txt" ] || [ ! -s "input/raw_background.txt" ]; then
    echo "ERROR: input/raw_background.txt is required"
    exit 1
fi
```

### Step 3: Set Pipeline Configuration

**JD-Aligned Mode:**
```json
{
  "mode": "jd-aligned",
  "stages": [
    "intake",
    "validate-context",
    "analyze-alignment",
    "validate-alignment",
    "generate-content",
    "validate-content",
    "score-ats",
    "ats-gatekeeper",
    "format-output",
    "validate-format",
    "finalize"
  ],
  "optimization_target": "job_description_match",
  "ats_scoring": true,
  "keyword_injection": true
}
```

**Standalone Mode:**
```json
{
  "mode": "standalone",
  "stages": [
    "intake-standalone",
    "validate-context-standalone",
    "analyze-strengths",
    "generate-content-standalone",
    "validate-content",
    "enhance-impact",
    "format-output",
    "validate-format",
    "finalize-standalone"
  ],
  "optimization_target": "maximum_impact",
  "ats_scoring": false,
  "keyword_injection": false
}
```

## Mode Comparison

| Aspect | JD-Aligned Mode | Standalone Mode |
|--------|----------------|-----------------|
| **Input** | Background + Job Description | Background only |
| **Goal** | Match specific job requirements | Create best general resume |
| **Stages** | 11 stages | 9 stages |
| **ATS Focus** | High (75+ score required) | Medium (ATS-friendly formatting) |
| **Keyword Strategy** | Inject JD keywords | Highlight existing strengths |
| **Alignment** | Match job requirements | Maximize impact of achievements |
| **Output** | Targeted resume for one role | Versatile resume for multiple roles |

## Output

Save to `pipeline_state.json`:
```json
{
  "mode": "standalone",
  "mode_detected_at": "2026-11-23T00:00:00Z",
  "has_job_description": false,
  "has_background": true,
  "execution_plan": {
    "stages": [...],
    "optimization_target": "maximum_impact"
  }
}
```

## User Notification

**JD-Aligned Mode Detected:**
```
🎯 JD-Aligned Mode Activated
   Input: Job description + Background
   Goal: Create targeted resume matching job requirements
   Pipeline: 11 stages with ATS optimization
```

**Standalone Mode Detected:**
```
✨ Standalone Mode Activated
   Input: Background only
   Goal: Create best general-purpose resume
   Pipeline: 9 stages focused on impact maximization
```

## Important Notes

- Mode detection happens BEFORE Stage 1 (Intake)
- Mode cannot be changed mid-execution
- If user wants to switch modes, they must restart the pipeline
- Both modes produce professional, ATS-friendly resumes
- JD-Aligned mode is more targeted; Standalone mode is more versatile
