# Independent verification of the footage — October 13, 2026

This folder documents a second, independent pass over the raw evidence files in [`../videos/`](../videos/), performed with ffmpeg/ffprobe on October 13, 2026. It confirms the readings and speed estimates in [`../report/collision-report.md`](../report/collision-report.md) without relying on the original analysis.

## File integrity and metadata (ffprobe)

| File | Duration | Resolution | Location metadata | Notes |
| --- | --- | --- | --- | --- |
| `2026-08-07-04-46-26 4.MP4` | 30.6 s | 724×510, 24 fps | 37.8374, -122.2950 (Emeryville Supercharger) | Tesla app export, rear camera, telemetry overlay |
| `2026-08-07-04-46-26 3.MP4` | 29.2 s | 724×510, 24 fps | 37.8374, -122.2950 | Tesla app export, side camera, telemetry overlay |
| `IMG_3887_2.MOV` | 32.5 s | 1280×720, 30 fps | 37.7818, -122.4067 | iPhone 16 Pro Max, created 2026-08-07 12:49:17 PDT |
| `IMG_3887_3.MOV` | 32.5 s | 1280×720, 30 fps | 37.7818, -122.4067 | Same creation date; a third uploaded copy (`IMG_3887_4.MOV`) was MD5-identical to this file and was not duplicated |

The iPhone clips, filmed about an hour after the 11:46 AM collision, record the in-car Dashcam playback and independently confirm the original recording's date, time and place.

## Telemetry readings observed (rear camera export)

Read directly from the gear/speed overlay in the extracted frames (grids in [`frame-grids/`](frame-grids/)):

| Clip time | Overlay reads | Scene |
| --- | --- | --- |
| 21.0 s | R, 0–1 MPH | Reversing begins; aisle behind is clear |
| 22.0–23.0 s | R, 3–4 MPH | Reversing; Kia Soul appears, approaching along the aisle |
| 23.5 s | R, 3 MPH | Kia closing |
| 23.75 s | R, 1 MPH | Braking; Kia's nose almost at the bumper |
| 24.0 s | **R, 0 MPH** | **Contact — the Kia's front corner fills the rear camera while the Model Y is stopped** |
| 24.25–25.5 s | 0 MPH (gear to D ≈24.4 s) | The Kia's left side slides across the entire rear; the Model Y never moves |
| 25.75–26.25 s | D, 0 MPH | The Kia clears the camera and stops a short distance past |

## Kia speed cross-check (pass-through timing)

The Kia Soul of this generation is 4.20 m long. Its nose reaches the fixed rear camera at ≈23.8–23.9 s and its rear bumper clears it at ≈25.5–25.8 s: 4.20 m past a fixed point in ≈1.7–1.9 s is an **average of about 5–6.5 MPH while decelerating**. Since the car was braking through the pass and stopped ≈2 s later, its speed at first contact was above that average — consistent with the report's **6–9 MPH at impact** and with the separately measured 13–16 MPH approach ([`../data/kia-speed-estimates.csv`](../data/kia-speed-estimates.csv)).

## Impact pulse — the body measurably moved on its suspension at 24.0 s

The side camera is rigidly mounted to the body, so once the vehicle is stationary, any image-wide shift is body motion. Frame-to-frame global image motion was measured at 24 fps by FFT phase correlation on a static background strip (building + sky), with the strip's left and right halves measured independently as a cross-check (script: [`scripts/measure_impact_pulse.py`](scripts/measure_impact_pulse.py)).

| Window | Frame-to-frame image motion |
| --- | --- |
| Reversing, 21.5–23.5 s | ≈5 px/frame — the car's own motion |
| Stationary, 23.79–23.96 s | ≤0.2 px (noise floor) |
| **24.000 s — contact** | **single vertical pulse: left half −2.10 px, right half −1.14 px, same direction, same frame** |
| Stationary, 24.04–24.79 s | ≤0.2 px |

**Validation** (exhibit: [`frame-grids/impact-pulse-validation.png`](frame-grids/impact-pulse-validation.png), differences amplified 6×):

