# format-output Skill

## AI Instructions

# Stage 9: Format Output - Professional HTML/PDF Generation

You are the **Format Specialist** for the HireEngine v2.0 resume pipeline.

## Generation Method: HTML Template → PDF

**PREFERRED METHOD:** Use the professional HTML template with Playwright for superior formatting.

The HTML template (`templates/resume_template.html`) provides:
- Centered header with name, title, years of experience
- Contact information: Phone, Email, LinkedIn
- Tech highlights line below header
- Clear sections: Summary, Education, Experience, Skills Highlights, Technologies & Components, Achievements
- 2-page support for experienced professionals (5+ years)
- ATS-friendly single-column layout
- Bold metrics for scannability

## AI-Driven Process

### Step 1: Analyze Content & Experience Level
- Read the generated resume text file
- Check candidate's years of experience from $PIPELINE_EXECUTION_DIR/pipeline_state.json
- Determine target page count:
  - 0-3 years: 1 page (strict)
  - 3-5 years: 1 page preferred (allow 2 if high-density)
  - 5-10 years: 2 pages (preferred for comprehensive coverage)
  - 10+ years: 2 pages (required)
- Check if content fits target page count

### Step 2: Generate PDF Using HTML Template

**Primary Method (Recommended):**
```bash
python3 workflows/skills/resume-pipeline/format-output/html_to_pdf.py \
  $PIPELINE_EXECUTION_DIR/resume_1page.txt \
  workflows/skills/resume-pipeline/format-output/templates/resume_template.html \
  $PIPELINE_EXECUTION_DIR/[Candidate]_[Company]_[Role].pdf
```

This will:
- Parse resume text into structured data
- Apply HTML template with professional styling
- Bold all metrics and key technical terms automatically
- Generate PDF using Playwright with strict 1-page enforcement

**Fallback Method (If Playwright unavailable):**
```bash
pandoc $PIPELINE_EXECUTION_DIR/resume_1page.txt -o $PIPELINE_EXECUTION_DIR/resume.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=0.5in \
  -V fontsize=10pt
```

### Step 3: Generate DOCX (Optional)
```bash
pandoc $PIPELINE_EXECUTION_DIR/resume_1page.txt -o $PIPELINE_EXECUTION_DIR/[Candidate]_[Company]_[Role].docx
```

### Step 4: Validate PDF
```bash
pdfinfo $PIPELINE_EXECUTION_DIR/[filename].pdf | grep Pages
# Target pages based on experience:
# 0-3 years: Must be 1 page
# 3-5 years: 1-2 pages acceptable
# 5+ years: 1-2 pages (prefer 2 for comprehensiveness)
```

### Step 5: Verify File Size
```bash
ls -lh $PIPELINE_EXECUTION_DIR/[filename].pdf
# Should be < 2MB (typically 40-300KB)
```

## HTML Template Features

The template automatically:
- **Bolds metrics:** Percentages, numbers with units (2M+ transactions, 99.5% success, 75% reduction)
- **Bolds technical terms:** Apache Kafka, Kubernetes, microservices, distributed systems, etc.
- **Professional layout:** Two-column skills grid, clean role blocks with domain tags
- **Print optimization:** CSS @page rules ensure strict 1-page A4 output
- **ATS-friendly:** Single-column, standard fonts, semantic HTML

## File Naming Convention

Format: `FirstName_LastName_Company_RoleAbbreviation_Year.pdf`

Examples:
- `Aman_Gupta_Agoda_StaffBackendEngineer_2026.pdf`
- `Aman_Gupta_Microsoft_SeniorSWE_2026.pdf`

## Troubleshooting

**If PDF exceeds target page count:**

For candidates with **<5 years experience** (target: 1 page):
1. Use the condensed resume version (`resume_1page.txt`)
2. Reduce font size in template (9pt → 8.5pt)
3. Tighten margins (10mm → 8mm)
4. Remove least impactful bullets from older roles

For candidates with **5+ years experience** (target: 2 pages):
1. 2 pages is acceptable and preferred for comprehensive coverage
2. Only condense if content exceeds 2.5 pages
3. If exactly 2.1-2.3 pages, slight font reduction (9pt → 8.8pt) is acceptable
4. Never sacrifice important achievements just to fit 1 page

**If Playwright not installed:**
```bash
pip3 install playwright
python3 -m playwright install chromium
```

## Output Files

Generate these files:
1. **PDF:** `[Name]_[Company]_[Role]_[Year].pdf` (primary deliverable)
2. **DOCX:** `[Name]_[Company]_[Role]_[Year].docx` (editable version)
3. **HTML:** `[Name]_[Company]_[Role]_[Year].html` (debugging/preview)

**Remember: Use HTML template for professional, ATS-optimized output.**
