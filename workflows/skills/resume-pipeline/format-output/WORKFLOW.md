# format-output Skill

## AI Instructions

# Stage 9: Format Output - Professional HTML/PDF Generation

You are the **Format Specialist** for the HireEngine v2.0 resume pipeline.

## Generation Method: HTML Template → PDF

**PREFERRED METHOD:** Use the professional HTML template with Playwright for superior formatting.

The HTML template (`templates/resume_template.html`) provides:
- Strict 1-page A4 enforcement via print-media CSS
- Professional two-column skills grid
- Bold metrics for scannability
- Clean semantic structure
- ATS-friendly single-column layout

## AI-Driven Process

### Step 1: Analyze Content
- Read the generated resume text file
- Check if condensed version needed (word count > 650)
- Determine if content fits in 1 page

### Step 2: Generate PDF Using HTML Template

**Primary Method (Recommended):**
```bash
python3 workflows/skills/resume-pipeline/format-output/html_to_pdf.py \
  output/resume_1page.txt \
  workflows/skills/resume-pipeline/format-output/templates/resume_template.html \
  output/[Candidate]_[Company]_[Role].pdf
```

This will:
- Parse resume text into structured data
- Apply HTML template with professional styling
- Bold all metrics and key technical terms automatically
- Generate PDF using Playwright with strict 1-page enforcement

**Fallback Method (If Playwright unavailable):**
```bash
pandoc output/resume_1page.txt -o output/resume.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=0.5in \
  -V fontsize=10pt
```

### Step 3: Generate DOCX (Optional)
```bash
pandoc output/resume_1page.txt -o output/[Candidate]_[Company]_[Role].docx
```

### Step 4: Validate PDF
```bash
pdfinfo output/[filename].pdf | grep Pages
# Must output: Pages: 1
```

### Step 5: Verify File Size
```bash
ls -lh output/[filename].pdf
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

**If PDF is 2 pages:**
1. Use the condensed resume version (`resume_1page.txt`)
2. Reduce font size in template (9pt → 8.5pt)
3. Tighten margins (10mm → 8mm)
4. Remove least impactful bullets from older roles

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
