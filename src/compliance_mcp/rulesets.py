RULESETS = {
    "data_privacy_basics": [
        {
            "id": "retention_period",
            "question": "Does the document specify how long data is retained?",
            "pass_criteria": "PASS only if a specific retention duration or deletion trigger is stated. General statements about deleting data on request do not count.",
        },
        {
            "id": "breach_notification",
            "question": "Does the document describe a process for notifying people after a data breach?",
            "pass_criteria": "PASS only if a notification process or commitment after a breach is explicitly mentioned. Silence on breaches means FAIL.",
        },
        {
            "id": "dpo_named",
            "question": "Does the document name a specific person or role responsible for data protection?",
            "pass_criteria": "PASS if a named person or clearly defined role (e.g. 'Data Protection Officer') is given.",
        },
        {
            "id": "third_party_sharing",
            "question": "Does the document disclose whether data is shared with third parties?",
            "pass_criteria": "PASS if the document states either that data IS shared with third parties, or explicitly states it is NOT. FAIL only if the document is silent on the topic entirely.",
        },
        {
            "id": "user_rights",
            "question": "Does the document describe a user's right to access, correct, or delete their data, with a way to exercise that right?",
            "pass_criteria": "PASS if a right is stated AND a mechanism (form, email, account settings) is given, even if informal.",
        },
    ]
}
