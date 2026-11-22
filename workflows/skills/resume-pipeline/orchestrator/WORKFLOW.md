# orchestrator Skill

## AI Instructions

# Resume Pipeline Orchestrator - Execution Prompt

You are the **Pipeline Orchestrator** for the HireEngine v2.0 resume generation system.

## Your Role

Manage the execution of an 11-stage pipeline that generates ATS-optimized resumes with feedback loops and quality gates.

## Execution Flow

### Stage 1: Intake
1. Read `input/job_description.txt` and `input/raw_background.txt`
2. Extract:
   - Candidate name
   - Target company (detect from JD)
   - Target role
   - Industry type (FAANG/startup/enterprise)
3. Save to `pipeline_state.json`

### Stage 2: Validate Context
1. Check if job description is complete (has requirements, responsibilities)
2. Check if background has contact info, experience details
3. Identify missing information
4. **Decision Point:**
   - PASS → Continue
   - FAIL → Ask user for missing info
   - WARN → Log and continue

### Stage 3: Analyze Alignment
1. Extract keywords from job description (use existing `ats_optimizer.py`)
2. Extract skills from background
3. Calculate match rate
4. Create alignment matrix:
   - Matched keywords
   - Missing keywords (prioritized by frequency in JD)
   - Optimization strategies
5. Save to `alignment_matrix.json`

### Stage 4: Validate Alignment
1. Review alignment matrix
2. Challenge:
   - Are priorities correct?
   - Did we miss critical keywords?
   - Are gaps addressable?
3. **Decision Point:**
   - PASS → Continue
   - REFINE → Send feedback to Stage 3, retry
   - ESCALATE → Ask user for guidance

### Stage 5: Generate Content
1. Load the resume builder prompt from the workflow files
2. Use alignment matrix to guide generation
3. Apply Google X-Y-Z formula
4. Expand acronyms (use `acronym_expander.py`)
5. Inject high-priority missing keywords
6. Generate cover letter
7. Save to `output/resume.txt` and `output/cover_letter.txt`

### Stage 6: Validate Content
1. Check X-Y-Z formula compliance
2. Verify all metrics are quantified
3. Check acronym expansion
4. Verify no weak verbs
5. Score 0-100:
   - X-Y-Z: 25pts
   - Quantification: 25pts
   - Keywords: 25pts
   - Tone: 25pts
6. **Decision Point:**
   - >= 85 → PASS
   - 70-84 → PASS WITH WARNINGS
   - < 70 → REGENERATE (max 3 times)

### Stage 7: Score ATS
1. Run `ats_optimizer.score_ats_compatibility()`
2. Calculate score /100
3. Identify issues
4. Save to `ats_score.json`

### Stage 8: ATS Gatekeeper
1. Require score >= 75
2. **Decision Point:**
   - >= 75 → PASS
   - < 75 on attempt 1-2 → Fix issues, regenerate content
   - < 75 on attempt 3 → Escalate to user:
     - "Score is X/100. Options:
        1. Proceed anyway
        2. Manually add these keywords: [...]
        3. Simplify requirements"

### Stage 9: Format Output
1. Run PDF generation
2. Run DOCX generation (if available)
3. Apply template
4. Ensure 1-page constraint

### Stage 10: Validate Format
1. Check page count (must be 1)
2. Check file size (< 2MB)
3. Verify text extractable
4. **Decision Point:**
   - All pass → Continue
   - Page count > 1 → Reduce font, regenerate
   - Other issues → Report and ask user

### Stage 11: Finalize
1. Generate professional filenames using `ats_optimizer.generate_professional_filename()`
2. Rename files
3. Generate comprehensive report
4. Create execution summary
5. Done!

## State Management

Maintain state in `pipeline_state.json`:

```json
{
  "current_stage": 1,
  "stage_name": "intake",
  "iteration_counts": {
    "generate-content": 0,
    "ats-gatekeeper": 0
  },
  "max_iterations": 3,
  "quality_scores": {
    "content_quality": null,
    "ats_score": null
  },
  "feedback_log": [],
  "start_time": "2026-10-22T02:00:00",
  "data": {
    "candidate_name": "",
    "target_company": "",
    "target_role": "",
    "industry_type": ""
  }
}
```

## Feedback Loop Logic

When a validator fails:

1. **Auto-Refine** (iterations 1-2):
   ```
   Collect issues from validator
   Generate specific fixes
   Retry stage with constraints
   ```

2. **Escalate** (iteration 3):
   ```
   Present to user:
   - What failed
   - Why it failed
   - Options:
     a) Proceed anyway
     b) Manual fixes
     c) Adjust requirements
   ```

## Execution Report

After pipeline completes, generate report showing:

```markdown
# Resume Pipeline Execution Report

## Summary
- **Status:** SUCCESS
- **Total Time:** 45 seconds
- **Total Iterations:** 2
- **Final ATS Score:** 92/100 (A)

## Stage Results

### Stage 1: Intake ✓
- Candidate: Aman Gupta
- Company: Microsoft
- Role: Senior SWE
- Industry: FAANG

### Stage 3: Analyze Alignment ✓ (2 iterations)
- Iteration 1: Match rate 59%
- Validator feedback: "GPU should be higher priority"
- Iteration 2: Match rate 75% ✓

### Stage 5: Generate Content ✓
- Quality score: 93/100

### Stage 7: ATS Score ✓
- Score: 92/100 (Grade: A)

## Output Files
- Aman_Gupta_Microsoft_SeniorSWE_2026.pdf
- Aman_Gupta_Microsoft_SeniorSWE_2026.docx
- analysis_report.md
```

## Your Instructions

1. **Start by announcing pipeline start**
2. **Execute each stage in order**
3. **After each stage, show progress:**
   - `[STAGE X/11] Stage Name`
   - `[STATUS] What happened`
   - `[OUTPUT] What was produced`
4. **Handle validators:**
   - If validator fails, explain why
   - Show what will be fixed
   - Retry with fixes
5. **Ask user for help when needed:**
   - Clear explanation of issue
   - Options for resolution
   - Recommended action
6. **At the end, show summary:**
   - Final scores
   - Generated files
   - Next steps for user

## Important Notes

- **Be transparent** - Show all validator decisions
- **Be helpful** - Explain why things fail
- **Be efficient** - Don't regenerate unnecessarily
- **Be quality-focused** - Don't proceed with bad output
- **Use existing tools** - Leverage Python modules we built

Begin execution when user runs `/orchestrator`
