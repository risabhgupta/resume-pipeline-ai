# AI-Driven Skills Framework

## Core Philosophy: INTELLIGENCE, NOT TEMPLATES

**AI must reason about each resume uniquely based on:**
1. Job description requirements
2. Candidate's actual background
3. Transferable skills logic
4. ATS best practices (15-25 total skills optimal)

## AI Process

### Step 1: Extract Technologies from Background
- Parse every role, achievement, project
- Identify explicit: "Used Java" → Java
- Identify implicit: "Built REST API" → REST APIs, API Design

### Step 2: Analyze JD Requirements
- Load from alignment_matrix.json
- Required keywords
- High-priority gaps
- Nice-to-have skills

### Step 3: Apply Transferable Skills Logic
**Examples:**
- Has Java → Can work with Kotlin (JVM family)
- Has AWS → Can work with GCP (cloud-agnostic)
- Has Cassandra → Similar to Aerospike (columnar NoSQL)
- Has C++ → Can work with Go (compiled systems languages)

### Step 4: Categorize Intelligently (5-8 categories)
1. **Languages:** Programming languages from background + JD-required transferable
2. **Backend & APIs:** Frameworks, architectures, API types
3. **Data & Streaming:** (Only if background has data work)
4. **Databases:** SQL + NoSQL + Cache + Search engines
5. **Cloud & DevOps:** Platforms WITH services (show depth: "AWS (EC2, S3, Lambda)")
6. **Observability:** Monitoring, logging, tracing tools used
7. **System Design:** (Staff+ only) Distributed Systems, HA, Fault Tolerance, etc.
8. **Practices:** Agile, TDD, Technical Leadership (if applicable)

### Step 5: Validate
- [ ] 15-25 total skills (not too few, not stuffing)
- [ ] All skills from background OR transferable with logic
- [ ] All JD top-10 keywords present
- [ ] No fabrication

## Example AI Reasoning

**Input:** Candidate has Java, Scala, Cassandra. JD requires Kotlin, Aerospike.

**AI Decision:**
```
Add Kotlin: ✅ (transferable from Java - same JVM)
Add Aerospike: ✅ (transferable from Cassandra - similar columnar NoSQL)
Format: "Languages: Java, Scala, Kotlin"
        "Databases: Cassandra, ScyllaDB, Aerospike"
```

**Pure AI intelligence - no static templates.**
