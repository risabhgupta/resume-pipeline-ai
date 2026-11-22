# Resume Pipeline - Independent Validation Framework

## Core Principle: Zero Trust Between Stages

**CRITICAL RULE:** Each validation stage must independently verify its inputs and outputs without trusting previous stages.

---

## Stage 2: Validate Context - Strengthened Requirements

### Independent Checks (Do NOT trust intake stage)

1. **Re-read files independently**
   ```bash
   # Don't trust pipeline_state.json extraction
   # Read files fresh
   wc -l input/job_description.txt  # Must have > 20 lines
   wc -l input/raw_background.txt   # Must have > 50 lines
   ```

2. **Verify JD completeness independently**
   - Count keywords independently: `grep -iE "required|responsibilities|qualifications" input/job_description.txt | wc -l`
   - Must find >= 3 sections
   - Extract and count technical keywords independently (not from alignment stage)

3. **Verify background completeness independently**
   - Count work experiences: `grep -E "^\w+ \d{4}" input/raw_background.txt | wc -l` >= 2
   - Verify contact: `grep -E "@|phone|\+\d+" input/raw_background.txt | wc -l` >= 2
   - Count skills independently: `grep -i "java\|python\|spring" input/raw_background.txt | wc -l` >= 3

4. **Fail early if incomplete**
   - If completeness < 70%, HALT pipeline immediately
   - Don't let garbage propagate through stages

---

## Stage 4: Validate Alignment - Strengthened Requirements

### Independent Checks (Do NOT trust analyzer)

1. **Re-verify alignment_matrix.json exists and is valid JSON**
   ```bash
   jq . output/alignment_matrix.json > /dev/null || exit 1
   ```

2. **Independently verify keyword claims**
   - For EACH "matched" keyword in alignment matrix:
     ```bash
     keyword="prompt engineering"
     grep -i "$keyword" input/raw_background.txt || echo "FALSE MATCH"
     ```
   - If > 20% of claimed matches are false → REJECT alignment

3. **Independently verify optimization strategies are truthful**
   - For each strategy marked "addressable":
     - Verify evidence exists in background
     - Reject any strategy without grep-verified evidence

4. **Independently check match rate calculation**
   - Recalculate from scratch
   - If differs from analyzer by > 5% → REJECT

---

## Stage 6: Validate Content - CRITICAL Independent Validation

### Independent Checks (Do NOT trust generator)

1. **Re-read resume.txt independently**
   ```bash
   wc -w output/resume.txt  # Verify word count
   ```

2. **Count bullets independently**
   ```bash
   grep -c "^•\|^-" output/resume.txt
   # Must match expected count (15-25 for typical resume)
   ```

3. **Verify EACH bullet independently for X-Y-Z formula**
   ```bash
   # Extract bullets
   grep "^•\|^-" output/resume.txt > /tmp/bullets.txt

   # Check each bullet has:
   # - Action verb (Architected, Built, Designed, etc.)
   # - Metric (%, number, time)
   # - Method (by doing X, using Y, through Z)
   ```

4. **Independently verify keyword presence**
   ```bash
   # For each top-10 JD keyword
   for keyword in "Java" "Spring Boot" "Microservices"; do
     grep -i "$keyword" output/resume.txt || echo "MISSING: $keyword"
   done
   ```

5. **Independently scan for weak verbs**
   ```bash
   grep -E "worked on|helped|assisted|participated|involved|responsible for" output/resume.txt
   # If any found → FAIL immediately
   ```

6. **Fail fast on quality issues**
   - If ANY bullet lacks X-Y-Z → Score = 0 for that component
   - If weak verbs detected → Professional Tone = 0
   - Don't proceed with bad content

---

## Stage 7: Score ATS - Independent Calculation

### Independent Checks (Do NOT trust content validator)

1. **Independently re-read resume.txt**

2. **Independently extract and count section headers**
   ```bash
   grep -E "^(SKILLS|EXPERIENCE|EDUCATION|PROJECTS)" output/resume.txt
   # Verify standard headers independently
   ```

