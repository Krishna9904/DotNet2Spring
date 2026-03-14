using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Text.Json;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

class Program
{
    static void Main()
    {
        // Example project relative to repo root
        string folderPath = Path.Combine(Directory.GetCurrentDirectory(), "..", "example-dotnet-project");

        var files = Directory.GetFiles(folderPath, "*.cs", SearchOption.AllDirectories)
            .Where(f => !f.Contains(@"\bin\") && !f.Contains(@"\obj\"));

        var controllers = new List<object>();
        var services = new List<string>();
        var entities = new List<string>();

        foreach (var file in files)
        {
            var code = File.ReadAllText(file);

            var tree = CSharpSyntaxTree.ParseText(code);
            var root = tree.GetRoot();

            var classes = root.DescendantNodes()
                .OfType<ClassDeclarationSyntax>();

            foreach (var cls in classes)
            {
                string className = cls.Identifier.Text;
                string baseClass = cls.BaseList?.Types.FirstOrDefault()?.ToString();

                if (baseClass == "ControllerBase" || baseClass == "Controller")
                {
                    string route = "";

                    var dependencies = new List<string>();

                    var attributes = cls.AttributeLists
                        .SelectMany(a => a.Attributes);

                    foreach (var attr in attributes)
                    {
                        if (attr.Name.ToString() == "Route")
                        {
                            route = attr.ArgumentList?.Arguments.First().ToString().Replace("\"", "");
                        }
                    }

                    var constructors = cls.Members.OfType<ConstructorDeclarationSyntax>();

                    foreach (var constructor in constructors)
                    {
                        foreach (var param in constructor.ParameterList.Parameters)
                        {
                            dependencies.Add(param.Type.ToString());
                        }
                    }

                    var methods = cls.Members.OfType<MethodDeclarationSyntax>();

                    foreach (var method in methods)
                    {
                        var methodAttributes = method.AttributeLists
                            .SelectMany(a => a.Attributes);

                        foreach (var attr in methodAttributes)
                        {
                            string httpMethod = "";

                            if (attr.Name.ToString().Contains("HttpGet"))
                                httpMethod = "GET";

                            if (attr.Name.ToString().Contains("HttpPost"))
                                httpMethod = "POST";

                            if (httpMethod != "")
                            {
                                string body = method.Body?.ToString();
                                string returnType = method.ReturnType.ToString();

                                var parameters = method.ParameterList.Parameters
                                    .Select(p => new
                                    {
                                        name = p.Identifier.Text,
                                        type = p.Type?.ToString()
                                    });

                                controllers.Add(new
                                {
                                    controller = className,
                                    route = route,
                                    action = method.Identifier.Text,
                                    http = httpMethod,
                                    returnType = returnType,
                                    parameters = parameters,
                                    dependencies = dependencies,
                                    body = body
                                });
                            }
                        }
                    }
                }

                else if (className.EndsWith("Service"))
                {
                    services.Add(className);
                }

                else if (cls.Members.OfType<PropertyDeclarationSyntax>().Any())
                {
                    entities.Add(className);
                }
            }
        }

        var result = new
        {
            controllers,
            services,
            entities
        };

        var json = JsonSerializer.Serialize(result, new JsonSerializerOptions
        {
            WriteIndented = true
        });

        Console.WriteLine(json);
    }
}
