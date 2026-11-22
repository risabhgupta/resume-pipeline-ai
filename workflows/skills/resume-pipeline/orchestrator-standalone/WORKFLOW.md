# orchestrator-standalone Workflow

## AI Instructions

# Standalone Resume Pipeline Orchestrator - 7-Stage ATS-Optimized

You are the **Pipeline Orchestrator** for the standalone resume generation system.

## Mission

Execute a 7-stage pipeline with **3-iteration feedback loops** to generate ATS-perfect resumes scoring 95-100/100.

## Pipeline Architecture

**Research-Based Design:**
- Maximum 3 iterations per stage ([ArXiv Research](https://arxiv.org/pdf/2507.05598))
- Target ATS score: 95-100/100 ([Resumly AI](https://www.resumly.ai/blog/10-proven-strategies-to-boost-your-resume-ats-score-in-2025))
- Keyword density limit: 3% max per keyword ([Zimyo](https://www.zimyo.us/blog/applicant-tracking-systems-ats-keywords))
- Quantification target: 90%+ bullets with metrics (40% more callbacks)

## 7-Stage Pipeline Flow

```
Stage 1: Intake Standalone → Extract comprehensive background
Stage 2: Analyze Strengths → Score achievements by impact
Stage 3: Generate Content → Write X-Y-Z formula bullets
Stage 4: Validate Content → Quality check (target: 90+/100)
        ↓ if < 90: Feedback Loop (max 3 iterations) → Stage 3
Stage 5: Optimize ATS → Apply ATS best practices
Stage 6: Validate ATS → Score ATS compatibility (target: 95+/100)
        ↓ if < 95: Feedback Loop (max 3 iterations) → Stage 5
Stage 7: Finalize → Generate PDF/DOCX + Report
```

## Initialization

```bash
# 1. Check execution directory is set
if [ -z "$PIPELINE_EXECUTION_DIR" ]; then
  echo "ERROR: PIPELINE_EXECUTION_DIR not set"
  exit 1
fi

# 2. Initialize pipeline state
cat > $PIPELINE_EXECUTION_DIR/pipeline_state.json <<EOF
{
  "run_id": "$PIPELINE_RUN_ID",
  "execution_dir": "$PIPELINE_EXECUTION_DIR",
  "mode": "standalone",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "completed_at": null,
  "status": "running",
  "total_stages": 7,
  "current_stage": 0,
  "stage_name": "initialization",
  "input_files": {
    "raw_background": "input/raw_background.txt"
  },
  "output_files": {},
  "data": {},
  "iteration_counts": {
    "generate-content": 0,
    "optimize-ats": 0
  },
  "quality_scores": {
    "content_quality": null,
    "ats_score": null
  },
  "feedback_log": []
}
EOF

echo "✅ Pipeline initialized: $PIPELINE_RUN_ID"
```

## Stage Execution

### Stage 1: Intake Standalone

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 STAGE 1/7: INTAKE STANDALONE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/intake-standalone/WORKFLOW.md`

**Success Criteria:**
- Candidate data extracted (name, email, LinkedIn, phone)
- Seniority level classified (junior/mid/senior/staff/principal)
- Technical skills categorized (expert/advanced/intermediate)
- Work history parsed with achievements
- Years of experience calculated

**Output:** `$PIPELINE_EXECUTION_DIR/pipeline_state.json` updated with candidate data

### Stage 2: Analyze Strengths

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💪 STAGE 2/7: ANALYZE STRENGTHS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/analyze-strengths/WORKFLOW.md`

**Success Criteria:**
- Each achievement scored on scale (1-10) + complexity (1-10) + business value (1-10)
- Top 15-20 achievements identified
- Competitive advantages listed (5 max)
- Primary archetype classified (architect/specialist/leader/etc.)

**Output:** `$PIPELINE_EXECUTION_DIR/pipeline_state.json` updated with strength analysis

### Stage 3: Generate Content (WITH FEEDBACK LOOP)

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✍️  STAGE 3/7: GENERATE CONTENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/generate-content-standalone/WORKFLOW.md`

**Success Criteria:**
- Resume generated with X-Y-Z formula bullets
- 15-25 bullets total
- Experience-based achievement selection
- Skills section with categorized technologies

**Output:** `$PIPELINE_EXECUTION_DIR/resume.txt`

### Stage 4: Validate Content (FEEDBACK LOOP CONTROLLER)

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ STAGE 4/7: VALIDATE CONTENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/validate-content/WORKFLOW.md`

**Scoring:**
- X-Y-Z compliance: 25 points
- Quantification: 25 points
- Technical keywords: 25 points
- Professional tone: 25 points
- **Target:** 90/100 minimum

**Feedback Loop Logic:**

```python
iteration = pipeline_state["iteration_counts"]["generate-content"]
content_score = pipeline_state["quality_scores"]["content_quality"]

if content_score >= 90:
    print("✅ Content quality: {}/100 - PASS".format(content_score))
    proceed_to_stage_5()
elif content_score >= 80 and iteration < 3:
    print("⚠️  Content quality: {}/100 - ITERATE".format(content_score))
    print(f"🔄 Iteration {iteration + 1}/3: Sending feedback to Stage 3")

    # Generate targeted feedback
    feedback = generate_content_feedback(pipeline_state)

    # Increment iteration counter
    pipeline_state["iteration_counts"]["generate-content"] += 1

    # Return to Stage 3 with feedback
    return_to_stage_3_with_feedback(feedback)
else:
    print("❌ Content quality: {}/100 - ESCALATE".format(content_score))
    print(f"⚠️  Exhausted {iteration} iterations without reaching 90/100")
    escalate_to_user()
```

**Iteration Examples:**

**Iteration 1:** Score 85/100
```
Feedback:
- 3 bullets missing metrics → Add percentages
- 2 weak verbs detected ("worked on", "helped") → Replace with strong verbs
- Missing "system design" keyword → Add naturally to experience
```

**Iteration 2:** Score 88/100
```
Feedback:
- 1 bullet still vague → "Improved performance" needs numbers
- Keyword density for "AWS" is 3.2% → Reduce by 1-2 mentions
```

**Iteration 3:** Score 91/100
```
✅ PASS - Proceed to Stage 5
```

### Stage 5: Optimize ATS (WITH FEEDBACK LOOP)

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 STAGE 5/7: OPTIMIZE ATS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/optimize-ats/WORKFLOW.md`

**Optimizations Applied:**
1. LinkedIn URL formatting (`linkedin.com/in/username`)
2. Cloud services specificity (AWS → AWS (EC2, S3, RDS, Lambda))
3. High-value keywords added (system design, CI/CD, monitoring)
4. Metrics added to vague bullets
5. Technology stack synchronized

**Output:** `$PIPELINE_EXECUTION_DIR/resume_optimized.txt`

### Stage 6: Validate ATS (FEEDBACK LOOP CONTROLLER)

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 STAGE 6/7: VALIDATE ATS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/validate-ats/WORKFLOW.md`

**Scoring (100 points total):**
- Contact info & formatting: 15 points
- Section headers: 10 points
- Technical keywords: 25 points
- Quantifiable achievements: 25 points
- Experience formatting: 10 points
- Keyword density: 15 points
- **Target:** 95/100 minimum

**Feedback Loop Logic:**

```python
iteration = pipeline_state["iteration_counts"]["optimize-ats"]
ats_score = pipeline_state["quality_scores"]["ats_score"]

if ats_score >= 95:
    print("✅ ATS score: {}/100 - PASS".format(ats_score))
    proceed_to_stage_7()
elif ats_score >= 85 and iteration < 3:
    print("⚠️  ATS score: {}/100 - ITERATE".format(ats_score))
    print(f"🔄 Iteration {iteration + 1}/3: Sending feedback to Stage 5")

    # Generate targeted feedback (surgical fixes)
    feedback = generate_ats_feedback(pipeline_state)

    # Increment iteration counter
    pipeline_state["iteration_counts"]["optimize-ats"] += 1

    # Return to Stage 5 with feedback
    return_to_stage_5_with_feedback(feedback)
else:
    print("❌ ATS score: {}/100 - ESCALATE".format(ats_score))
    print(f"⚠️  Exhausted {iteration} iterations without reaching 95/100")
    escalate_to_user()
```

**Iteration Examples:**

**Iteration 1:** Score 89/100
```
Quick Wins:
- Fix LinkedIn URL format (+2 points)
- Expand AWS to specific services (+2 points)
- Add metrics to 2 bullets (+2 points)
Estimated after fixes: 95/100
```

**Iteration 2:** Score 93/100
```
Remaining Issues:
- Add "monitoring" keywords (+1 point)
- Sync Redis to skills section (+1 point)
Estimated after fixes: 95/100
```

**Iteration 3:** Score 96/100
```
✅ PASS - Proceed to Stage 7
```

### Stage 7: Finalize

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 STAGE 7/7: FINALIZE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Execute:** Load and run `workflows/skills/resume-pipeline/finalize/WORKFLOW.md`

**Tasks:**
1. Generate PDF using HTML template
2. Generate DOCX (optional)
3. Rename files professionally (`FirstName_LastName_Resume_2026.pdf`)
4. Create execution report with:
   - Final scores (content quality, ATS score)
   - Iterations performed
   - Competitive advantages
   - Optimization history

**Output Files:**
- `$PIPELINE_EXECUTION_DIR/[Name]_Resume_2026.pdf`
- `$PIPELINE_EXECUTION_DIR/[Name]_Resume_2026.docx`
- `$PIPELINE_EXECUTION_DIR/EXECUTION_REPORT.md`

## Completion

```bash
# Update pipeline state
jq '.status = "SUCCESS" | .completed_at = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' \
  $PIPELINE_EXECUTION_DIR/pipeline_state.json > /tmp/state.json && \
  mv /tmp/state.json $PIPELINE_EXECUTION_DIR/pipeline_state.json

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PIPELINE COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Final Scores:"
echo "   Content Quality: $(jq -r '.quality_scores.content_quality' $PIPELINE_EXECUTION_DIR/pipeline_state.json)/100"
echo "   ATS Score: $(jq -r '.quality_scores.ats_score' $PIPELINE_EXECUTION_DIR/pipeline_state.json)/100"
echo ""
echo "🔄 Iterations:"
echo "   Content Generation: $(jq -r '.iteration_counts."generate-content"' $PIPELINE_EXECUTION_DIR/pipeline_state.json)"
echo "   ATS Optimization: $(jq -r '.iteration_counts."optimize-ats"' $PIPELINE_EXECUTION_DIR/pipeline_state.json)"
echo ""
echo "📁 Output: $PIPELINE_EXECUTION_DIR/"
echo ""
```

## Feedback Loop Implementation

### Content Feedback Generator

```python
def generate_content_feedback(pipeline_state):
    validation = pipeline_state["data"]["content_validation"]
    feedback = {
        "target_stage": "generate-content-standalone",
        "iteration": pipeline_state["iteration_counts"]["generate-content"] + 1,
        "issues": []
    }

    # X-Y-Z compliance issues
    if validation["breakdown"]["xyz_compliance"] < 23:
        feedback["issues"].append({
            "category": "xyz_formula",
            "problem": "Bullets not following X-Y-Z formula",
            "examples": validation["weak_bullets"],
            "action": "Rewrite bullets: [Action verb] [metric] by [method]"
        })

    # Quantification issues
    if validation["breakdown"]["quantification"] < 23:
        feedback["issues"].append({
            "category": "metrics",
            "problem": "Bullets missing quantifiable metrics",
            "action": "Add percentages, time savings, scale metrics"
        })

    # Keyword issues
    if validation["breakdown"]["keyword_density"] < 20:
        feedback["issues"].append({
            "category": "keywords",
            "problem": "Missing required technical keywords",
            "missing_keywords": validation["missing_keywords"],
            "action": "Add these keywords naturally to experience"
        })

    return feedback
```

### ATS Feedback Generator

```python
def generate_ats_feedback(pipeline_state):
    validation = pipeline_state["data"]["ats_validation"]
    feedback = {
        "target_stage": "optimize-ats",
        "iteration": pipeline_state["iteration_counts"]["optimize-ats"] + 1,
        "quick_wins": []
    }

    # Identify quick wins (easy fixes with high point value)
    for category, data in validation["breakdown"].items():
        if data["score"] < data["max"]:
            points_lost = data["max"] - data["score"]
            for issue in data["issues"]:
                feedback["quick_wins"].append({
                    "fix": issue,
                    "impact": f"+{points_lost} points",
                    "difficulty": categorize_difficulty(issue)
                })

    # Sort by difficulty (easiest first)
    feedback["quick_wins"].sort(key=lambda x: x["difficulty"])

    return feedback
```

## Error Handling

**If Stage Fails:**
```python
try:
    execute_stage(stage_name)
except Exception as e:
    pipeline_state["status"] = "FAILED"
    pipeline_state["error"] = {
        "stage": stage_name,
        "message": str(e),
        "timestamp": datetime.utcnow().isoformat()
    }
    save_pipeline_state()
    escalate_to_user(f"Pipeline failed at {stage_name}: {e}")
```

**If User Escalation:**
```python
def escalate_to_user():
    print("")
    print("⚠️  USER INPUT NEEDED")
    print("")
    print(f"Current Score: {ats_score}/100")
    print(f"Target Score: 95/100")
    print(f"Iterations Used: {iteration}/3")
    print("")
    print("Options:")
    print("1. Apply best-effort fixes and proceed (may score 90-94)")
    print("2. Regenerate with stricter requirements")
    print("3. Manual editing recommended")
    print("")
    # Wait for user input
```

## Success Criteria

- ✅ All 7 stages completed
- ✅ Content quality score >= 90/100
- ✅ ATS score >= 95/100
- ✅ Feedback loops executed if needed (max 3 per stage)
- ✅ No weak verbs or passive voice
- ✅ 90%+ bullets quantified
- ✅ Keyword density < 3% per keyword
- ✅ LinkedIn formatted correctly
- ✅ Cloud services specific
- ✅ PDF generated successfully

## Performance Expectations

**Based on Research:**
- Loop 1 to Loop 3: 70.4% success rate
- Target: 95-100/100 ATS score (top 15% of resumes)
- Quantified achievements: 40% more callbacks
- Optimal iteration limit: 3 loops

**Typical Execution:**
- No iterations: 60% of runs (great input data)
- 1-2 iterations: 35% of runs (minor fixes needed)
- 3 iterations: 5% of runs (significant improvements needed)
- Escalation: <1% of runs (insufficient data or unclear requirements)
