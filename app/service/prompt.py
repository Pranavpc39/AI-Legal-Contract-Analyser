CONTRACT_ANALYSIS_PROMPT="""
    You are an expert legal analyst specializing in Indian contract law.
    Analyze the following contract text and provide a structured analysis

    CONTRACT_TEXT:
    {contract_text}

    provide you analysis as a JSON object with exactly this structure:
    {{
    "summary":"A 2-3 sentence summary of what this contract is about"
    "contract_type":"The type of contract (e.g., NDA, Service Agreement, Employment Contract)",
    "key_clauses":[
        {{
            "clause_title":"name of the clause",
            "clause_text":"the relevant text from the contract",
            "explanation":"what this clause means in simple terms".
            "is_standard": true of false
        }}
    ],
    "risk_flag":[
        {{
            "risk_title":"short title of the risk",
            "description":"what the risk is",
            "risk_level":"low" or "medium" or "high" or "critical",
            "recommendation":"what to do about it",
            "clause_reference":"Which clause this refers to"
        }}
    ],
    "overall_risk_level":"low" or "medium" or "critical",
    "recommendations":[
        "Recommendation 1",
        "Recommendation 2",
    ]
    }}

    Rules:
    -  Identify at least 3-5 key clauses
    -  Flag any unusual, missing, or one-sided clauses as risks
    -  Be specific with clause references
    -  Keep explanations simple and clear
    -  Return ONLY the JSON object, no other text
"""

CLAUSE_EXTRACTION_PROMPT="""
    Extract all distinct clauses from this contract text.
    For each clause, provide the title and the full text.

    Contract TEXT:
    {contract_text}

    return as a JSON array:
    [
        {{
            "clause_title": "Titile",
            "clause_text": "Full text of the clause"
        }}
    ]

    return ONLY the JSON arrya, no other text.
"""

RISK_ASSESSMENT_PROMPT="""
    You are legal risk assessor. Review these contract clauses and flag risks.

    CLAUSES:
    {clauses_text}

    For each risk found, provide:
    {{
        "risk_title": "Short title",
        "description": "What makes this risky",
        "risk_level": "low" or "medium" or "high" or "critical",
        "recommendation": "What to do",
        "clause_reference": "Which clause"
    }}

    Return as a JSON array. Return ONLY the JSON array, no other text.
"""

SUMMARY_PROMPT="""
    Summarize this contract in 3-4 sentences for a non-lawyer.
    Include: what it's about,who the parties are, key obligations, and duration.

    CONTRACT TEXT:
    {contract_text}

    return only the summary text, no JSON.
"""