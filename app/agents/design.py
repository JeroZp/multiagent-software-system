def design_agent():

    er_diagram = """
erDiagram
    USER ||--o{ ACCOUNT : owns
    USER ||--o{ TRANSACTION : performs
    ACCOUNT ||--o{ TRANSACTION : contains
"""

    sequence_diagram = """
sequenceDiagram
    participant User
    participant App
    participant Backend
    participant PaymentService

    User->>App: Initiate Payment
    App->>Backend: Request
    Backend->>PaymentService: Process
    PaymentService-->>Backend: Result
    Backend-->>App: Response
    App-->>User: Confirmation
"""

    return {
        "er": er_diagram,
        "sequence": sequence_diagram
    }
