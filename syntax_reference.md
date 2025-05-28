# PyETR Syntax Quick Reference

## Basic View Construction

```python
from pyetr import View

# Simple fact
view = View.from_str("{Rain()}")

# Multiple possibilities (OR)
view = View.from_str("{Sunny(),Rainy(),Cloudy()}")

# Conjunction (AND)
view = View.from_str("{Hot()Humid()}")

# Complex combinations
view = View.from_str("{Hot()Sunny(),Cold()Rainy()}")
# Means: (Hot AND Sunny) OR (Cold AND Rainy)
```

## Logical Operators

| Syntax | Meaning | Example |
|--------|---------|---------|
| `A()` | Predicate A | `{Happy()}` |
| `~A()` | NOT A | `{~Raining()}` |
| `A()B()` | A AND B | `{Hot()Sunny()}` |
| `A(),B()` | A OR B | `{Hot(),Cold()}` |
| `{A()}^{B()}` | A given B (conditional) | `{Wet()}^{Rain()}` |

## Quantifiers & Variables

```python
# Universal quantifier (for all x)
view = View.from_str("∀x {Human(x)Mortal(x)}^{Human(x)}")
# Alternative syntax
view = View.from_str("Ax {Human(x)Mortal(x)}^{Human(x)}")

# Existential quantifier (there exists x)  
view = View.from_str("∃x {Student(x)}")
# Alternative syntax
view = View.from_str("Ex {Student(x)}")

# Multiple quantifiers
view = View.from_str("∀x ∃y {Teaches(x,y)}")
```

## Issue Markers (Questioning)

```python
# Mark what's "at issue" (being questioned) with *
view = View.from_str("∀x {Student(x*)}")  # Questioning if x is a student
view = View.from_str("∀x {Mortal(x)}^{Human(x*)}")  # Questioning if x is human
```

## Weights (Advanced)

```python
# Multiplicative weight (confidence level)
view = View.from_str("{0.8=* Rain()}")

# Additive weight  
view = View.from_str("{5=+ Happy()}")

# Both weights
view = View.from_str("{0.9=* 3=+ Sunny()}")
```

## Decision Making

```python
from pyetr.inference import default_decision

# Decision question
dq = View.from_str("{do(Buy(Book())),~do(Buy(Book()))}")

# Conditional value
cv = View.from_str("∀x {Value()}^{do(Buy(x))Useful(x)}")

# Prior belief
pr = View.from_str("{Useful(Book())}")

# Make decision
decision = default_decision(dq=dq, cv=[cv], pr=[pr])
```

## Common Inference Patterns

```python
from pyetr.inference import default_inference_procedure

# Simple modus ponens
premise1 = View.from_str("{Mortal(Socrates())}^{Human(Socrates())}")
premise2 = View.from_str("{Human(Socrates())}")
conclusion = default_inference_procedure([premise1, premise2])

# Universal instantiation
rule = View.from_str("∀x {Mortal(x)}^{Human(x)}")
fact = View.from_str("{Human(Socrates())}")
conclusion = default_inference_procedure([rule, fact])
```

## View Operations

```python
# Update (combine information)
v1 = View.from_str("{A()}")
v2 = View.from_str("{B()}")
combined = v1.update(v2)

# Factor (simplify)
simplified = view.factor()

# Answer (resolve issues)
resolved = view.answer()

# Merge (external update)
merged = view.merge(other_view)
```

## Common Patterns

### Creating Facts
```python
fact = View.from_str("{Cat(Fluffy())}")
fact = View.from_str("{Tall(John())Smart(John())}")  # John is tall AND smart
```

### Creating Rules
```python
rule = View.from_str("∀x {Animal(x)}^{Cat(x)}")  # All cats are animals
rule = View.from_str("∀x {Wet()}^{Rain()}")      # If it rains, things get wet
```

### Disjunctions (OR)
```python
either_or = View.from_str("{Sunny(),Rainy()}")   # Either sunny OR rainy
multiple = View.from_str("{A(),B(),C()}")        # A OR B OR C
```

### Complex Statements
```python
# Either (hot and sunny) or (cold and rainy)
weather = View.from_str("{Hot()Sunny(),Cold()Rainy()}")

# If human, then mortal
mortality = View.from_str("∀x {Mortal(x)}^{Human(x)}")

# There exists someone who is both tall and smart
someone = View.from_str("∃x {Tall(x)Smart(x)}")
```

## Predefined Examples

```python
from pyetr.cases import e17, e56_default_inference

# Example 17: Card reasoning
print(e17.v)  # View the premises
print(e17.c)  # View the conclusion
e17.test()    # Run the reasoning

# Example 56: Student-professor reasoning
print(e56_default_inference.v)
e56_default_inference.test()
```

## Debugging Tips

```python
# Different ways to inspect a view
view = View.from_str("{A()}")

print(view)           # Default string representation
print(view.to_str())  # Same as above
print(view.base)      # More detailed base representation
print(view.detailed)  # Full internal structure
```

## Common Errors to Avoid

1. **Missing quantifiers**: `{Student(x)}` → Should be `∀x {Student(x)}`
2. **Wrong asterisk placement**: `{A()*}` → Should be `{A(x*)}` with variable
3. **Mismatched parentheses**: `{A(}` → Should be `{A()}`
4. **Forgotten commas in OR**: `{A()B(),C()}` vs `{A(),B(),C()}`

## Next Steps

- Run `python3 getting_started.py` for a hands-on introduction
- Run `python3 tutorial.py` for comprehensive examples  
- Explore `examples/` directory for more cases
- Read docs at: https://oxford-hai-lab.github.io/PyETR 