1. *Control for moving objects:* during 24.50–24.54 s the Kia is still sliding through the camera's view, yet the background strip's mean absolute change is only 0.15 — an object moving through the scene does not create the signal.
2. *The contact pair* (23.958 → 24.000 s) measures 1.62 mean absolute change, about **10× the control**, with edge ghosting across the entire background (cloud edges, roofline, pole) — which only motion of the camera itself produces.
3. *Two independent halves* of the strip shift in the same direction in the same frame.

With the vehicle stationary, a one-frame, vertical, image-wide displacement at exactly the moment the rear camera shows the Kia's bodywork at the bumper means the body itself pitched — and a stationary car's body moves vertically only on its suspension. This is direct, measurable evidence that the impact force traveled through the structure and worked the suspension. The pixel magnitudes are reported as measured; converting them to millimetres depends on scene depth and is deliberately not attempted.

A frame of `IMG_3887_2.MOV` read in this session also shows the in-car Dashcam viewer labeled "Emeryville — Fri, Aug 7, 2026 11:46:33" with the car's own clock at 12:49 pm — the original recording's date, time and place confirmed from the vehicle's screen (exhibit: [`../exhibits/in-car-playback_emeryville-aug7.png`](../exhibits/in-car-playback_emeryville-aug7.png)).

## Impact mechanics — how big this hit was

Masses (published curb weights + 80 kg driver): Kia Soul 2,844 lb ([KBB 2020 Soul specs](https://www.kbb.com/kia/soul/2020/specs)) → ≈1,370 kg; Model Y Long Range AWD 4,363 lb → ≈2,059 kg.

Kinetic energy the Kia carried into contact at the estimated 6–9 MPH:

| Impact speed | Energy delivered |
| --- | --- |
| 6 MPH | ≈4.9 kJ |
| 9 MPH | ≈11.1 kJ |
| Federal no-damage test (2.5 MPH barrier, a car of the Model Y's weight) | ≈1.3 kJ |

The arithmetic, so anyone can check it (KE = ½mv²): 0.5 × 1,370 kg × (2.68 m/s)² = 4.9 kJ; 0.5 × 1,370 kg × (4.02 m/s)² = 11.1 kJ; test reference 0.5 × 2,059 kg × (1.12 m/s)² = 1.29 kJ.

**This impact carried 3.8–8.6 times the energy of the federal bumper test.** That matters because the federal bumper standard's protective criteria — the only regime in which a car's "propulsion, suspension, steering, and braking systems shall remain in adjustment" — end at 2.5 MPH ([49 CFR 581.5(c)(5)](https://www.law.cornell.edu/cfr/text/49/581.5); paragraph numbering confirmed by [NHTSA interpretation 16-000385](https://www.nhtsa.gov/interpretations/16-000385-49-cfr-part-581-response-alliance-global)). Above that speed, no rule protects the suspension from being knocked out of adjustment; at 4–9× the test energy, alignment-relevant damage is a foreseeable outcome, not an exotic claim.

Load-path note (general vehicle design, to be confirmed on this car by the shop): the impact centered on the liftgate and rear bumper; the rear bumper structure mounts to the body's rear structure, which also carries the rear suspension's mounting points — the same corner where the owner reports the right-rear wheel's inward lean and inner-shoulder tire wear.

What this analysis deliberately does not claim: no video or calculation can see inside a suspension. The determination belongs to the four-wheel alignment measurement and component inspection requested in the report — Tesla's own Service Manual ("Alignment Requirement — Suspension", [2025 edition](https://service.tesla.com/docs/ModelY/ServiceManual/2025/en-us/GUID-36116414-79E1-4EF0-91C3-3643C36586B2.html)) notes the quick EPAS check should not be used to find collision suspension damage, pointing to the full four-wheel alignment check instead.

## Method notes

- Frames were extracted with ffmpeg at fixed timestamps, without alteration; grids in `frame-grids/` tile them in time order.
- The Model Y's speeds need no estimation: they are burned into the export by Tesla's software.
- All speed figures for the Kia are estimates from the footage; the raw clips are included so anyone can repeat the measurement.
