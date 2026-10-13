# Multi-Sectoral Household Needs Assessment: Hararghe, Ethiopia

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![XLSForm](https://img.shields.io/badge/XLSForm-v1.0-blue)](https://xlsform.org/)
[![Python](https://img.shields.io/badge/Python-3.x-green)](https://www.python.org/)

An XLSForm survey instrument for KoboToolbox / ODK, designed for rapid household needs assessment and resilience profiling in **East and West Hararghe** (Oromia Region, Ethiopia).

> **Status:** Portfolio project demonstrating XLSForm design and data collection expertise. All data, coordinates, and test submissions are synthetic. Form is currently English-only; multi-language support (Amharic, Afaan Oromo, Somali) is planned for future implementation.

| | |
|---|---|
| **Download** | [`form/hararghe_hna_v1.xlsx`](form/hararghe_hna_v1.xlsx) |
| **Platforms** | KoboToolbox, ODK Collect, ODK Central, Enketo |
| **Language** | English (multi-language support planned for future) |

---

## Key Features

- **Complex Calculations:** HHS, rCSI, TLU, and dependency ratio computed in-form using XLSForm calculations
- **Dynamic Skip Logic:** Conditional questions based on consent, location cascading, and household composition
- **Data Quality Controls:** GPS accuracy checks, bounding box validation, regex phone validation, age consistency constraints
- **Household Roster:** Repeat group with automatic aggregation (school-age children, dependents, working-age population)
- **Cascading Selects:** Zone → Woreda → Kebele with choice filters for geographic accuracy
- **Multi-Platform Compatible:** Works on KoboToolbox, ODK Collect, ODK Central, and Enketo
- **Python Analysis Script:** Data cleaning, QC checks, and indicator recalculation template included

---

## 1. Purpose

Humanitarian teams need fast, comparable household data to prioritise assistance. This form collects standard food-security and WASH indicators alongside livelihood data specific to Hararghe's agro-pastoral and Khat-producing economy, and it computes the headline indicators **inside the form**, so enumerators and supervisors can see results before leaving the household.

**Design goals**
1. Prevent bad data at entry (constraints, regex, required fields) instead of cleaning it afterwards.
2. Keep the enumerator's workload low (skip logic, cascading selects, automatic calculations).
3. Make fabricated or low-quality interviews detectable (metadata, GPS, photo and audit checks).
4. Compute key indicators (HHS, rCSI, TLU, dependency ratio) inside the form for immediate feedback.

---

## 2. Testing the form

To test the form:

1. Download [`form/hararghe_hna_v1.xlsx`](form/hararghe_hna_v1.xlsx)
2. Upload to KoboToolbox or open in ODK Collect
3. Walk through these paths to see the logic work:

| Try this | Expect this |
|---|---|
| Choose **Zone: East Hararghe** | Woreda list shows only East Hararghe woredas; Kebele list stays empty until a Woreda is chosen |
| Enter phone `0812345678` | Rejected with a validation message (must be 10 digits starting 09 or 07) |
| Set household size to `5` | Roster repeats exactly 5 times |
| In the roster, enter a child older than the household head minus 12 | Constraint message blocks the entry |
| In Section 3, answer **No** to "Did the household experience any shock?" | The entire shock module is skipped |
| In WASH, select **Piped water on plot** as the main source | Distance and travel-time questions are skipped |
| Finish the form | Computed HHS, rCSI, TLU, and dependency ratio are saved with the submission |

---

## 3. Form structure

Six groups covering household demographics, livelihoods, food security, WASH, and verification.

### Section 1: Metadata, consent, and location
- **Metadata:** `start`, `end`, `today`, `deviceid` captured automatically. Interview duration is calculated in post-collection analysis.
- **Consent gate:** if the respondent declines, the form ends (`relevant` on all later groups).
- **Phone validation:** `regex(., '^(09|07)[0-9]{8}$')`. This validates Ethiopian mobile formats generally; it does not verify which operator owns the number.
- **Cascading location:** Zone → Woreda → Kebele using `choice_filter` with `zone` and `woreda` filter columns in the `choices` sheet.
  - East Hararghe examples: Babile, Gursum, Jarso
  - West Hararghe examples: Chiro, Gemechis, Mieso

### Section 2: Household roster
- A `begin_repeat` driven by `repeat_count = ${hh_size}`, bounded by a constraint (1–30) on household size.
- Each member records: relationship to head, sex, age, school attendance (if 5–18), and disability flag.
- **Calculated per member** (inside the repeat): flags such as `school_age` (5–18), `under5`, `dependent` (under 15 or over 64), `working_age` (15–64).
- **Aggregated at household level** (outside the repeat) using `sum(${flag})`:
  - Number of school-age children, number out of school
  - Presence of children under 5 (triggers nutrition follow-up)
  - **Dependency ratio** = dependents ÷ working-age members, guarded against divide-by-zero with `if(${n_working} > 0, ..., 99)`
- **Age consistency:** the household head's age is captured *before* the roster. Members recorded as the head's children must satisfy `. <= ${head_age} - 12`. Comparing against a single stored value is more reliable than comparing across repeat rows.

### Section 3: Livelihoods
- **Land allocation:** hectares under Khat, sorghum, maize, and other crops. A constraint checks that the sum of allocations does not exceed total land reported.
- **Livestock and TLU:** numeric counts per species, each multiplied by a conversion factor and summed:

  | Species | TLU factor |
  |---|---|
  | Cattle | 0.7 |
  | Camel | 1.0 |
  | Sheep / goat | 0.1 |
  | Donkey | 0.5 |
  | Poultry | 0.01 |

  (Factors follow commonly used East Africa values. Adjust to your programme's standard and cite it.)
- **Shock module:** a `select_multiple` of shocks (crop failure, livestock disease, market disruption, etc.). Follow-up questions use `selected(${shocks}, 'crop_failure')` so each follow-up appears only for the shocks reported.

### Section 4: Food security
- **Household Hunger Scale (HHS):** three questions, each with a yes/no occurrence and a frequency (rarely / sometimes / often). Frequency scores 1, 1, 2. Total 0–6.
  - 0–1: little or no hunger
  - 2–3: moderate hunger
  - 4–6: severe hunger
- **Reduced Coping Strategy Index (rCSI):** five behaviours, each asked as "days in the past 7" (0–7, enforced by constraint), multiplied by the standard severity weights:

  | Behaviour | Weight |
  |---|---|
  | Rely on less preferred / less expensive food | 1 |
  | Borrow food or rely on help from relatives | 2 |
  | Limit portion size at mealtimes | 1 |
  | Restrict adult consumption so children can eat | 3 |
  | Reduce number of meals per day | 1 |

  Score range 0–56. Higher is worse.

### Section 5: WASH
- **Main water source** with seasonal variation (dry vs. wet season). Options include piped water, boreholes, protected/unprotected wells, springs, rivers, rainwater, and bottled water.
- **Skip logic:** if the source is on-plot piped water, distance and time questions are bypassed (`relevant = ${water_dry} != 'piped_plot'`).
- Sanitation and handwashing items follow JMP-style categories.

### Section 6: Verification
- **Photo capture** of the dwelling or plot (`image`, with `max-pixels=1024` to control upload size).
- **Signature** (`image` with `appearance=signature`) for consent.
- **GPS capture** (`geopoint`) with:
  - an accuracy check: `number(selected-at(., 3)) <= 20`
  - a bounding-box check on latitude/longitude extracted with `substring-before` and `selected-at`, to flag points outside the Hararghe operating area
  - Cross-checking points against a sampling frame is done **after collection** (see `analysis/`), because XLSForm cannot do this natively.

---

## 4. Data workflow

```
Enumerator (ODK Collect / Enketo)
        │  submit
        ▼
KoboToolbox server  ──►  Export (XLS / CSV, repeat groups as separate sheets)
                                   │
                                   ▼
                    analysis/clean_and_score.py
                      • checks duration, GPS, duplicates
                      • recomputes HHS / rCSI / TLU to confirm form calculations
                      • produces a quality-control summary by enumerator
                                   │
                                   ▼
                          Dashboards / reports
```

Sample data: `data/sample_submissions.csv` (20 synthetic records, including intentionally flawed ones used to test the QC script).

---

## 5. Repository layout

```
├── README.md
├── DESIGN.md
├── form/
│   └── hararghe_hna_v1.xlsx        # the XLSForm
├── docs/
│   └── data_dictionary.md          # every variable: name, type, label, constraint
├── data/
│   └── sample_submissions.csv
├── analysis/
│   └── clean_and_score.py
└── LICENSE
```

---

## 6. Technical notes and known limitations

- **Geofencing is approximate.** Bounding-box checks catch gross errors only. A rectangle is not the real boundary of the zones.
- **Kebele and woreda lists** are illustrative and not an official administrative gazetteer. Verify against CSA / OCHA COD data before production.
- **Calculations** run client-side. Always recompute indicators in analysis rather than trusting the form's values blindly.
- **Multi-language support:** Form is currently English-only. Amharic, Afaan Oromo, and Somali translations are planned for future implementation.

---

## 7. Tools and standards

XLSForm spec · pyxform · KoboToolbox · ODK Collect · Enketo · HHS (FANTA) · rCSI (WFP/CARE) · TLU conversion factors · JMP WASH ladders

---

## 8. Author & Skills

**Arfan Eliyas** - Data Collection & M&E Specialist | KoboToolbox/ODK Expert

### Technical Competencies Demonstrated

**XLSForm Design:**
- Complex calculations and conditional logic
- Repeat groups with aggregation functions
- Cascading selects with choice filters
- Regex validation and constraint design
- Multi-platform form deployment

**Data Collection Methodology:**
- Standard humanitarian indicators (HHS, rCSI, TLU)
- Multi-sectoral household assessment design
- Data quality control frameworks
- Enumerator training considerations

**Data Analysis:**
- Python for data cleaning and QC
- Indicator recalculation and validation
- GPS and metadata analysis
- Enumerator performance tracking

**M&E Best Practices:**
- Form design for data quality at source
- Skip logic to reduce enumerator burden
- Verification mechanisms (GPS, photos, signatures)

---

### 📬 Connect With Me

- **Email:** [arfaneliyas27@gmail.com](mailto:arfaneliyas27@gmail.com)
- **LinkedIn:** [linkedin.com/in/arfaneliyas](https://www.linkedin.com/in/arfaneliyas/?isSelfProfile=true)

---

Licence: MIT (form and code). Synthetic data only.
