# Resume Pipeline Command

Execute the HireEngine v2.0 multi-stage pipeline with feedback loops and quality gates.

Load and execute the orchestrator workflow from `workflows/skills/resume-pipeline/orchestrator/WORKFLOW.md`

This will run the complete 11-stage pipeline:
1. Intake - Load job description and background
2. Validate Context - Check completeness
3. Analyze Alignment - Keyword gap analysis
4. Validate Alignment - Challenge assumptions
5. Generate Content - Create resume with X-Y-Z formula
6. Validate Content - Quality check
7. Score ATS - Calculate ATS compatibility
8. ATS Gatekeeper - Enforce quality threshold
9. Format Output - Generate PDF/DOCX
10. Validate Format - Ensure 1-page
11. Finalize - Professional naming and packaging

The pipeline includes:
- Automatic refinement loops (up to 3 iterations per stage)
- Quality gates (content >= 85/100, ATS >= 75/100)
- User escalation when automated fixes fail
- Comprehensive execution report

Execute the orchestrator prompt and begin pipeline execution.
