%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#E6F1FB', 'primaryBorderColor': '#378ADD', 'primaryTextColor': '#0C447C', 'secondaryColor': '#E1F5EE', 'secondaryBorderColor': '#1D9E75', 'secondaryTextColor': '#085041', 'tertiaryColor': '#FAECE7', 'tertiaryBorderColor': '#D85A30', 'tertiaryTextColor': '#712B13'}}}%%

flowchart TD
    A["🎤 User Input<br/><i>Natural language request</i>"] --> B
    B["🧠 Planner Agent (LLM)<br/><i>Parse intent → UserProfile</i>"] --> C
    C["🎵 Recommender Engine<br/><i>Weighted scoring on catalog</i>"] --> D
    D["💬 Explainer Agent (LLM)<br/><i>Generate friendly response</i>"] --> E
    E["🔍 Evaluator (Guardrail)<br/><i>Confidence score + validation</i>"] --> F{Confidence<br/>≥ 0.5?}

    F -- "Yes ✓" --> G["📋 Final Output<br/><i>Recommendations + explanations</i>"]
    F -- "No ✗" --> H["🔄 Refine Profile<br/><i>Relax constraints</i>"]
    H --> B

    I[("📀 Song Catalog<br/><i>CSV · 20 songs</i>")] --> C
    J["📝 Logger<br/><i>All steps recorded</i>"] -.-> B
    J -.-> C
    J -.-> D
    J -.-> E

    K["🧪 Test Harness<br/><i>Batch evaluation</i>"] -.-> A

    style A fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style B fill:#EEEDFE,stroke:#534AB7,color:#26215C
    style C fill:#E1F5EE,stroke:#0F6E56,color:#04342C
    style D fill:#EEEDFE,stroke:#534AB7,color:#26215C
    style E fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style F fill:#FAEEDA,stroke:#854F0B,color:#412402
    style G fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style H fill:#FAEEDA,stroke:#854F0B,color:#412402
    style I fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style J fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style K fill:#FAEEDA,stroke:#854F0B,color:#412402
