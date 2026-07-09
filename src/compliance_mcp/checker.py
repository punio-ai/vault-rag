import httpx
import json
from compliance_mcp.config import settings
from compliance_mcp.vectorstore import query_document
from compliance_mcp.rulesets import RULESETS

CHECK_PROMPT_TEMPLATE = """You are auditing a document against a specific compliance requirement.

Requirement: {question}
Pass criteria: {pass_criteria}

Example: if a document says "We share data with our marketing partners," that IS an explicit \
disclosure of third-party sharing — verdict should be "pass" for that criterion, even though \
it doesn't use the exact words "third party."

Relevant excerpt from the document:
\"\"\"
{evidence}
\"\"\"

Based ONLY on this excerpt and the pass criteria above, judge the requirement.
Respond with ONLY valid JSON, no other text, in this exact format:
{{"verdict": "pass" | "fail" | "unclear", "reason": "one sentence explanation"}}

If the excerpt doesn't contain enough information to judge, use "unclear" — do not guess."""


def _ask_llm(prompt: str) -> dict:
    response = httpx.post(
        f"{settings.OLLAMA_HOST}/api/generate",
        json={
            "model": settings.LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.0}
        },
        timeout=60.0,
    )
    response.raise_for_status()
    raw = response.json()["response"]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"verdict": "unclear", "reason": "Could not parse model response."}


def check_document(doc_id: str, ruleset_name: str) -> dict:
    if ruleset_name not in RULESETS:
        return {"status": "error", "message": f"Unknown ruleset: {ruleset_name}"}

    rules = RULESETS[ruleset_name]
    results = []

    for rule in rules:
        evidence_chunks = query_document(doc_id, rule["question"], n_results=1)
        evidence = evidence_chunks[0][
            "text"] if evidence_chunks else "(no relevant content found)"

        prompt = CHECK_PROMPT_TEMPLATE.format(
            question=rule["question"],
            pass_criteria=rule["pass_criteria"],
            evidence=evidence,
        )
        verdict = _ask_llm(prompt)

        results.append({
            "rule_id": rule["id"],
            "question": rule["question"],
            "verdict": verdict.get("verdict", "unclear"),
            "reason": verdict.get("reason", ""),
            "evidence_snippet": evidence[:150],
        })

    passed = sum(1 for r in results if r["verdict"] == "pass")
    return {
        "doc_id": doc_id,
        "ruleset": ruleset_name,
        "score": f"{passed}/{len(rules)}",
        "results": results,
    }
