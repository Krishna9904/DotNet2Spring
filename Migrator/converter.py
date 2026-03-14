import subprocess
import json
import requests
import os

# =====================================
# PROJECT ROOT
# =====================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROSLYN_PROJECT = os.path.join(PROJECT_ROOT, "RoslynAnalyzer", "RoslynAnalyzer.csproj")

BASE_DIR = os.path.join(PROJECT_ROOT, "springboot-output")

# =====================================
# API KEY FROM ENV
# =====================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("Please set GROQ_API_KEY environment variable")

# =====================================
# CREATE SPRING BOOT STRUCTURE
# =====================================

def create_project_structure():

    folders = [
        "src/main/java/com/migrator/controller",
        "src/main/java/com/migrator/service",
        "src/main/java/com/migrator/repository",
        "src/main/java/com/migrator/entity",
        "src/main/resources"
    ]

    for folder in folders:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

create_project_structure()

# =====================================
# GENERATE POM
# =====================================

def generate_pom():

    pom = """
<project xmlns="http://maven.apache.org/POM/4.0.0">
<modelVersion>4.0.0</modelVersion>

<groupId>com.migrator</groupId>
<artifactId>migrated-app</artifactId>
<version>1.0.0</version>

<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>3.2.0</version>
</parent>

<dependencies>

<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
<groupId>com.h2database</groupId>
<artifactId>h2</artifactId>
</dependency>

</dependencies>

</project>
"""

    with open(os.path.join(BASE_DIR, "pom.xml"), "w") as f:
        f.write(pom)

generate_pom()

# =====================================
# PROPERTIES
# =====================================

def generate_properties():

    props = """
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
"""

    path = os.path.join(BASE_DIR, "src/main/resources/application.properties")

    with open(path, "w") as f:
        f.write(props)

generate_properties()

# =====================================
# CALL GROQ
# =====================================

def call_llm(prompt):

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]

# =====================================
# RUN ROSLYN ANALYZER
# =====================================

process = subprocess.run(
    ["dotnet", "run", "--project", ROSLYN_PROJECT],
    capture_output=True,
    text=True
)

output = process.stdout

json_start = output.find("{")

if json_start == -1:
    raise Exception("Roslyn analyzer did not return JSON:\n" + output)

json_data = output[json_start:]

data = json.loads(json_data)

controllers = data["controllers"]
services = data["services"]
entities = data["entities"]

# =====================================
# FILE WRITER
# =====================================

def write_file(path, content):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)

# =====================================
# CONTROLLERS
# =====================================

def generate_controller(controller):

    prompt = f"""
Convert this ASP.NET controller method into Spring Boot.

Controller: {controller['controller']}
Route: {controller['route']}
HTTP Method: {controller['http']}
Method Name: {controller['action']}
Return Type: {controller['returnType']}
Parameters: {controller['parameters']}
Dependencies: {controller['dependencies']}

C# Method Body:
{controller['body']}

Return ONLY valid Java Spring Boot code.
"""

    return call_llm(prompt)

for controller in controllers:

    java_code = generate_controller(controller)

    path = os.path.join(BASE_DIR, "src/main/java/com/migrator/controller", controller["controller"] + ".java")

    write_file(path, java_code)

# =====================================
# SERVICES
# =====================================

def generate_service(service):

    prompt = f"""
Generate Spring Boot service class.

Service name: {service}

Return ONLY Java code.
"""

    return call_llm(prompt)

for service in services:

    java_code = generate_service(service)

    path = os.path.join(BASE_DIR, "src/main/java/com/migrator/service", service + ".java")

    write_file(path, java_code)

# =====================================
# ENTITIES
# =====================================

def generate_entity(entity):

    prompt = f"""
Convert C# model into Spring Boot JPA entity.

Entity: {entity}

Return ONLY Java code.
"""

    return call_llm(prompt)

# =====================================
# REPOSITORIES
# =====================================

def generate_repository(entity):

    code = f"""
package com.migrator.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.migrator.entity.{entity};

public interface {entity}Repository extends JpaRepository<{entity}, Long> {{

}}
"""

    path = os.path.join(BASE_DIR, "src/main/java/com/migrator/repository", entity + "Repository.java")

    write_file(path, code)

for entity in entities:

    java_code = generate_entity(entity)

    path = os.path.join(BASE_DIR, "src/main/java/com/migrator/entity", entity + ".java")

    write_file(path, java_code)

    generate_repository(entity)

print("Spring Boot project generated successfully.")
