# Input Directory

Place your input files here before running the pipeline.

## Required Files

### 1. `job_description.txt`
The complete job posting you're targeting. Include:
- Job title
- Company name
- Required qualifications
- Responsibilities
- Nice-to-have skills

### 2. `raw_background.txt`
Your career background information. Include:
- Resume or LinkedIn export
- Work experience with dates
- Technical skills
- Achievements and metrics
- Education
- Contact information

## Example

```
input/
├── job_description.txt    # Target job posting
└── raw_background.txt     # Your background
```

The pipeline will read these files and generate an optimized resume in the `output/` directory.
