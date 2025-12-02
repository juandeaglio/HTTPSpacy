 Here is Claude's plan:
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
 TDD Implementation Plan: create_server() Function

 Overview

 Implement the create_server() composition root function using Test-Driven Development (TDD) with an inside-out approach, following hexagonal    
 architecture and event-driven design principles.

 Architecture

 ┌─────────────────────────────────────────────────────────┐
 │ Composition Root (src/config.py)                       │
 │  └─ create_server() - Dependency Injection             │
 └─────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ↓                ↓                ↓
 ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
 │ Event Bus   │  │ Tokenizer   │  │ Web Server  │
 │ (Adapter)   │  │ (Adapter)   │  │ (Adapter)   │
 └─────────────┘  └─────────────┘  └─────────────┘
         │                │                │
         └────────────────┼────────────────┘
                          ↓
         ┌────────────────────────────────┐
         │ SentencizeUseCase              │
         │ (Application Layer)            │
         └────────────────────────────────┘
                          │
                          ↓
         ┌────────────────────────────────┐
         │ Domain Layer                   │
         │  - Events                      │
         │  - Value Objects               │
         │  - Port Interfaces             │
         └────────────────────────────────┘

 Implementation Sequence

 Phase 1: Domain Layer (Pure Logic)

 1.1 Domain Events

 Files:
 - Test: tests/unit/domain/test_events.py
 - Implementation: src/domain/events.py

 TDD Steps:
 1. RED: Write test for SentencizeRequested event with text and timestamp
 2. GREEN: Implement as frozen dataclass with text: str and timestamp: datetime
 3. RED: Write test for TextTokenized event with sentences list and timestamp
 4. GREEN: Implement as frozen dataclass with sentences: List[str] and timestamp: datetime
 5. REFACTOR: Extract common event base if duplication emerges

 1.2 Value Objects

 Files:
 - Test: tests/unit/domain/test_value_objects.py
 - Implementation: src/domain/value_objects.py

 TDD Steps:
 1. RED: Test Text creation with valid input
 2. GREEN: Implement Text as frozen dataclass with value: str
 3. RED: Test Text rejects empty/whitespace-only strings
 4. GREEN: Add validation in __post_init__ raising ValueError
 5. RED: Test Sentences creation and to_list() method
 6. GREEN: Implement Sentences with value: List[str] and to_list() method
 7. REFACTOR: Ensure immutability and clear error messages

 1.3 Port Interfaces

 Files:
 - Test: tests/unit/domain/test_ports.py
 - Implementation: src/domain/ports.py

 TDD Steps:
 1. RED: Test that ISentenceTokenizer is abstract with tokenize() method
 2. GREEN: Define ISentenceTokenizer(ABC) with @abstractmethod tokenize(text: Text) -> Sentences
 3. RED: Test that IEventBus is abstract with publish() method
 4. GREEN: Define IEventBus(ABC) with @abstractmethod publish(event: Any) -> None
 5. REFACTOR: Ensure clear docstrings on interfaces

 Phase 2: Application Layer (Use Case Logic)

 2.1 SentencizeUseCase

 Files:
 - Test: tests/unit/application/test_sentencize_use_case.py
 - Implementation: src/application/sentencize_use_case.py

 TDD Steps:
 1. RED: Test use case constructor accepts tokenizer and event_bus
 2. GREEN: Implement __init__ storing dependencies
 3. RED: Test execute() calls tokenizer with Text object
 4. GREEN: Implement execute() creating Text and calling tokenizer.tokenize()
 5. RED: Test execute() publishes SentencizeRequested event before tokenization
 6. GREEN: Add event_bus.publish(SentencizeRequested(text=text)) before tokenization
 7. RED: Test execute() publishes TextTokenized event after tokenization
 8. GREEN: Add event_bus.publish(TextTokenized(sentences=sentences.to_list())) after tokenization
 9. RED: Test events are published in correct order
 10. GREEN: Verify order is: request event → tokenize → result event
 11. REFACTOR: Clean up method structure, ensure single responsibility

 Phase 3: Adapter Layer (Infrastructure)

 3.1 InMemoryEventBus

 Files:
 - Test: tests/unit/adapters/test_in_memory_event_bus.py
 - Implementation: src/adapters/events/in_memory_event_bus.py

 TDD Steps:
 1. RED: Test publish() delivers event to subscriber synchronously
 2. GREEN: Implement with defaultdict(list) storing handlers, publish() iterates handlers
 3. RED: Test publish() without subscribers doesn't fail
 4. GREEN: Use .get(event_type, []) to handle missing subscriptions
 5. RED: Test multiple subscribers receive same event
 6. GREEN: Ensure all handlers in list are called
 7. REFACTOR: Consider thread safety if needed (not required for synchronous case)

 3.2 SpacyTokenizer

 Files:
 - Test: tests/unit/adapters/test_spacy_tokenizer.py
 - Implementation: src/adapters/tokenizer/spacy_tokenizer.py

 TDD Steps:
 1. RED: Test tokenization of single sentence
 2. GREEN: Load spaCy model in __init__, implement tokenize() using nlp(text).sents
 3. RED: Test tokenization of multiple sentences
 4. GREEN: Ensure doc.sents iteration captures all sentences
 5. RED: Test with lorem ipsum text (7-8 sentences expected)
 6. GREEN: Strip whitespace from each sentence: [sent.text.strip() for sent in doc.sents]
 7. REFACTOR: Consider lazy model loading or model caching

 Note: Requires spacy package and en_core_web_sm model installed.

 3.3 FastAPI Adapter

 Files:
 - Test: tests/unit/adapters/test_fastapi_adapter.py
 - Implementation: src/adapters/web/fastapi_adapter.py

 TDD Steps:
 1. RED: Test create_fastapi_app() returns FastAPI instance
 2. GREEN: Implement function creating FastAPI() app
 3. RED: Test app has state.event_bus set
 4. GREEN: Add app.state.event_bus = event_bus
 5. RED: Test /sentencize route exists
 6. GREEN: Add @app.get("/sentencize") endpoint
 7. RED: Test endpoint calls use case and returns proper JSON
 8. GREEN: Implement handler calling use_case.execute(lorem_ipsum) and returning {"sentences": sentences.to_list()}
 9. REFACTOR: Extract lorem ipsum constant, consider making text dynamic in future

 3.4 BackgroundServer

 Files:
 - Test: tests/unit/adapters/test_background_server.py
 - Implementation: src/adapters/web/background_server.py

 TDD Steps:
 1. RED: Test BackgroundServer has app attribute
 2. GREEN: Implement __init__ accepting app, host, port parameters
 3. RED: Test start() method exists and returns immediately (non-blocking)
 4. GREEN: Implement start() launching uvicorn in daemon thread
 5. RED: Test stop() method exists
 6. GREEN: Implement stop() with thread join and timeout
 7. REFACTOR: Ensure uvicorn config uses log_level="error" to reduce noise in tests

 Phase 4: Composition Root

 4.1 create_server()

 Files:
 - Test: tests/unit/config.py (already exists)
 - Implementation: src/config.py

 TDD Steps:
 1. RED: Run existing unit test - should fail with import error
 2. GREEN: Implement create_server() function:
 def create_server() -> BackgroundServer:
     event_bus = InMemoryEventBus()
     tokenizer = SpacyTokenizer()
     use_case = SentencizeUseCase(tokenizer=tokenizer, event_bus=event_bus)
     app = create_fastapi_app(use_case=use_case, event_bus=event_bus)
     server = BackgroundServer(app=app, host="127.0.0.1", port=80)
     return server
 3. REFACTOR: Ensure clear comments explaining dependency injection flow

 Phase 5: Acceptance Test Validation

 File: tests/acceptance/test_serve_sentence.py (already exists)

 Validation Steps:
 1. Run acceptance test: python -m pytest tests/acceptance/test_serve_sentence.py -v
 2. Verify server starts in background
 3. Verify HTTP GET to http://127.0.0.1/sentencize returns valid JSON
 4. Verify response matches IpsumResponseModel schema
 5. Verify sentences list contains multiple sentences from lorem ipsum

 Event Flow

 HTTP GET /sentencize
     ↓
 FastAPI endpoint handler
     ↓
 use_case.execute(text)
     ↓
 [EVENT] event_bus.publish(SentencizeRequested(text))
     ↓
 tokenizer.tokenize(Text(text))
     ↓
 [EVENT] event_bus.publish(TextTokenized(sentences))
     ↓
 return Sentences
     ↓
 {"sentences": [...]}

 Critical Files to Modify

 1. src/config.py - Main composition root (currently empty)
 2. src/adapters/web/rest.py - Will be replaced by fastapi_adapter.py
 3. tests/unit/config.py - Integration test (already exists, needs to pass)
 4. tests/acceptance/test_serve_sentence.py - E2E test (already exists, needs to pass)

 New Files to Create

 Domain Layer:
 - src/domain/__init__.py
 - src/domain/events.py
 - src/domain/value_objects.py
 - src/domain/ports.py
 - tests/unit/domain/__init__.py
 - tests/unit/domain/test_events.py
 - tests/unit/domain/test_value_objects.py
 - tests/unit/domain/test_ports.py

 Application Layer:
 - src/application/__init__.py
 - src/application/sentencize_use_case.py
 - tests/unit/application/__init__.py
 - tests/unit/application/test_sentencize_use_case.py

 Adapter Layer:
 - src/adapters/__init__.py
 - src/adapters/events/__init__.py
 - src/adapters/events/in_memory_event_bus.py
 - src/adapters/tokenizer/__init__.py
 - src/adapters/tokenizer/spacy_tokenizer.py
 - src/adapters/web/__init__.py
 - src/adapters/web/fastapi_adapter.py
 - src/adapters/web/background_server.py
 - tests/unit/adapters/__init__.py
 - tests/unit/adapters/test_in_memory_event_bus.py
 - tests/unit/adapters/test_spacy_tokenizer.py
 - tests/unit/adapters/test_fastapi_adapter.py
 - tests/unit/adapters/test_background_server.py

 Dependencies Required

 Add to pyproject.toml:
 dependencies = [
     "fastapi[standard]>=0.123.0",
     "pydantic>=2.12.5",
     "requests>=2.32.5",
     "uvicorn>=0.38.0",
     "spacy>=3.7.0",  # NEW
 ]

 Install spaCy language model:
 python -m spacy download en_core_web_sm

 Testing Strategy

 1. Unit tests: Test each component in isolation
   - Domain: Pure logic, no mocks
   - Application: Mock domain ports
   - Adapters: Test real implementations
 2. Integration test: tests/unit/config.py validates real dependency wiring
 3. Acceptance test: tests/acceptance/test_serve_sentence.py validates E2E behavior

 Test Execution Order

 # 1. Domain layer (no dependencies)
 pytest tests/unit/domain/ -v

 # 2. Application layer (mocked dependencies)
 pytest tests/unit/application/ -v

 # 3. Adapter layer (real implementations)
 pytest tests/unit/adapters/ -v

 # 4. Integration (composition root)
 pytest tests/unit/config.py -v

 # 5. Acceptance (end-to-end)
 pytest tests/acceptance/ -v

 Key Design Principles

 1. Dependency Inversion: Application depends on domain ports, not concrete adapters
 2. Inside-Out TDD: Build from domain core outward to infrastructure
 3. Red-Green-Refactor: Always write failing test first, then minimal passing code
 4. Hexagonal Architecture: Clear separation between domain, application, and adapters
 5. Event-Driven: Use case publishes domain events for observability
 6. Composition Root: Single place (create_server()) where all dependencies are wired

 Success Criteria

 ✅ All unit tests pass
 ✅ Integration test passes (tests/unit/config.py)
 ✅ Acceptance test passes (tests/acceptance/test_serve_sentence.py)
 ✅ create_server() returns server with:
 - server.app (FastAPI instance)
 - server.app.state.event_bus (InMemoryEventBus)
 - server.start() method (starts uvicorn in background)
 ✅ HTTP GET /sentencize returns {"sentences": [...]}
 ✅ Domain events published: SentencizeRequested → TextTokenized
 ✅ Clean hexagonal architecture with proper dependency flow