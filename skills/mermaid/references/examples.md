# Mermaid Diagram Examples

Complete examples of common diagram patterns.

## API Request Flow (Sequence Diagram)

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Auth
    participant API
    participant DB
    
    Client->>Gateway: POST /api/data
    Gateway->>Auth: Validate token
    Auth-->>Gateway: OK
    Gateway->>API: Forward request
    API->>DB: Query data
    DB-->>API: Results
    API-->>Gateway: Response
    Gateway-->>Client: 200 OK
```

## State Machine (Authentication)

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated
    Unauthenticated --> Authenticating: Login attempt
    Authenticating --> Authenticated: Success
    Authenticating --> Unauthenticated: Failure
    Authenticated --> Unauthenticated: Logout
    Authenticated --> Authenticated: Refresh token
    Authenticated --> [*]: Session expired
```

## Data Pipeline (Flowchart)

```mermaid
flowchart LR
    Source1[(Raw Data 1)] --> Ingest[Data Ingestion]
    Source2[(Raw Data 2)] --> Ingest
    Source3[(Raw Data 3)] --> Ingest
    
    Ingest --> Clean[Data Cleaning]
    Clean --> Transform[Transform]
    
    Transform --> Validate{Valid?}
    Validate -->|Yes| Load[Load to DW]
    Validate -->|No| Error[Error Queue]
    
    Load --> DW[(Data Warehouse)]
    Error --> Alert[Send Alert]
    
    style Source1 fill:#e1f5ff
    style Source2 fill:#e1f5ff
    style Source3 fill:#e1f5ff
    style DW fill:#d4edda
    style Error fill:#f8d7da
```

## Decision Tree (User Onboarding)

```mermaid
flowchart TD
    Start([New User]) --> HasAccount{Has Account?}
    
    HasAccount -->|No| Register[Register]
    HasAccount -->|Yes| Login[Login]
    
    Register --> Verify{Email Verified?}
    Verify -->|No| SendEmail[Send Verification]
    Verify -->|Yes| Profile
    SendEmail --> WaitVerify[Wait for Click]
    WaitVerify --> Profile[Complete Profile]
    
    Login --> Auth{Auth Success?}
    Auth -->|No| Retry[Show Error]
    Auth -->|Yes| Dashboard
    Retry --> Login
    
    Profile --> Dashboard([Dashboard])
    
    style Start fill:#e1f5ff
    style Dashboard fill:#d4edda
    style Retry fill:#fff3cd
```

## System Architecture (Component Diagram)

```mermaid
flowchart TB
    subgraph Frontend
        Web[Web App]
        Mobile[Mobile App]
    end
    
    subgraph API Layer
        Gateway[API Gateway]
        Auth[Auth Service]
    end
    
    subgraph Services
        User[User Service]
        Order[Order Service]
        Payment[Payment Service]
    end
    
    subgraph Data
        UserDB[(User DB)]
        OrderDB[(Order DB)]
        Cache[(Redis Cache)]
    end
    
    Web --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> User
    Gateway --> Order
    
    Order --> Payment
    User --> UserDB
    Order --> OrderDB
    User --> Cache
    
    style Gateway fill:#fff3cd
    style Auth fill:#fff3cd
    style Cache fill:#e1f5ff
```

## CI/CD Pipeline (Gantt Chart)

```mermaid
gantt
    title Deployment Pipeline
    dateFormat HH:mm
    
    section Build
    Clone Repo: done, 00:00, 2m
    Install Deps: done, 00:02, 5m
    Run Tests: done, 00:07, 8m
    Build Assets: active, 00:15, 10m
    
    section Deploy
    Push to Registry: 00:25, 3m
    Update Staging: 00:28, 5m
    Health Check: 00:33, 2m
    Deploy Production: 00:35, 10m
```

## Error Handling Flow

```mermaid
flowchart TD
    Request[Incoming Request] --> Try{Try}
    
    Try -->|Success| Process[Process Data]
    Try -->|Error| Catch[Catch Error]
    
    Catch --> Type{Error Type?}
    Type -->|Network| Retry[Retry with Backoff]
    Type -->|Validation| Reject[400 Bad Request]
    Type -->|Auth| Unauthorized[401 Unauthorized]
    Type -->|Server| Log[Log & Alert]
    
    Retry --> Attempts{Attempts < 3?}
    Attempts -->|Yes| Try
    Attempts -->|No| Fail[503 Service Unavailable]
    
    Process --> Success([200 OK])
    Reject --> End([Return Error])
    Unauthorized --> End
    Log --> Fail
    Fail --> End
    
    style Success fill:#d4edda
    style Reject fill:#f8d7da
    style Unauthorized fill:#f8d7da
    style Fail fill:#f8d7da
```

## Multi-Stage Approval

```mermaid
flowchart LR
    Submit([Submit Request]) --> Review1{Manager<br/>Approval}
    
    Review1 -->|Reject| Denied1[Rejected]
    Review1 -->|Approve| Review2{Finance<br/>Approval}
    
    Review2 -->|Reject| Denied2[Rejected]
    Review2 -->|Approve| Review3{Executive<br/>Approval}
    
    Review3 -->|Reject| Denied3[Rejected]
    Review3 -->|Approve| Execute[Execute Request]
    
    Execute --> Complete([Completed])
    
    Denied1 --> Archive[Archive]
    Denied2 --> Archive
    Denied3 --> Archive
    
    style Submit fill:#e1f5ff
    style Complete fill:#d4edda
    style Archive fill:#6c757d
```

## Use These As Templates

Copy and modify these examples for your specific use cases. Focus on:

- Clear node naming (not `A`, `B`, `C`)
- Consistent styling for similar elements
- Logical flow direction
- Color coding for status/importance
