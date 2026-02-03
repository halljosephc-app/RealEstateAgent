# Real Estate Analysis Agent

A reusable AI-powered system for analyzing property documents and generating comprehensive buyer intelligence reports.

## What This Does

Give it property documents (inspections, MLS listings, pest reports, contractor quotes) and it generates 5 professionally-formatted reports tailored for different audiences:

| Document | Audience | Purpose |
|----------|----------|---------|
| **1 - START HERE** | Busy decision-makers | 1-page executive summary |
| **2 - Full Details** | Family members | Comprehensive analysis with costs |
| **3 - Pre-Offer Checklist** | Action takers | Fillable verification steps |
| **4 - Move-In Priority List** | Contractors | Repair prioritization by urgency |
| **5 - For Your Realtor** | Buyer's agent | Negotiation brief with comps |

## Installation

### 1. Clone the Repository

```bash
cd ~/Documents
git clone https://github.com/yourusername/RealEstateAgent.git
```

Or download and extract to your Documents folder.

### 2. Install Dependencies

```bash
# For PDF generation
npm install -g md-to-pdf

# For OCR (optional, only if you have scanned documents)
pip install pdf2image pytesseract Pillow
```

For OCR on Windows, also install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

---

## Quick Start

### Step 1: Create a Property Folder

Create a new folder for your property analysis (anywhere you like):

```bash
mkdir ~/Documents/MyPropertyAnalysis
cd ~/Documents/MyPropertyAnalysis
mkdir input output
```

### Step 2: Add Your Documents

Copy all property documents into the `input/` folder:
- Home inspection PDF
- MLS listing / Redfin printout
- Termite/pest reports
- Contractor quotes
- Disclosure documents

### Step 3: Run OCR (if needed)

If you have scanned documents, run the OCR script:

```bash
# Adjust path to where you cloned RealEstateAgent
python ~/Documents/RealEstateAgent/scripts/ocr_pdfs.py
```

### Step 4: Start Claude Code

```bash
cd ~/Documents/MyPropertyAnalysis
claude
```

### Step 5: Run the Analysis

Use this prompt template (adjust the path to where you installed RealEstateAgent):

```
@~/Documents/RealEstateAgent/CLAUDE.md

Analyze property at [ADDRESS].

Buyers: [describe - e.g., "60+ year old couple looking for retirement home"]
Budget: [maximum budget, e.g., "$1,100,000"]
Key concerns: [any known issues, e.g., "neighbor workshop noise, fire zone"]

Read the example outputs in @~/Documents/RealEstateAgent/example/output/
to understand the exact style and format to use.

Source documents are in ./input/
Generate the 5 standard output documents in ./output/
```

**Note:** Replace `~/Documents/RealEstateAgent` with your actual install path.

### Step 6: Generate PDFs

```bash
cd output
npx md-to-pdf "*.md"
```

Or use the batch script (Windows):
```bash
path/to/RealEstateAgent/scripts/generate_pdfs.bat
```

---

## Folder Structure

```
RealEstateAgent/
|
+-- CLAUDE.md           # Agent instructions (the "brain")
+-- README.md           # This file
|
+-- config/
|   +-- defaults.json        # Financial assumptions
|   +-- pricing-rules.json   # Odd-number pricing psychology
|   +-- cost-estimates.json  # SoCal contractor rates
|
+-- schemas/
|   +-- property.schema.json  # Property data structure
|   +-- findings.schema.json  # Inspection findings structure
|
+-- scripts/
|   +-- ocr_pdfs.py          # OCR for scanned documents
|   +-- generate_pdfs.bat    # Batch PDF conversion (Windows)
|
+-- example/                 # Reference example (24364 Arcadia)
    +-- input/               # Source documents
    +-- extracted/           # Text extractions
    +-- output/              # The 5 output documents
```

---

## Key Features

### Odd-Number Pricing Psychology
All offer amounts use specific, odd numbers (e.g., $973,000 instead of $975,000). This signals careful calculation rather than arbitrary rounding.

### Cost Ranges, Never Single Numbers
Every repair estimate is a range ($40,000 - $45,000), never a single number. This accounts for real-world variability.

### Walk-Away Triggers
Critical deal-breakers are prominently highlighted:
- Noise issues that can't be fixed
- Insurance unavailability
- Major unpermitted structural work
- Environmental contamination

### Audience-Appropriate Tone
- Family documents: Conversational, honest, practical
- Agent document: Professional, data-driven, negotiation-focused

### Cross-Document Analysis
The system identifies patterns across documents:
- Recurring issues in multiple pest reports
- Items marked "not completed" in completion notices
- Contradictions between sources

---

## Customization

### Adjust Financial Assumptions
Edit `config/defaults.json` to change:
- Interest rates
- Property tax rates
- Insurance costs
- Maintenance assumptions

### Modify Pricing Strategy
Edit `config/pricing-rules.json` to change:
- Discount percentages for different property conditions
- Market time discount thresholds
- Maximum offer formulas

### Update Repair Costs
Edit `config/cost-estimates.json` to adjust:
- Contractor rates for your region
- Specific repair cost ranges
- Premium multipliers (lead paint, hillside, etc.)

---

## Example Prompts

### For a Retirement Home

```
Analyze property at 123 Main Street, City, CA 91234.

Buyers: Retired couple in their 60s, downsizing from larger home.
Low tolerance for repair work - prefer move-in ready but considering
this property for the large lot and quiet neighborhood.

Budget: $1,000,000 maximum, $200,000 cash for repairs if needed

Key concerns: Property has been on market 4 months, 2 price drops.
Inspection mentions old electrical panel and roof issues.
```

### For a Family Home

```
Analyze property at 456 Oak Avenue, Town, CA 90000.

Buyers: Family with 2 kids, need good school district.
Handy homeowners comfortable with some DIY work.
First-time buyers, pre-approved for conventional loan.

Budget: $850,000 maximum, prefer under $800,000

Key concerns: House was built in 1965, no updates visible in listing.
Want to understand true cost to modernize.
```

### For an Investor

```
Analyze property at 789 Investment Blvd, Metro, CA 95000.

Buyers: Real estate investor, plan to renovate and rent or flip.
High tolerance for work, looking for value-add opportunity.

Budget: $600,000 purchase + $150,000 renovation budget

Key concerns: Need accurate repair costs for ROI calculation.
Focus on structural issues and major systems.
```

---

## Troubleshooting

### Large Inspection Reports (50+ pages)
Ask Claude to process in chunks:
```
Read the inspection PDF pages 1-15 first. Extract all findings
to a list. Then continue with pages 16-30, and so on.
```

### Scanned/Image PDFs
Run the OCR script first:
```bash
python scripts/ocr_pdfs.py
```

### Missing Cost Estimates
Reference the cost database directly:
```
Use @config/cost-estimates.json for California contractor rates.
```

### Outputs Don't Match Example Style
Explicitly reference the examples:
```
Your output must match the exact formatting in @example/output/1 - START HERE.md
including table styles, bullet separators, and section structure.
```

---

## Requirements

- Claude Code CLI (`claude`)
- Node.js (for md-to-pdf)
- Python 3 + Tesseract (for OCR, only if you have scanned documents)

---

## Credits

Built with Claude Code. Example analysis based on 24364 Arcadia Street, Newhall, CA.

Pricing psychology based on negotiation research showing that precise numbers signal careful analysis and are more effective in negotiations than round numbers.
