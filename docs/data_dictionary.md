# Data Dictionary

Complete variable documentation for the Hararghe Household Needs Assessment form. Types, skip logic, constraints, and calculations are documented as implemented in the XLSForm.

| Variable | Type | Label (English) | Required | Relevant | Constraint | Calculation |
|---|---|---|---|---|---|---|
| `start` | start |  |  |  |  |  |
| `end` | end |  |  |  |  |  |
| `today` | today |  |  |  |  |  |
| `deviceid` | deviceid |  |  |  |  |  |
| `g_meta` | begin_group | Hararghe Household Needs Assessment |  |  |  |  |
| `intro_note` | note | DEMONSTRATION FORM. All data entered is test data. Do not enter real personal information. This survey asks about your household's food, livelihood and water situation. Taking part is voluntary and you can stop at any time. |  |  |  |  |
| `consent` | select_one yesno | Do you agree to take part? | yes |  |  |  |
| `consent_end` | note | Thank you. The interview ends here. |  | `${consent} = 'no'` |  |  |
| `g_location` | begin_group | Section 1: Location and household basics |  | `${consent} = 'yes'` |  |  |
| `enum_id` | select_one enumerators | Enumerator ID | yes |  |  |  |
| `interview_date` | date | Interview date | yes |  | `. <= today() and . >= today() - 30` |  |
| `zone` | select_one zones | Zone | yes |  |  |  |
| `woreda` | select_one woredas | Woreda | yes |  |  |  |
| `kebele` | select_one kebeles | Kebele | yes |  |  |  |
| `resp_name_code` | text | Respondent code | yes |  | `regex(., '^[A-Z]{2}[0-9]{3}$')` |  |
| `resp_phone` | text | Respondent phone number (optional) |  |  | `regex(., '^(09\|07)[0-9]{8}$')` |  |
| `resp_sex` | select_one sex | Sex of respondent | yes |  |  |  |
| `resp_age` | integer | Age of respondent | yes |  | `. >= 15 and . <= 99` |  |
| `head_age` | integer | Age of the household head | yes |  | `. >= 15 and . <= 99` |  |
| `head_sex` | select_one sex | Sex of the household head | yes |  |  |  |
| `hh_size` | integer | Total number of household members | yes |  | `. >= 1 and . <= 30` |  |
| `g_roster` | begin_group | Section 2: Household roster |  | `${consent} = 'yes'` |  |  |
| `roster` | begin_repeat | Household member |  |  |  |  |
| `m_rel` | select_one relationship | Relationship to the household head | yes |  |  |  |
| `m_sex` | select_one sex | Sex | yes |  |  |  |
| `m_age` | integer | Age in years | yes |  | `. >= 0 and . <= 100 and (${m_rel} != 'child' or . <= ${head_age} - 12)` |  |
| `m_school` | select_one yesno | Is this person currently attending school? | yes | `${m_age} >= 5 and ${m_age} <= 18` |  |  |
| `m_disability` | select_one yesno | Does this person have difficulty seeing, hearing, walking or remembering? | yes | `${m_age} >= 5` |  |  |
| `f_school_age` | calculate |  |  |  |  | `if(${m_age} >= 5 and ${m_age} <= 18, 1, 0)` |
| `f_out_school` | calculate |  |  |  |  | `if(${f_school_age} = 1 and ${m_school} = 'no', 1, 0)` |
| `f_under5` | calculate |  |  |  |  | `if(${m_age} < 5, 1, 0)` |
| `f_dependent` | calculate |  |  |  |  | `if(${m_age} < 15 or ${m_age} > 64, 1, 0)` |
| `f_working` | calculate |  |  |  |  | `if(${m_age} >= 15 and ${m_age} <= 64, 1, 0)` |
| `n_school_age` | calculate |  |  |  |  | `sum(${f_school_age})` |
| `n_out_school` | calculate |  |  |  |  | `sum(${f_out_school})` |
| `n_under5` | calculate |  |  |  |  | `sum(${f_under5})` |
| `n_dependent` | calculate |  |  |  |  | `sum(${f_dependent})` |
| `n_working` | calculate |  |  |  |  | `sum(${f_working})` |
| `dep_ratio` | calculate |  |  |  |  | `if(${n_working} > 0, round(${n_dependent} div ${n_working}, 2), 99)` |
| `has_under5` | calculate |  |  |  |  | `if(${n_under5} > 0, 1, 0)` |
| `roster_check` | calculate |  |  |  |  | `if(count(${m_age}) = ${hh_size}, 1, 0)` |
| `u5_sick` | select_one yesno | Did any child under 5 have diarrhoea or fever in the last 2 weeks? | yes | `${has_under5} = 1` |  |  |
| `u5_muac` | select_one yesno | Was any child under 5 screened for malnutrition in the last 3 months? | yes | `${has_under5} = 1` |  |  |
| `g_livelihood` | begin_group | Section 3: Livelihoods |  | `${consent} = 'yes'` |  |  |
| `main_income` | select_one income_src | Main source of household income | yes |  |  |  |
| `land_total` | decimal | Total land cultivated (hectares) | yes |  | `. >= 0 and . <= 50` |  |
| `land_khat` | decimal | Hectares under khat | yes |  | `. >= 0` |  |
| `land_sorghum` | decimal | Hectares under sorghum | yes |  | `. >= 0` |  |
| `land_maize` | decimal | Hectares under maize | yes |  | `. >= 0` |  |
| `land_other` | decimal | Hectares under other crops | yes |  | `. >= 0 and (${land_khat} + ${land_sorghum} + ${land_maize} + .) <= ${land_total}` |  |
| `khat_share` | calculate |  |  |  |  | `if(${land_total} > 0, round(${land_khat} div ${land_total} * 100, 0), 0)` |
| `n_cattle` | integer | Number of cattle owned | yes |  | `. >= 0 and . <= 500` |  |
| `n_camel` | integer | Number of camels owned | yes |  | `. >= 0 and . <= 500` |  |
| `n_shoat` | integer | Number of sheep and goats owned | yes |  | `. >= 0 and . <= 1000` |  |
| `n_donkey` | integer | Number of donkeys owned | yes |  | `. >= 0 and . <= 500` |  |
| `n_poultry` | integer | Number of poultry owned | yes |  | `. >= 0 and . <= 1000` |  |
| `tlu` | calculate |  |  |  |  | `round(${n_cattle} * 0.7 + ${n_camel} * 1.0 + ${n_shoat} * 0.1 + ${n_donkey} * 0.5 + ${n_poultry} * 0.01, 2)` |
| `any_shock` | select_one yesno | Did the household experience any shock in the last 12 months? | yes |  |  |  |
| `g_shock` | begin_group | Shocks in the last 12 months |  | `${any_shock} = 'yes'` |  |  |
| `shocks` | select_multiple shock_types | Which shocks did the household experience? | yes |  |  |  |
| `shock_crop_loss` | integer | What percentage of the harvest was lost? | yes | `selected(${shocks}, 'crop_failure')` | `. >= 0 and . <= 100` |  |
| `shock_livestock_loss` | integer | How many livestock were lost? | yes | `selected(${shocks}, 'livestock_disease')` | `. >= 0` |  |
| `shock_market_effect` | select_one market_effect | How did the market disruption affect the household? | yes | `selected(${shocks}, 'market_disruption')` |  |  |
| `shock_worst` | select_one shock_types | Which was the worst shock? | yes | `count-selected(${shocks}) > 1` |  |  |
| `shock_coping` | select_multiple coping_actions | How did the household cope with the shock? | yes |  |  |  |
| `g_food` | begin_group | Section 4: Food security |  | `${consent} = 'yes'` |  |  |
| `hhs_intro` | note | In the past 4 weeks (30 days): |  |  |  |  |
| `hhs1` | select_one yesno | Was there ever no food of any kind to eat in your house because of lack of resources? | yes |  |  |  |
| `hhs1_f` | select_one hhs_freq | How often did this happen? | yes | `${hhs1} = 'yes'` |  |  |
| `hhs2` | select_one yesno | Did you or any household member go to sleep hungry because there was not enough food? | yes |  |  |  |
| `hhs2_f` | select_one hhs_freq | How often did this happen? | yes | `${hhs2} = 'yes'` |  |  |
| `hhs3` | select_one yesno | Did you or any household member go a whole day and night without eating anything? | yes |  |  |  |
| `hhs3_f` | select_one hhs_freq | How often did this happen? | yes | `${hhs3} = 'yes'` |  |  |
| `hhs1_s` | calculate |  |  |  |  | `if(${hhs1} = 'no', 0, if(${hhs1_f} = 'often', 2, 1))` |
| `hhs2_s` | calculate |  |  |  |  | `if(${hhs2} = 'no', 0, if(${hhs2_f} = 'often', 2, 1))` |
| `hhs3_s` | calculate |  |  |  |  | `if(${hhs3} = 'no', 0, if(${hhs3_f} = 'often', 2, 1))` |
| `hhs_score` | calculate |  |  |  |  | `${hhs1_s} + ${hhs2_s} + ${hhs3_s}` |
| `hhs_cat` | calculate |  |  |  |  | `if(${hhs_score} <= 1, 'little_none', if(${hhs_score} <= 3, 'moderate', 'severe'))` |
| `rcsi_intro` | note | In the past 7 days, how many days did the household have to: |  |  |  |  |
| `rcsi_pref` | integer | Rely on less preferred or less expensive food? | yes |  | `. >= 0 and . <= 7` |  |
| `rcsi_borrow` | integer | Borrow food or rely on help from friends or relatives? | yes |  | `. >= 0 and . <= 7` |  |
| `rcsi_portion` | integer | Limit portion size at mealtimes? | yes |  | `. >= 0 and . <= 7` |  |
| `rcsi_adult` | integer | Restrict adult consumption so small children could eat? | yes |  | `. >= 0 and . <= 7` |  |
| `rcsi_meals` | integer | Reduce the number of meals eaten per day? | yes |  | `. >= 0 and . <= 7` |  |
| `rcsi_score` | calculate |  |  |  |  | `${rcsi_pref} * 1 + ${rcsi_borrow} * 2 + ${rcsi_portion} * 1 + ${rcsi_adult} * 3 + ${rcsi_meals} * 1` |
| `rcsi_cat` | calculate |  |  |  |  | `if(${rcsi_score} <= 3, 'low', if(${rcsi_score} <= 18, 'medium', 'high'))` |
| `g_wash` | begin_group | Section 5: Water, sanitation and hygiene |  | `${consent} = 'yes'` |  |  |
| `water_dry` | select_one water_src | Main source of drinking water in the dry season | yes |  |  |  |
| `water_wet` | select_one water_src | Main source of drinking water in the wet season | yes |  |  |  |
| `water_dist` | select_one water_dist | Distance to the dry-season water source | yes | `${water_dry} != 'piped_plot'` |  |  |
| `water_time` | integer | Round-trip time to fetch water (minutes) | yes | `${water_dry} != 'piped_plot'` | `. >= 1 and . <= 480 and not(${water_dist} = 'under_500m' and . > 60)` |  |
| `water_queue` | integer | Minutes spent waiting in the queue | yes | `${water_dry} != 'piped_plot'` | `. >= 0 and . <= 480` |  |
| `water_enough` | select_one yesno | Did the household have enough water for all needs in the last 7 days? | yes |  |  |  |
| `water_treat` | select_one water_treat | How is drinking water usually treated? | yes |  |  |  |
| `san_type` | select_one san_type | What type of toilet does the household use? | yes |  |  |  |
| `san_share` | select_one yesno | Is the toilet shared with other households? | yes | `${san_type} != 'open_defecation'` |  |  |
| `hw_place` | select_one yesno | Is there a handwashing place? (observe) | yes |  |  |  |
| `hw_soap` | select_one yesno | Is soap or ash available at the handwashing place? (observe) | yes | `${hw_place} = 'yes'` |  |  |
| `g_verify` | begin_group | Section 6: Verification |  | `${consent} = 'yes'` |  |  |
| `gps` | geopoint | Capture the GPS location (stand outside the home) | yes |  | `number(selected-at(., 3)) <= 20` |  |
| `gps_box` | calculate |  |  |  |  | `if(number(selected-at(${gps}, 0)) >= 8.0 and number(selected-at(${gps}, 0)) <= 10.0 and number(selected-at(${gps}, 1)) >= 40.0 and number(selected-at(${gps}, 1)) <= 43.5, 1, 0)` |
| `gps_warn` | note | Warning: the location appears to be outside the Hararghe area. |  | `${gps} != '' and ${gps_box} = 0` |  |  |
| `photo_house` | image | Photo of the dwelling | yes |  |  |  |
| `photo_plot` | image | Photo of the farm plot | yes | `${land_total} > 0` |  |  |
| `consent_sig` | image | Respondent signature | yes |  |  |  |
| `enum_notes` | text | Enumerator notes (optional) |  |  |  |  |
| `summary_note` | note | Summary: HHS score ${hhs_score} (${hhs_cat}). rCSI score ${rcsi_score} (${rcsi_cat}). TLU ${tlu}. Dependency ratio ${dep_ratio}. |  |  |  |  |