3. **Independently extract contact info**
   ```bash
   grep -E "@" output/resume.txt  # Email
   grep -E "\+\d+|\(\d{3}\)" output/resume.txt  # Phone
   # Don't trust validator claims
   ```

4. **Independently calculate keyword match**
   - Re-extract JD keywords from scratch
   - Re-count matches in resume.txt
   - Calculate match rate independently
   - If differs from alignment stage by > 10% → Flag warning

5. **Independently verify formatting**
   - Check for tables: `grep -E "^\|" output/resume.txt` (should be 0)
   - Check for images: (not applicable for .txt)

---

## Stage 10: Validate Format - CRITICAL Content Verification

### Independent Checks (Do NOT trust formatter)

**This is where the critical bug was found. Make these checks MANDATORY:**

1. **Independently verify PDF exists**
   ```bash
   test -f output/*.pdf || exit 1
   ls -lh output/*.pdf
   ```

2. **Independently verify page count**
   ```bash
   pdfinfo output/*.pdf | grep "Pages:"
   # MUST be exactly 1 page
   # If != 1 → FAIL immediately
   ```

3. **CRITICAL: Independently verify content completeness**
   ```bash
   # Count bullets in source
   source_bullets=$(grep -c "^•\|^-" output/resume.txt)

   # Extract PDF text
   pdftotext output/*.pdf /tmp/pdf_text.txt

   # Count content in PDF (bullets may appear as - or • or · in PDF)
   pdf_bullets=$(grep -E "•|–|reducing|built|designed|developed" /tmp/pdf_text.txt | wc -l)

   # MUST have >= 80% of source bullets
   min_required=$((source_bullets * 80 / 100))

   if [ $pdf_bullets -lt $min_required ]; then
     echo "CRITICAL FAILURE: PDF missing bullets"
     echo "Source: $source_bullets bullets"
     echo "PDF: $pdf_bullets bullets"
     exit 1
   fi
   ```

4. **Independently verify each role has content**
   ```bash
   # For each company name in source
   for company in "WEX" "Microsoft" "OLA" "Freecharge"; do
     grep -A 5 "$company" /tmp/pdf_text.txt | grep -E "reducing|built|designed" || echo "MISSING BULLETS FOR $company"
   done
   ```

5. **Independently verify skills section**
   ```bash
   pdftotext output/*.pdf - | grep -A 10 "SKILLS\|TECHNICAL SKILLS" | grep "Java\|Spring\|Python" || echo "MISSING SKILLS"
   ```

6. **Independently verify extractability**
   ```bash
   # Extract text and verify critical elements
   pdf_text=$(pdftotext output/*.pdf -)
   echo "$pdf_text" | grep -i "aman gupta" || exit 1
   echo "$pdf_text" | grep "@" || exit 1
   echo "$pdf_text" | wc -w  # Must be > 400 words
   ```

7. **Fail immediately if content missing**
   - Don't proceed to finalize if PDF is empty or incomplete
   - Regenerate with fixes

---

## General Framework Improvements

### 1. Add Validation Logging

Each validation stage must log:
```json
{
  "stage": "validate-format",
  "timestamp": "ISO-8601",
  "checks_performed": [
    {"check": "page_count", "expected": 1, "actual": 1, "result": "PASS"},
    {"check": "bullet_count", "expected": 19, "actual": 19, "result": "PASS"},
    {"check": "content_completeness", "expected": "> 80%", "actual": "100%", "result": "PASS"}
  ],
  "independent_verification": true,
  "trusted_previous_stage": false
}
```

### 2. Add Cross-Stage Consistency Checks

After each stage, verify consistency:
```bash
# Example: After Stage 7 (Score ATS)
# Verify ATS score makes sense given content quality score
if [ $ats_score -gt $content_quality ]; then
  echo "WARNING: ATS score ($ats_score) > Content quality ($content_quality)"
  echo "This is suspicious - verify independently"
fi
```

### 3. Add Checksum Verification

