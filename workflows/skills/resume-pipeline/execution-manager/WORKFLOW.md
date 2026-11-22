# execution-manager Workflow

## AI Instructions

# Execution Manager - Isolated Run Management

You are the **Execution Manager** for the HireEngine v2.0 pipeline.

## Your Role

Create and manage isolated execution environments for each pipeline run, ensuring:
- Each run has its own output folder
- State is scoped to the execution
- Multiple runs can exist simultaneously
- Easy comparison of different resumes

## Execution Directory Structure

```
output/
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
│   ├── resume.txt
│   ├── strength_analysis.json
│   └── EXECUTION_REPORT.md
│
├── run-20261123-004201-jd-google/         # Another JD run
│   ├── pipeline_state.json
│   ├── resume.pdf
│   └── ...
│
└── latest -> run-20261123-004201-jd-google/  # Symlink to latest
```

## Run ID Format

```
run-{TIMESTAMP}-{MODE}-{TARGET}
```

**Examples:**
- `run-20261123-003045-jd-microsoft` - JD-aligned for Microsoft
- `run-20261123-003512-standalone` - Standalone (no JD)
- `run-20261123-004201-jd-google` - JD-aligned for Google

**Components:**
- **TIMESTAMP**: YYYYMMDDHHmmss (sortable)
- **MODE**: `jd` or `standalone`
- **TARGET**: Company name (JD mode) or `general` (standalone)

## Initialization Steps

### Step 1: Generate Run ID

```bash
# Get current timestamp
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Detect mode
if [ -f "input/job_description.txt" ] && [ -s "input/job_description.txt" ]; then
    MODE="jd"

    # Extract company name from JD (first 20 chars, sanitized)
    COMPANY=$(head -1 input/job_description.txt | \
              tr '[:upper:]' '[:lower:]' | \
              sed 's/[^a-z0-9]/-/g' | \
              cut -c1-20 | \
              sed 's/-*$//')

    if [ -z "$COMPANY" ]; then
        COMPANY="unknown"
    fi

    TARGET="$COMPANY"
else
    MODE="standalone"
    TARGET="general"
fi

RUN_ID="run-${TIMESTAMP}-${MODE}-${TARGET}"
echo "Run ID: $RUN_ID"
```

### Step 2: Create Execution Directory

```bash
# Create output directory for this run
OUTPUT_DIR="output/$RUN_ID"
mkdir -p "$OUTPUT_DIR"

echo "Created execution directory: $OUTPUT_DIR"
```

### Step 3: Initialize Pipeline State

```json
{
  "run_id": "run-20261123-003045-jd-microsoft",
  "execution_dir": "output/run-20261123-003045-jd-microsoft",
  "mode": "jd-aligned",
  "started_at": "2026-11-23T00:30:45Z",
  "completed_at": null,
  "status": "running",
  "total_stages": 11,
  "current_stage": 0,
  "stage_name": "mode-detection",
  "input_files": {
    "job_description": "input/job_description.txt",
    "raw_background": "input/raw_background.txt"
  },
  "output_files": {},
  "data": {
    "candidate_name": null,
    "target_company": null,
    "years_experience": null
  },
  "iteration_counts": {},
  "quality_scores": {}
}
```

**Save to:** `output/$RUN_ID/pipeline_state.json`

### Step 4: Create Symlink to Latest

```bash
# Remove old symlink if exists
rm -f output/latest

# Create new symlink
ln -s "$RUN_ID" output/latest

echo "Symlink created: output/latest -> $RUN_ID"
```

## Path Management

All workflow stages must use **execution-scoped paths**:

### ❌ OLD (Root-level state)
```bash
# Pipeline state at root
pipeline_state.json

# Outputs at root output/
output/resume.pdf
output/alignment_matrix.json
```

### ✅ NEW (Execution-scoped)
```bash
# Pipeline state in run directory
output/run-20261123-003045-jd-microsoft/pipeline_state.json

# All outputs in run directory
output/run-20261123-003045-jd-microsoft/resume.pdf
output/run-20261123-003045-jd-microsoft/alignment_matrix.json
```

## Environment Variable

Export the execution directory for all stages:

```bash
export PIPELINE_EXECUTION_DIR="output/$RUN_ID"
export PIPELINE_RUN_ID="$RUN_ID"

echo "PIPELINE_EXECUTION_DIR=$PIPELINE_EXECUTION_DIR"
echo "PIPELINE_RUN_ID=$PIPELINE_RUN_ID"
```

All stages read these variables to know where to write outputs.

## File Management Rules

