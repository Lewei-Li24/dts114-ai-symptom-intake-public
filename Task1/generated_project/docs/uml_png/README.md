# UML PNG Exports

Render the PlantUML source files in the parent folder to create:

- `use_case.png`
- `class_diagram.png`
- `activity_diagram.png`

The `.puml` source files are included so the diagrams remain reproducible. If PlantUML is installed, run:

```bash
plantuml -tpng docs/*.puml -o uml_png
```
