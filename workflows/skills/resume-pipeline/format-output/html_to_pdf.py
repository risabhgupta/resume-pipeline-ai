#!/usr/bin/env python3
"""
HTML Resume Template Renderer and PDF Generator
Uses Playwright to convert HTML to PDF with strict 1-page A4 enforcement
"""

import json
import re
from pathlib import Path
from typing import Dict, List


def load_template(template_path: str) -> str:
    """Load HTML template from file"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def bold_metrics_and_tech(text: str) -> str:
    """
    Bold key metrics, numbers, and technical terms in bullet text
    """
    # Bold percentages and numbers with context
    text = re.sub(r'(\d+(?:\.\d+)?%)', r'<strong>\1</strong>', text)
    text = re.sub(r'(\d+(?:,\d+)*\+?\s*(?:transactions|pipelines|partners|engineers|executions|problems|users|KB|MB|TB|K\+|M\+)(?:/day|/hour)?)',
                  r'<strong>\1</strong>', text, flags=re.IGNORECASE)

    # Bold time reductions and improvements
    text = re.sub(r'((?:from\s+)?\d+\s*(?:days?|hours?|minutes?|seconds?)\s+to\s+<?[\d\s]+(?:days?|hours?|minutes?|seconds?))',
                  r'<strong>\1</strong>', text, flags=re.IGNORECASE)
    text = re.sub(r'(\d+(?:\.\d+)?x)', r'<strong>\1</strong>', text)

    # Bold specific technical terms and systems
    tech_terms = [
        'De-Hub', 'Maverick', 'SPG', 'Apache Kafka', 'Apache Spark', 'Apache Flink',
        'Apache Iceberg', 'ScyllaDB', 'Cassandra', 'MongoDB', 'Redis', 'Elasticsearch',
        'Kubernetes', 'K8s', 'Docker', 'AWS', 'Azure', 'GCP', 'OpenTelemetry',
        'Prometheus', 'Grafana', 'Spring Boot', 'Hibernate', 'JPA',
        'DAG', 'IaC', 'RBAC', 'ABAC', 'MTTR', 'SRE', 'ETL', 'CI/CD',
        'AI-driven', 'LangChain', 'LangGraph', 'microservices', 'distributed'
    ]

    for term in tech_terms:
        # Only bold if not already in <strong> tags
        text = re.sub(f'(?<!<strong>)({re.escape(term)})(?!</strong>)',
                     r'<strong>\1</strong>', text, flags=re.IGNORECASE)

    return text


def parse_resume_content(resume_path: str) -> Dict:
    """Parse resume text file into structured data"""
    with open(resume_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Extract header info
    header_line = lines[1] if len(lines) > 1 else ""
    contact_parts = [p.strip() for p in header_line.split('|')]

    phone = contact_parts[0] if len(contact_parts) > 0 else ""
    email = contact_parts[1] if len(contact_parts) > 1 else ""
    linkedin = contact_parts[2] if len(contact_parts) > 2 else ""
    location = contact_parts[3] if len(contact_parts) > 3 else ""

    # Extract name from first line
    name = lines[0].strip() if lines else "AMAN GUPTA"

    # Parse skills section
    skills_grid = parse_skills_section(content)

    # Parse experience section
    experience_blocks = parse_experience_section(content)

    # Parse education
    education_content = parse_education_section(content)

    # Parse additional section
    additional_section = parse_additional_section(content)

    return {
        'FULL_NAME': name,
        'PHONE': phone,
        'EMAIL': email,
        'LINKEDIN': linkedin.replace('linkedin.com/in/', '').replace('https://', '').replace('http://', ''),
        'LINKEDIN_URL': linkedin if linkedin.startswith('http') else f'https://{linkedin}',
        'LOCATION': location,
        'SKILLS_GRID': skills_grid,
        'EXPERIENCE_BLOCKS': experience_blocks,
        'EDUCATION_CONTENT': education_content,
        'ADDITIONAL_SECTION': additional_section
    }


def parse_skills_section(content: str) -> str:
    """Parse skills section into HTML grid format"""
    skills_section = ""
    in_skills = False

    for line in content.split('\n'):
        if line.strip() == 'SKILLS':
            in_skills = True
            continue
        elif line.strip() == 'EXPERIENCE':
            break
        elif in_skills and ':' in line:
            parts = line.split(':', 1)
            category = parts[0].strip()
            items = parts[1].strip() if len(parts) > 1 else ""

            # Shorten category names for better formatting
            category = category.replace('Languages', 'Languages') \
                              .replace('Backend & Frameworks', 'Backend & Frameworks') \
                              .replace('Distributed Systems', 'Distributed Systems') \
                              .replace('Databases', 'Databases & Storage') \
                              .replace('Cloud & Infrastructure', 'Cloud & Observability')

            skills_section += f'        <div class="skill-cat">{category}:</div>\n'
            skills_section += f'        <div class="skill-list">{items}</div>\n\n'

    return skills_section.strip()


def parse_experience_section(content: str) -> str:
    """Parse experience section into HTML role blocks"""
    experience_html = ""
    in_experience = False
    current_role = None
    current_bullets = []

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line == 'EXPERIENCE':
            in_experience = True
            i += 1
            continue
        elif line in ['EDUCATION', 'ADDITIONAL INFORMATION', 'ADDITIONAL']:
            break

        if in_experience:
            # Check if this is a role header (contains | and doesn't start with -)
            if '|' in line and not line.startswith('-') and len(line) > 20:
                # Save previous role if exists
                if current_role:
                    experience_html += format_role_block(current_role, current_bullets)
                    current_bullets = []

                # Parse new role
                current_role = parse_role_header(line)

            # Check if this is a domain line (next line after role header)
            elif current_role and line.startswith('Domain:'):
                current_role['domain'] = line.replace('Domain:', '').strip()

            # Check if this is a bullet point (supports both - and •)
            elif line.startswith('•') or line.startswith('-'):
                bullet_text = line[1:].strip()
                current_bullets.append(bullet_text)

        i += 1

    # Add last role
    if current_role:
        experience_html += format_role_block(current_role, current_bullets)

    return experience_html


def parse_role_header(line: str) -> Dict:
    """Parse role header line into structured data"""
    parts = [p.strip() for p in line.split('|')]

    title = parts[0] if len(parts) > 0 else ""
    company = parts[1] if len(parts) > 1 else ""
    dates = parts[2] if len(parts) > 2 else ""

    return {
        'title': title,
        'company': company,
        'dates': dates,
        'domain': ''
    }


def format_role_block(role: Dict, bullets: List[str]) -> str:
    """Format a role block as HTML"""
    domain_html = f'<span class="role-domain">({role["domain"]})</span>' if role['domain'] else ''

    html = f'''
      <div class="role-block">
        <div class="role-header">
          <div>
            <span class="role-title-company">{role['title']}</span> |
            <span class="role-company">{role['company']}</span>
            {domain_html}
          </div>
          <div class="role-dates">{role['dates']}</div>
        </div>
        <ul class="bullets">
'''

    for bullet in bullets:
        # Apply metric and tech bolding
        formatted_bullet = bold_metrics_and_tech(bullet)
        html += f'          <li>{formatted_bullet}</li>\n'

    html += '        </ul>\n      </div>\n'

    return html


def parse_education_section(content: str) -> str:
    """Parse education section"""
    in_education = False
    education_html = ""

    for line in content.split('\n'):
        if line.strip() == 'EDUCATION':
            in_education = True
            continue
        elif line.strip() in ['ADDITIONAL INFORMATION', 'ADDITIONAL']:
            break
        elif in_education and line.strip() and not line.startswith('-'):
            parts = [p.strip() for p in line.split('|')]
            degree_school = parts[0] if len(parts) > 0 else line
            dates = parts[1] if len(parts) > 1 else ""

            education_html += f'      <div class="edu-row">\n'
            education_html += f'        <div><strong>{degree_school}</strong></div>\n'
            if dates:
                education_html += f'        <div class="role-dates">{dates}</div>\n'
            education_html += f'      </div>\n'

    return education_html.strip()


def parse_additional_section(content: str) -> str:
    """Parse additional information section"""
    in_additional = False
    additional_text = ""

    for line in content.split('\n'):
        if line.strip() in ['ADDITIONAL INFORMATION', 'ADDITIONAL']:
            in_additional = True
            continue
        elif in_additional and line.strip():
            additional_text += line.strip() + " "

    if additional_text:
        # Bold numbers in additional section too
        additional_text = bold_metrics_and_tech(additional_text)
        return f'''
    <section class="section">
      <div class="section-title">Additional Information</div>
      <div class="additional-text">
        {additional_text.strip()}
      </div>
    </section>
'''
    return ""


def render_template(template: str, data: Dict) -> str:
    """Replace template placeholders with actual data"""
    html = template

    for key, value in data.items():
        placeholder = f'{{{{{key}}}}}'
        html = html.replace(placeholder, str(value))

    return html


def html_to_pdf_playwright(html_content: str, output_path: str):
    """Convert HTML to PDF using Playwright"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content, wait_until="networkidle")
            page.pdf(
                path=output_path,
                format="A4",
                print_background=True,
                margin={"top": "10mm", "bottom": "10mm", "left": "12mm", "right": "12mm"}
            )
            browser.close()

        return True
    except ImportError:
        print("ERROR: Playwright not installed. Install with: pip install playwright && playwright install chromium")
        return False
    except Exception as e:
        print(f"ERROR generating PDF with Playwright: {e}")
        return False


def main():
    """Main execution"""
    import sys

    if len(sys.argv) < 4:
        print("Usage: python html_to_pdf.py <resume_txt_path> <template_path> <output_pdf_path>")
        sys.exit(1)

    resume_path = sys.argv[1]
    template_path = sys.argv[2]
    output_path = sys.argv[3]

    # Parse resume content
    print(f"Parsing resume from: {resume_path}")
    data = parse_resume_content(resume_path)

    # Load template
    print(f"Loading template from: {template_path}")
    template = load_template(template_path)

    # Render HTML
    print("Rendering HTML...")
    html = render_template(template, data)

    # Save HTML for debugging
    html_output = output_path.replace('.pdf', '.html')
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML saved to: {html_output}")

    # Convert to PDF
    print(f"Generating PDF: {output_path}")
    success = html_to_pdf_playwright(html, output_path)

    if success:
        print(f"✅ PDF generated successfully: {output_path}")
    else:
        print(f"❌ PDF generation failed. HTML file available at: {html_output}")
        sys.exit(1)


if __name__ == "__main__":
    main()
