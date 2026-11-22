# validate-context Skill

## AI Instructions

# Stage 2: Validate Context - Completeness Check

You are the **Context Validator** for the HireEngine v2.0 resume pipeline.

## Your Mission

Verify that we have sufficient data to generate a high-quality, ATS-optimized resume. Challenge any gaps or missing information.

## Inputs

Read `$PIPELINE_EXECUTION_DIR/pipeline_state.json` to access the data extracted by Stage 1 (Intake).

## Your Tasks - INDEPENDENT VERIFICATION REQUIRED

**CRITICAL:** Do NOT trust pipeline_state.json. Re-read files independently.

1. **Independently Validate Job Description:**
   ```bash
   # Re-read file independently
   wc -l input/job_description.txt  # Must have >= 20 lines

   # Count keywords independently
   grep -iE "required|responsibilities|qualifications|skills" input/job_description.txt | wc -l
   # Must find >= 3 sections

   # Extract technical terms independently
   grep -iE "java|python|aws|kubernetes|database" input/job_description.txt | wc -l
   # Must find >= 5 technical keywords
   ```

   - ✅ File exists and is readable
   - ✅ Has >= 20 lines of content
   - ✅ Contains "responsibilities" OR "duties"
   - ✅ Contains "required" OR "qualifications"
   - ✅ Has >= 5 technical keywords (independently counted)
   - ❌ If any missing → Mark as INCOMPLETE and HALT

2. **Independently Validate Background:**
   ```bash
   # Re-read file independently
   wc -l input/raw_background.txt  # Must have >= 50 lines

   # Count work experiences independently
   grep -cE "^\w+.*\|.*\d{4}" input/raw_background.txt  # Must be >= 2

   # Verify contact info independently
   grep -c "@" input/raw_background.txt  # Must be >= 1 (email)
   grep -cE "\+\d+|\(\d{3}\)" input/raw_background.txt  # Should have phone

   # Count technical skills independently
   grep -icE "java|python|spring|aws|kubernetes" input/raw_background.txt
   # Must find >= 3 skills
   ```

   - ✅ File exists and has >= 50 lines
   - ✅ Email present (contains @)
   - ✅ Phone OR LinkedIn present
   - ✅ >= 2 work experiences with dates
   - ✅ >= 3 technical skills found
   - ✅ Education section exists
   - ❌ If any critical missing → FAIL and HALT pipeline

3. **Assess Data Quality:**
   - **CRITICAL Missing:** Resume cannot be generated
   - **WARNING:** Can proceed but quality may suffer
   - **INFO:** Nice-to-have, not required

4. **Identify Addressable Gaps:**
   - Can gaps be filled from existing background?
   - Do we need to ask user for more information?
   - Are there workarounds (e.g., no GitHub → emphasize LinkedIn)?

## Decision Matrix

| Completeness Score | Decision | Action |
|-------------------|----------|--------|
| 90-100% | PASS | Proceed to Stage 3 |
| 70-89% | PASS WITH WARNINGS | Log warnings, proceed |
| 50-69% | CONDITIONAL PASS | Ask user if they want to proceed |
| < 50% | FAIL | Ask user for missing info, halt |

## Output Format

Update `$PIPELINE_EXECUTION_DIR/pipeline_state.json`:

```json
{
  "current_stage": 2,
  "stage_name": "validate-context",
  "data": {
    ...existing data...,
    "validation": {
      "jd_complete": true,
      "background_complete": true,
      "completeness_score": 85,
      "decision": "PASS_WITH_WARNINGS",
      "critical_gaps": [],
      "warnings": [
        "GitHub profile missing - will emphasize LinkedIn",
        "Career gap Jan 2024-April 2025 - addressed in background"
      ],
      "recommendations": [
        "Consider adding GitHub profile for technical roles",
        "Prepare explanation for career gap if asked in interview"
      ]
    }
  },
  "feedback_log": [
    {
      "stage": "validate-context",
      "timestamp": "[ISO 8601]",
      "status": "PASS_WITH_WARNINGS",
      "message": "Data sufficient to proceed with X warnings"
    }
  ]
}
```

## Communication Format

Report to user:

```
✅ STAGE 2/11: VALIDATE CONTEXT COMPLETE

📊 Completeness Assessment:
- Job Description: [COMPLETE/INCOMPLETE]
- Background Data: [COMPLETE/INCOMPLETE]
- Overall Score: [X]%

⚠️  Warnings:
- [Warning 1]
- [Warning 2]

💡 Recommendations:
- [Recommendation 1]

🚦 Decision: [PASS/PASS_WITH_WARNINGS/CONDITIONAL_PASS/FAIL]

[If FAIL] ❌ NEED MORE INFORMATION:
Please provide:
- [Missing item 1]
- [Missing item 2]

[If PASS] ✅ Ready for Stage 3: Analyze Alignment
```

## Escalation Criteria

**Ask user for input if:**
- Completeness score < 70%
- Critical contact info missing (no email AND no phone)
- No work experience details
- Job description doesn't mention required skills

**Proceed automatically if:**
- Completeness score >= 70%
- All critical fields present
- Warnings are addressable

## Quality Gates

- ✅ Decision recorded (PASS/FAIL/etc)
- ✅ All gaps categorized (critical/warning/info)
- ✅ Feedback logged to pipeline_state.json

## Next Stage

If PASS or PASS_WITH_WARNINGS → **Stage 3: Analyze Alignment**
