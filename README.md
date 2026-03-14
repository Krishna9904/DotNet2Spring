# Roslyn2Spring

AI-assisted migration tool that converts **ASP.NET Core Web APIs into Spring Boot services** using **Roslyn static analysis** and **LLM-based code transformation**.

This project demonstrates how compiler-level analysis combined with modern language models can automate backend migration between ecosystems.

---

# Overview

Migrating backend systems from **.NET to Java ecosystems** is a common requirement in large organizations.

However, manual migration is:

- slow
- expensive
- error-prone

Roslyn2Spring automates part of this process by combining **compiler-based analysis** with **LLM-powered transformation**.

The tool:

1. Analyzes .NET Web APIs using **Roslyn**
2. Extracts architecture metadata
3. Captures method signatures and logic
4. Uses an **LLM to translate code**
5. Generates a **Spring Boot project**

---

# Architecture

```
ASP.NET Core Project
        ↓
Roslyn Static Analyzer
        ↓
Architecture Metadata (JSON)
        ↓
Python Migration Engine
        ↓
LLM Code Transformation
        ↓
Spring Boot Project
```

---

# Key Components

## Roslyn Analyzer

The project uses the **Microsoft Roslyn compiler platform** to analyze C# code.

Roslyn provides access to the **C# Abstract Syntax Tree (AST)** and allows the tool to understand the structure of the code.

The analyzer extracts:

- Controllers
- HTTP routes
- HTTP methods
- Method names
- Return types
- Parameters
- Dependency injection
- Services
- Entities
- Method bodies

Example extracted metadata:

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

## Python Migration Engine

The Python pipeline performs the following tasks:

- Executes the Roslyn analyzer
- Extracts architecture JSON
- Constructs LLM prompts
- Generates Java code
- Creates a Spring Boot project structure

Generated project structure:

```
springboot-output
├── pom.xml
├── src/main/java/com/migrator/controller
├── src/main/java/com/migrator/service
├── src/main/java/com/migrator/entity
├── src/main/java/com/migrator/repository
└── src/main/resources/application.properties
```

---

## LLM Code Transformation

The migration engine uses an LLM to translate **C# logic into Java**.

Example:

### ASP.NET Controller

```csharp
[HttpGet]
public string GetUsers()
{
    return _service.GetUsers();
}
```

### Generated Spring Boot Controller

```java
@GetMapping("/api/users")
public String getUsers() {
    return userService.getUsers();
}
```

---

# Technologies Used

- C#
- Roslyn Compiler Platform
- Python
- Groq API
- Spring Boot
- Maven
- Java

---

# Project Structure

```
dotnet-migrator
│
├── RoslynAnalyzer
│   └── Roslyn static analysis engine
│
├── Migrator
│   └── Python migration pipeline
│
├── example-dotnet-project
│   └── Sample ASP.NET Web API
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Setup

## Install Python Dependencies

```
pip install -r requirements.txt
```

---

## Set Groq API Key

Windows:

```
set GROQ_API_KEY=your_api_key_here
```

Linux/macOS:

```
export GROQ_API_KEY=your_api_key_here
```

---

## Run Migration

```
python Migrator/converter.py
```

Generated Spring Boot project will appear in:

```
springboot-output/
```

---

# Example Workflow

1. Provide an ASP.NET Core Web API project
2. Run the migration tool
3. Roslyn analyzes the code
4. Metadata is generated
5. LLM converts logic
6. Spring Boot project is generated

---

# Current Capabilities

The prototype supports migration of:

- ASP.NET Controllers
- Routes
- HTTP methods
- Dependency injection
- Service classes
- Entity classes
- Basic method logic

---

# Limitations

This prototype currently focuses on **API migration** and does not yet support:

- LINQ query translation
- Async/await mapping
- DTO transformation
- Authentication middleware
- Complex Entity Framework mappings
- Advanced dependency graphs

---

# Future Improvements

Potential future improvements include:

- Roslyn SemanticModel analysis
- LINQ → JPA query conversion
- Async method migration
- DTO generation
- Authentication middleware migration
- Dependency graph based conversion
- Full enterprise project migration

---

# Why Roslyn?

Roslyn provides **compiler-level access to C# code**, enabling the tool to understand:

- syntax trees
- type systems
- attributes
- dependency injection patterns

This allows the migration engine to extract **meaningful architecture information**, not just raw text.

---

# License

MIT License

---

# Author


Krishna

Software Engineer | Data Engineer | AI & LLM Developer 