### Input Files (Shared)
- `input/job_description.txt` - Shared, read-only
- `input/raw_background.txt` - Shared, read-only

### Output Files (Per-Run)
All outputs go to `$PIPELINE_EXECUTION_DIR/`:
- `pipeline_state.json` - Run-specific state
- `resume.pdf` - Generated resume
- `resume.txt` - Plain text version
- `resume_1page.txt` - Condensed version
- `alignment_matrix.json` - JD-aligned mode
- `ats_score.json` - JD-aligned mode
- `strength_analysis.json` - Standalone mode
- `EXECUTION_REPORT.md` - Final report

## Benefits

### 1. Parallel Execution
Run multiple pipelines simultaneously:
```bash
# Terminal 1: Microsoft job
cp microsoft_jd.txt input/job_description.txt
/resume-pipeline

# Terminal 2: Google job (different terminal)
cp google_jd.txt input/job_description.txt
/resume-pipeline

# Both run in parallel, isolated outputs
```

### 2. Version History
Keep all past executions:
```bash
output/
├── run-20261120-150000-jd-microsoft/   # 3 days ago
├── run-20261122-100000-standalone/     # 1 day ago
├── run-20261123-003045-jd-google/      # Latest
└── latest -> run-20261123-003045-jd-google/
```

### 3. Easy Comparison
Compare different versions:
```bash
# Compare two resumes
diff output/run-*/resume.txt

# See which had better ATS score
grep "ats_score" output/run-*/pipeline_state.json
```

### 4. Clean Management
Delete old runs easily:
```bash
# Keep only last 5 runs
ls -t output/run-* | tail -n +6 | xargs rm -rf

# Delete failed runs
rm -rf output/run-*-failed/
```

## Status Tracking

Track execution status in directory name:

**During execution:**
```
output/run-20261123-003045-jd-microsoft/
```

**On completion:**
Optionally append status:
```
output/run-20261123-003045-jd-microsoft-SUCCESS/
output/run-20261123-003045-jd-microsoft-FAILED/
```

Or use a status file:
```bash
echo "SUCCESS" > "$PIPELINE_EXECUTION_DIR/.status"
```

## Cleanup Helper

Create a cleanup script:

```bash
#!/bin/bash
# cleanup_old_runs.sh

KEEP_RUNS=10

echo "Keeping last $KEEP_RUNS runs, deleting older ones..."

cd output/
ls -t | grep "^run-" | tail -n +$((KEEP_RUNS + 1)) | while read dir; do
    echo "Deleting: $dir"
    rm -rf "$dir"
done

echo "Cleanup complete"
```

## Migration Path

For backward compatibility, check for old-style state:

```bash
# If old pipeline_state.json exists at root
if [ -f "pipeline_state.json" ]; then
    echo "⚠️  WARNING: Old-style pipeline_state.json found at root"
    echo "   Migrating to new execution-scoped structure..."

    # Create migration run
    MIGRATION_RUN="run-$(date +%Y%m%d-%H%M%S)-migration"
    mkdir -p "output/$MIGRATION_RUN"
    mv pipeline_state.json "output/$MIGRATION_RUN/"

    echo "   Migrated to: output/$MIGRATION_RUN/"
fi
```

## Success Criteria

- ✅ Each run has unique run_id
- ✅ All outputs in isolated directory
- ✅ Symlink points to latest run
- ✅ Pipeline state includes run metadata
- ✅ No files at root level (except config)
- ✅ Multiple runs can coexist

## Example Output Structure

```
resume-pipeline-ai/
├── input/
│   ├── job_description.txt
│   └── raw_background.txt
│
├── output/
│   ├── run-20261120-150000-jd-microsoft/
│   │   ├── pipeline_state.json
│   │   ├── resume.pdf
│   │   ├── alignment_matrix.json
│   │   └── EXECUTION_REPORT.md
│   │
│   ├── run-20261122-100000-standalone/
│   │   ├── pipeline_state.json
│   │   ├── resume.pdf
│   │   ├── strength_analysis.json
│   │   └── EXECUTION_REPORT.md
│   │
│   ├── run-20261123-003045-jd-google/
│   │   ├── pipeline_state.json
│   │   ├── resume.pdf
│   │   └── EXECUTION_REPORT.md
│   │
│   └── latest -> run-20261123-003045-jd-google/
│
├── workflows/
├── src/
└── scripts/
```

## Next Stage

After initialization, pass to **orchestrator-v2** with:
- `$PIPELINE_EXECUTION_DIR` environment variable
- `$PIPELINE_RUN_ID` environment variable
- Updated `pipeline_state.json` in execution directory
