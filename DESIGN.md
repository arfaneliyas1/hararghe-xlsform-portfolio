# Design Document: Hararghe Household Needs Assessment

This document outlines the design decisions and planning process for the Hararghe Household Needs Assessment XLSForm.

## Project Context

**Target Area:** East and West Hararghe zones, Oromia Region, Ethiopia
**Purpose:** Rapid household needs assessment and resilience profiling
**Target Users:** Trained enumerators using KoboToolbox/ODK Collect
**Respondents:** Household heads or adults familiar with household affairs

## Design Goals

1. **Data Quality First** - Prevent bad data at entry through constraints, validation, and required fields
2. **Enumerator Efficiency** - Minimize workload through skip logic, cascading selects, and automatic calculations
3. **Fraud Detection** - Make fabricated or low-quality interviews detectable through metadata, GPS, and audit checks
4. **Immediate Feedback** - Compute key indicators inside the form so results are visible before leaving the household

## Indicator Selection

### Food Security
- **Household Hunger Scale (HHS)** - Standard FANTA indicator for household food access
  - 3 questions covering food availability, hunger, and severe deprivation
  - Score range 0-6 (little/no hunger to severe hunger)
  
- **Reduced Coping Strategy Index (rCSI)** - WFP/CARE indicator for coping behaviors
  - 5 coping strategies with severity weights
  - Score range 0-56 (low to high coping)

### Livelihoods
- **Tropical Livestock Units (TLU)** - Standard livestock wealth indicator
  - Conversion factors: cattle (0.7), camel (1.0), sheep/goat (0.1), donkey (0.5), poultry (0.01)
  
- **Dependency Ratio** - Household economic pressure indicator
  - Dependents (under 15, over 64) ÷ Working-age (15-64)

### WASH
- JMP-style categories for water source, sanitation, and handwashing
- Distance and time to water source for access assessment

## Form Structure

### Section 1: Metadata, Consent, Location
**Rationale:** Capture administrative data and obtain consent before collecting sensitive information.

**Key Features:**
- Consent gate - if declined, form ends immediately
- Cascading location selects (Zone → Woreda → Kebele) to reduce errors
- Phone validation with Ethiopian mobile format (09/07 prefix)
- Respondent code format (2 letters + 3 digits) for anonymity

### Section 2: Household Roster
**Rationale:** Capture demographic composition for dependency ratio and vulnerability analysis.

**Key Features:**
- Dynamic repeat based on household size (1-30 members)
- Age consistency check: children must be at least 12 years younger than household head
- Automatic flagging of school-age children (5-18), under-5s, dependents, working-age
- Follow-up questions for households with under-5 children (health screening)

### Section 3: Livelihoods
**Rationale:** Understand economic base and shock exposure specific to Hararghe's agro-pastoral context.

**Key Features:**
- Land allocation by crop (khat, sorghum, maize, other) with total constraint
- Khat-specific calculation (percentage of total land) - critical for Hararghe economy
- Livestock counts with TLU calculation
- Shock module with skip logic (only shown if shocks experienced)
- Shock-specific follow-up questions based on selected shocks

**Note on Land Measurement:**
This form uses hectares as the standard unit for international reporting. In a real deployment in Ethiopia, it would be more appropriate to:
- Use local measurement units familiar to farmers 
- Include conversion guidance in enumerator training materials
- Convert to hectares in analysis for standard reporting
- This approach improves data accuracy by using units respondents understand

**Note on Crop Allocation:**
This form asks for exact hectares by crop (khat, sorghum, maize, other). In a real deployment, farmers may struggle with precise measurements. Better approaches include:
- Asking for proportions/percentages of land by crop (e.g., "What percentage is khat?")
- Using local units for each crop type
- Training enumerators to help with estimation using visual aids
- Accounting for inter-cropping and seasonal variations
- These methods improve accuracy while still allowing conversion to hectares in analysis

### Section 4: Food Security
**Rationale:** Measure food access and coping strategies using standardized indicators.

**Key Features:**
- HHS questions with frequency follow-up (rarely/sometimes/often)
- Automatic HHS scoring and categorization
- rCSI questions with day counts (0-7) and weighted scoring
- Automatic rCSI scoring and categorization

### Section 5: WASH
**Rationale:** Assess water, sanitation, and hygiene conditions following JMP standards.

**Key Features:**
- Seasonal water source variation (dry vs wet season)
- Skip logic: if piped water on plot, skip distance/time questions
- Time-distance consistency check (soft warning for implausible combinations)
- Sanitation and handwashing observation questions

### Section 6: Verification
**Rationale:** Collect evidence to validate interview quality and location.

**Key Features:**
- GPS capture with accuracy check (≤20m required)
- GPS bounding box check to flag locations outside Hararghe
- Photo capture of dwelling and farm plot
- Digital signature for consent
- Summary screen showing computed indicators

## Data Quality Controls

### Enumerator Tracking
**Current Implementation:** Manual enumerator ID selection at the start of each survey.

**Production Approaches:**
1. **Device-Enumerator Mapping:** Assign each tablet/phone to a specific enumerator. Use `deviceid` to automatically identify the enumerator in analysis, preventing manual selection errors.
2. **Server-Based Authentication:** Use KoboToolbox user accounts. The server automatically records which enumerator submitted each form, providing the most secure tracking method.

For this demonstration form, manual selection is used to show the concept of enumerator tracking. In a real deployment, device-enumerator mapping or server authentication would be preferred for data security and fraud prevention.

### Input Validation
- Phone numbers: 10 digits, must start with 09 or 07
- Respondent codes: 2 capital letters + 3 digits
- Ages: 15-99 for adults, 0-100 for household members
- Household size: 1-30 members
- Land values: non-negative, crop allocation cannot exceed total
- rCSI entries: 0-7 days per behavior

### Skip Logic
- Consent gate: entire form after consent requires consent = 'yes'
- Shock module: only shown if any_shock = 'yes'
- Shock follow-ups: only shown for specific shocks selected
- Water distance/time: skipped if piped water on plot
- School questions: only for ages 5-18
- Disability question: only for ages 5+
- Under-5 follow-up: only if has_under5 = 1

### Consistency Checks
- Child age must be ≤ head_age - 12
- Land allocation by crop must sum to ≤ total land
- Water time should be consistent with distance (soft warning)

### Fraud Detection
- GPS accuracy check (≤20m)
- GPS bounding box check (Hararghe area)
- Interview duration (calculated in analysis)
- Duplicate respondent code detection (in analysis)
- Photo evidence requirement

## Geographic Scope

**Bounding Box (Approximate):**
- Latitude: 8.0° to 10.0°
- Longitude: 40.0° to 43.5°

**Administrative Units:**
- Zones: East Hararghe, West Hararghe
- Woredas: 4 per zone (8 total) - illustrative, verify against CSA/OCHA COD
- Kebeles: 4 per woreda (32 total) - illustrative placeholders

## Known Limitations

1. **Geofencing** - Bounding box is approximate; real zone boundaries are irregular
2. **Administrative Lists** - Woreda and kebele names are illustrative; verify against official data
3. **Language** - Form is currently English-only; multi-language support planned for future
4. **Client-side Calculations** - Always recompute indicators in analysis for validation

## Future Enhancements

1. Multi-language support (Amharic, Afaan Oromo, Somali)
2. Official administrative gazetteer integration
3. More precise GPS boundaries (shapefile-based)
4. Additional livelihood modules (market access, credit)
5. Offline form validation improvements

---

**Author:** Arfan Eliyas  
**Date:** October 2026  
**Version:** 1.0
