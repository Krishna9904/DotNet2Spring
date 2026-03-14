# DotNet2Spring

DotNet2Spring is a prototype tool that converts **ASP.NET Core Web APIs into Spring Boot services** using **Roslyn static analysis** and **LLM-based code transformation**.

The project explores how **compiler-level code analysis** combined with **large language models** can automate backend migration between ecosystems such as:

.NET → Java (Spring Boot)

---

## Why this project?

Migrating APIs between platforms is common in many organizations. Rewriting services manually can be time consuming and error-prone.

DotNet2Spring explores a workflow where:

1. A .NET project is analyzed using Roslyn.
2. Architecture metadata is extracted from the source code.
3. Method logic and structure are captured.
4. An LLM translates the logic into Java.
5. A Spring Boot project is generated automatically.

---

## How it works

```
ASP.NET Core Project
        ↓
Roslyn Analyzer
        ↓
Architecture Metadata (JSON)
        ↓
Python Migration Pipeline
        ↓
LLM Code Conversion
        ↓
Spring Boot Project
```

---

## What the analyzer extracts

Using the Roslyn compiler platform, the analyzer detects:

- Controllers
- HTTP routes
- HTTP methods (GET, POST)
- Method names
- Return types
- Parameters
- Dependency injection
- Services
- Entities
- Method bodies

Example metadata produced by the analyzer:

```json
{
  "controller": "UserController",
  "route": "api/users",
  "http": "GET",
  "action": "GetUsers",
  "returnType": "string",
  "parameters": [],
  "dependencies": ["UserService"],
  "body": "{ return _service.GetUsers(); }"
}
```

---

## Project structure

```
dotnet-migrator
│
├── RoslynAnalyzer
│   Roslyn-based C# analyzer
│
├── Migrator
│   Python migration pipeline
│
├── example-dotnet-project
│   Sample ASP.NET Web API used for testing
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Setup

Install Python dependencies:

```
pip install -r requirements.txt
```

Set your Groq API key.

Windows:

```
set GROQ_API_KEY=your_api_key_here
```

Linux / macOS:

```
export GROQ_API_KEY=your_api_key_here
```

---

## Run the migration

```
python Migrator/converter.py
```

The generated Spring Boot project will appear in:

```
springboot-output/
```

---

## Example

ASP.NET controller:

```csharp
[HttpGet]
public string GetUsers()
{
    return _service.GetUsers();
}
```

Generated Spring Boot controller:

```java
@GetMapping("/api/users")
public String getUsers() {
    return userService.getUsers();
}
```

---

## Technologies used

- C#
- Roslyn Compiler Platform
- Python
- Groq API
- Spring Boot
- Java
- Maven

---

## Author

Krishna

Software Engineer focused on backend systems, AI applications, and developer tooling.
