# NB_TEMPLATE

## Purpose

NB_TEMPLATE is the Reading Point compiler.

It transforms a Reading Point specification into a complete engineering notebook bundle.

---

## Inputs

```
RP_TEMPLATE.yaml
```

describing:

- Reading Point identity
- Engineering objective
- Engineering dialogue
- Repository grammar
- Engineering statements
- Forward context

---

## Compiler

```
NB_TEMPLATE.ipynb
```

The compiler:

- validates the Reading Point specification;
- renders engineering dialogue figures;
- generates accessibility text;
- produces notebook records;
- packages the notebook bundle.

---

## Generated Bundle

```
PNG
ALT TEXT
README
METADATA
MANIFEST
ZIP
```

---

## Repository Architecture

```
Reading Order
        ↓
Engineering Statements
        ↓
Reading Point Specification
        ↓
NB_TEMPLATE
        ↓
Notebook Bundle
```

---

## Reading Point Workflow

```
specifications/RP_11_A.yaml
            ↓
RP_TEMPLATE.yaml
            ↓
Run NB_TEMPLATE.ipynb
            ↓
NB_11_A bundle
```

The same workflow applies to every Reading Point.

---

## Compiler Responsibilities

NB_TEMPLATE:

- validates specifications;
- derives notebook identities;
- derives artifact identities;
- renders engineering dialogue;
- records notebook metadata;
- records notebook manifests;
- packages release artifacts.

---

## Renderer

```
dialogue_renderer.py
```

The renderer knows only engineering dialogue.

It does not know repository identities or Reading Point numbers.

---

## Specification

```
RP_TEMPLATE.yaml
```

The specification describes engineering semantics.

The compiler derives filenames, notebook identities, artifact identities, and release records.

---

## Version

Current compiler:

```
NB_TEMPLATE v1.1.0
```

Architecture:

```
Reading Point Compiler
```

---

*Admissible generalizations trail leading specifications.*
