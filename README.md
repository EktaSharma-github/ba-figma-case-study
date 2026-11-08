# Halden Logistics: Expense Reimbursement Redesign

A portfolio project for a **Functional Business Analyst** role. It shows the full BA workflow in Figma/FigJam: discovery → current-state analysis → future-state design → solution wireframes → requirements & traceability → business case.

> Halden Logistics is a fictional company. All figures are illustrative portfolio data. Say so when you present it.

## The case in one paragraph

Halden is a 1,200-person logistics firm. Field staff claim travel expenses with an Excel template and paper receipts. Claims take **14.2 working days** to be paid, **31%** are returned at least once, and AP re-keys every line into the ERP. As the BA, you mapped the process, found 5 root-cause pain points, designed a to-be process with OCR capture, a policy engine and an ERP integration, wrote the requirements, and ran an 8-week pilot. Cycle time fell to **3.1 days**.

## What's in this folder

| File | What it shows | BA skill demonstrated |
|---|---|---|
| `figma-frames/01-stakeholder-map.svg` | Power/interest grid + interview quotes | Stakeholder analysis, elicitation |
| `figma-frames/02-as-is-process.svg` | BPMN swimlane, 4 lanes, numbered pain points | Process mapping, root-cause analysis |
| `figma-frames/03-to-be-process.svg` | Future-state BPMN with automation + risk-based routing | Process redesign, solution thinking |
| `figma-frames/04-journey-map.svg` | Persona journey with emotion curve | Customer/user empathy, opportunity framing |
| `figma-frames/05-wireframes.svg` | 3 mobile screens + desktop approver queue, annotated with requirement IDs | Functional design, UI/UX collaboration |
| `figma-frames/06-requirements-rtm.svg` | User story + Gherkin AC, MoSCoW backlog, RTM | Requirements engineering, traceability |
| `figma-frames/07-impact-kpis.svg` | KPI tiles, pilot chart, business case | Benefits realisation, stakeholder reporting |
| `build_frames.py` | Regenerates every SVG (`python3 build_frames.py`) | — |

## Build it in Figma (about 2–3 hours)

The SVGs are a starting point. Importing them is fast, but rebuilding the key parts *natively* is what proves your Figma skills to a reviewer who opens the file.

### 1. Set up the file
Create a Figma Design file named **"Halden – Expense Reimbursement (BA Case Study)"** with these pages:

```
📄 00 Cover
📄 01 Discovery         ← stakeholder map
📄 02 Process (As-Is)
📄 03 Process (To-Be)
📄 04 Journey
📄 05 Wireframes + Prototype
📄 06 Requirements & RTM
📄 07 Impact
📄 🧱 Library            ← components + variables
```

### 2. Import the frames
Drag each SVG onto its page. Figma converts it into vector layers with live, editable text. Select the result and press **Ctrl/Cmd + Alt + G** (Frame selection) so each one is a proper frame. Rename it, e.g. `02 / As-Is / v1`.

### 3. Create variables (Library page)
Local variables → new collection **"Halden tokens"**:

| Variable | Value | Use |
|---|---|---|
| `color/ink` | `#1B2430` | text, strokes |
| `color/muted` | `#5B6676` | secondary text |
| `color/line` | `#C9D1DB` | borders |
| `color/canvas` | `#F3F5F8` | frame background |
| `color/human` | `#1F5FAD` / tint `#E3EDF9` | human tasks, primary action |
| `color/auto` | `#0F7B6C` / tint `#DDF2EE` | automated tasks, success |
| `color/system` | `#5B4BB7` / tint `#ECE9FA` | integrations |
| `color/risk` | `#B93A32` / tint `#FBE6E4` | pain points, errors |
| `color/warn` | `#A86A00` / tint `#FDF0D5` | gateways, warnings |
| `space/sm, md, lg` | 8 / 16 / 24 | auto-layout gaps |

Bind fills on the imported frames to these variables. This is a quick win reviewers notice.

### 4. Build components (Library page)
Rebuild these natively with **Auto Layout** and **variants**, then swap them into the imported frames:

- **BPMN / Task**: variants `type = human | automated | system`
- **BPMN / Gateway**, **BPMN / Event** (`start | end`)
- **Pain point marker**: number as a text property
- **Status pill**: variants `Done | In test | Build | Backlog`
- **Input field**: variants `default | ocr-filled | error`
- **Button**: variants `primary | secondary`
- **Req annotation**: sticky-note callout with a text property for the IDs

Use **component properties** (text + boolean) so one component covers every case.

### 5. Connectors
For the swimlanes, replace the static arrows with FigJam-style connectors (paste the process into a **FigJam** board), or keep them in Design using the **Autoflow** plugin. Connectors that follow the boxes when you move them show you understand the tool.

### 6. Prototype the wireframes
On page 05:
1. Duplicate the three mobile frames to sit at **iPhone 15 (393×852)** size.
2. Link *Scan* → *Review* (On tap, Smart animate), *Continue* → *Submitted*.
3. Make the amount field an **interactive component**: tapping *Continue* with ₹6,850 swaps the field to `error` and shows the policy banner.
4. Set a **flow starting point** called "Claimant happy path".

### 7. Dev Mode and handoff
- Mark frames 05 and 06 **Ready for dev**.
- Add Dev Mode annotations to fields: data type, validation rule, source system (e.g. `Amount · decimal(12,2) · BR-07 · ERP: WRBTR`).

### 8. Cover page
Title, your name, role ("Functional BA"), a 2-line problem statement, the 4 KPI tiles from frame 07, and a thumbnail grid of the other pages.

## Talking points for interviews

- **Why swimlanes:** handoffs between lanes are where the delay lived. 4 of 5 pain points sit on a lane boundary.
- **Risk-based routing:** rather than removing approvals, the policy engine routes by risk so managers only see what needs judgement. Low-risk claims skip the manager.
- **Traceability:** every requirement links back to a pain point and forward to a screen and a UAT case. If a requirement traces to nothing, cut it.
- **Gherkin acceptance criteria:** QA wrote test cases straight from them, so fewer defects came back to the BA during SIT.
- **What I'd do next:** add mileage claims, corporate-card feeds and per-diem rules, and run a second pilot in the highest-volume region.

## Resume bullet

> Led functional analysis for an expense-reimbursement redesign: mapped as-is/to-be BPMN processes, defined 32 MoSCoW-prioritised requirements with Gherkin acceptance criteria and full traceability, and designed annotated Figma wireframes and a clickable prototype. Pilot cut claim cycle time from 14.2 to 3.1 days *(portfolio case study)*.