Track file checksums to detect unexpected changes:
```bash
# After resume.txt generated
source_checksum=$(md5sum output/resume.txt | awk '{print $1}')

# Before PDF generation
current_checksum=$(md5sum output/resume.txt | awk '{print $1}')

if [ "$source_checksum" != "$current_checksum" ]; then
  echo "ERROR: resume.txt modified unexpectedly"
  exit 1
fi
```

### 4. Add Bullet-Level Validation

Don't just count bullets - validate each one:
```python
def validate_bullet_independently(bullet_text):
    checks = {
        'has_action_verb': bool(re.match(r'^(Architected|Built|Designed|Developed|Optimized|Created|Led|Improved|Reduced|Scaled|Implemented)', bullet_text)),
        'has_metric': bool(re.search(r'\d+%|\d+[KM]\+?|99\.\d+%|\d+ (transactions|pipelines|engineers)', bullet_text)),
        'has_method': bool(re.search(r' by | using | through | via | with | implementing ', bullet_text)),
        'no_weak_verbs': not re.search(r'worked on|helped|assisted|participated|involved|responsible for', bullet_text, re.I),
        'length_ok': 50 <= len(bullet_text) <= 250
    }
    return all(checks.values()), checks
```

### 5. Add Validation Summary Report

After each validation stage, create independent summary:
```markdown
## Stage X Validation Summary

### Independent Checks Performed: 8
### Checks Passed: 7
### Checks Failed: 1
### Checks Skipped: 0

### Failed Check Details:
- bullet_count_match: Expected 19, Found 0 in PDF
- **Action Required:** Regenerate PDF with fixed parser

### Confidence Score: 87% (based on independent verification)
```

---

## Bug Prevention Checklist

Before marking any validation stage as PASS:

- [ ] I re-read all input files independently (not from cache/state)
- [ ] I verified data with grep/wc/shell commands (not just Python logic)
- [ ] I compared actual vs expected values numerically
- [ ] I tested failure scenarios (what if input is empty/corrupted?)
- [ ] I logged all verification steps with actual values
- [ ] I did NOT trust previous stage outputs without verification
- [ ] I failed fast on critical issues (didn't let bad data propagate)
- [ ] I provided specific error messages (not generic "validation failed")

---

## Implementation Priority

1. **CRITICAL (Do immediately):**
   - Fix Stage 10 content completeness check (DONE)
   - Add bullet counting to Stage 10
   - Add independent role verification to Stage 10

2. **HIGH (Do next):**
   - Add independent keyword verification to Stage 4
   - Add independent X-Y-Z verification to Stage 6
   - Add checksum tracking between stages

3. **MEDIUM (Do soon):**
   - Add cross-stage consistency checks
   - Add detailed validation logging
   - Add validation summary reports

4. **LOW (Nice to have):**
   - Add automated regression tests
   - Add validation confidence scores
   - Add validation replay capability

---

## Testing the Framework

Create test scenarios to verify validations work:

### Test 1: Empty Bullets
```bash
# Create resume.txt with role headers but no bullets
# Expected: Stage 6 should FAIL with "No bullets found"
```

### Test 2: Keyword Stuffing
```bash
# Create resume with keywords but no context
# Expected: Stage 4 should detect and reject
```

### Test 3: Weak Verbs
```bash
# Create bullets starting with "Worked on"
# Expected: Stage 6 should FAIL immediately
```

### Test 4: PDF Missing Content
```bash
# Simulate PDF generation failure
# Expected: Stage 10 should FAIL with specific error
```

---

## Version History

- **v1.0** (2026-10-25): Initial validation framework (had trust issues)
- **v2.0** (2026-10-25): Independent validation framework (zero trust)
  - Added mandatory content verification at Stage 10
  - Added bullet counting and role verification
  - Fixed HTML parser bullet detection bug
  - Added independent re-verification at each stage

---

## Maintenance

This framework must be reviewed and updated:
- After every pipeline bug is found
- After every validation failure in production
- Monthly to ensure checks remain relevant

**Last Updated:** 2026-10-25
**Next Review Due:** 2026-11-25
