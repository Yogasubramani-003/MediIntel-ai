from typing import Dict, List

DRUG_INTERACTIONS = {
    "warfarin": ["aspirin", "ibuprofen", "naproxen"],
    "metformin": ["ibuprofen", "cimetidine"],
    "lisinopril": ["spironolactone", "ibuprofen"],
    "atorvastatin": ["gemfibrozil", "erythromycin"],
}

ALLERGY_ALERTS = ["penicillin", "aspirin", "sulfa", "ibuprofen", "latex"]


def build_risk_alert(title: str, description: str, severity: str) -> Dict[str, str]:
    return {"title": title, "description": description, "severity": severity}


def normalize_value(value: str) -> float:
    try:
        return float(value.replace("mg", "").replace("g", "").replace("%", "").strip())
    except Exception:
        return 0.0


def compute_risks(extracted: Dict[str, any]) -> List[Dict[str, str]]:
    risks = []
    meds = [m.get("drug_name", "").lower() for m in extracted.get("medications", []) if m.get("drug_name")]
    allergies = (extracted.get("allergies") or "").lower()
    if allergies:
        for allergen in ALLERGY_ALERTS:
            if allergen in allergies:
                risks.append(build_risk_alert(
                    title="Allergy Conflict",
                    description=f"The report mentions allergy to {allergen}. Review prescribed medication carefully.",
                    severity="Red"
                ))
                break
    for med in meds:
        if med in DRUG_INTERACTIONS:
            conflicts = [x for x in DRUG_INTERACTIONS[med] if x in meds]
            if conflicts:
                risks.append(build_risk_alert(
                    title="Drug Interaction",
                    description=f"{med.title()} may interact with {', '.join(conflicts)}.",
                    severity="Dark Red"
                ))
    if not risks and meds:
        risks.append(build_risk_alert(
            title="No Major Interactions Detected",
            description="Medication analysis did not detect high-risk interactions from the extracted report.",
            severity="Green"
        ))
    glucose = normalize_value(extracted.get("glucose") or "0")
    if glucose and glucose > 140:
        risks.append(build_risk_alert(
            title="Glucose Alert",
            description=f"Elevated glucose value detected ({glucose}). Monitor for hyperglycemia.",
            severity="Orange"
        ))
    if extracted.get("blood_pressure"):
        bp = extracted["blood_pressure"]
        if "/" in bp:
            systolic, diastolic = bp.split("/")
            try:
                if int(systolic) >= 140 or int(diastolic) >= 90:
                    risks.append(build_risk_alert(
                        title="Blood Pressure Risk",
                        description=f"Hypertensive blood pressure detected ({bp}).",
                        severity="Orange"
                    ))
            except ValueError:
                pass
    return risks
