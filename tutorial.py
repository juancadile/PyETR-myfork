#!/usr/bin/env python3
"""
PyETR Tutorial: Understanding the Erotetic Theory of Reasoning

This tutorial demonstrates how to use PyETR, which implements the Erotetic Theory 
of Reasoning from the book "Reason & Inquiry" (OUP 2023).

The core idea: reasoning aims at resolving "issues" (questions), and rational 
thinking emerges when we maintain sufficient inquisitiveness in our reasoning process.
"""

from pyetr import View
from pyetr.inference import default_inference_procedure, default_decision
from pyetr.cases import e17

print("=" * 60)
print("PyETR Tutorial: Erotetic Theory of Reasoning")
print("=" * 60)

# ============================================================================
# PART 1: Understanding Views
# ============================================================================
print("\n1. UNDERSTANDING VIEWS")
print("-" * 30)

# Views are the central objects in ETR - they represent both information and 
# the "issues" (questions) that drive reasoning

# Example from the book (Example 17): Card reasoning
print("Example 17 from the book - Card reasoning:")
print("P1: There's a king and no ace, OR there's an ace and no king")
print("P2: There is a king")
print("Conclusion: There is no ace")

# Create views using string notation
p1 = View.from_str("{~King()Ace(),King()~Ace()}")  # P1: (~King ∧ Ace) ∨ (King ∧ ~Ace)
p2 = View.from_str("{King()}")                      # P2: King

print(f"\nP1 as view: {p1}")
print(f"P2 as view: {p2}")

# The * symbol indicates what's "at issue" (what we're questioning)
# It works with arbitrary objects (variables), not function terms
print("\nExample with issue markers (asterisks):")
student_with_issue = View.from_str("∀z {Student(z*)}")
print(f"Student view with z at issue: {student_with_issue}")
print("This means we're questioning whether z is a Student")

# ============================================================================
# PART 2: Basic Inference
# ============================================================================
print("\n\n2. BASIC INFERENCE")
print("-" * 30)

# Use the default inference procedure to draw conclusions
conclusion = default_inference_procedure((p1, p2))
print(f"Conclusion from P1 + P2: {conclusion}")

# This gives us {~Ace()} - there is no ace!
print("Explanation: Since there's a king (P2), and we know from P1 that")
print("we can't have both king and ace, we conclude there's no ace.")

# ============================================================================
# PART 3: Working with Predefined Cases
# ============================================================================
print("\n\n3. PREDEFINED CASES")
print("-" * 30)

# PyETR includes many examples from the book
print("Using predefined case e17 (same as above):")
print(f"Views: {e17.v}")
print(f"Expected conclusion: {e17.c}")

# Test the case to see the reasoning steps
print("\nTesting the case (with verbose output):")
e17.test(verbose=True)

# ============================================================================
# PART 4: More Complex Examples
# ============================================================================
print("\n\n4. MORE COMPLEX EXAMPLES")
print("-" * 30)

# Example with quantifiers and dependencies
print("Example with universal and existential quantifiers:")
student_view = View.from_str("∀z ∃w {Student(z*)Reads(z,w)Book(w)}^{Student(z*)}")
print(f"View: {student_view}")
print("This says: For all z, if z is a student (and we're questioning this),")
print("then there exists some w such that z reads w and w is a book")

# Example with functions and terms
print("\nExample with functions:")
socrates_view = View.from_str("{Man(Socrates()*)}")
mortality_rule = View.from_str("Ax {Mortal(x)}^{Man(x*)}")
print(f"Premise: {socrates_view}")
print(f"Rule: {mortality_rule}")

conclusion2 = default_inference_procedure([socrates_view, mortality_rule])
print(f"Conclusion: {conclusion2}")
print("Since Socrates is a man, and all men are mortal, Socrates is mortal.")

# ============================================================================
# PART 5: Decision Making
# ============================================================================
print("\n\n5. DECISION MAKING")
print("-" * 30)

# ETR can also handle decision problems
print("Decision example: Should I buy a video?")

# Decision question: buy video or not?
decision_question = View.from_str("{do(Buy(Video()*)),~do(Buy(Video()))}")

# Conditional value: buying things that are fun has value
conditional_value = View.from_str("Ax {Fun()}^{do(Buy(x*))}")

# Prior belief: videos are fun
prior = View.from_str("{1=+ 0} ^ {Fun()}")

print(f"Decision question: {decision_question}")
print(f"Value condition: {conditional_value}")
print(f"Prior belief: {prior}")

decision = default_decision(dq=decision_question, cv=[conditional_value], pr=[prior])
print(f"Decision: {decision}")
print("Since videos are fun, and buying fun things has value, buy the video!")

# ============================================================================
# PART 6: Understanding the Syntax
# ============================================================================
print("\n\n6. UNDERSTANDING THE SYNTAX")
print("-" * 30)

print("Key syntax elements:")
print("• {A,B,C} - stage (disjunction: A OR B OR C)")
print("• {A B C} - state (conjunction: A AND B AND C)")  
print("• ~ - negation (NOT)")
print("• * - marks what's 'at issue' (being questioned)")
print("• ^{...} - supposition (conditional context)")
print("• ∀x, ∃x - universal/existential quantifiers")
print("• Ax - universal quantifier over x")
print("• do(...) - action/decision")
print("• =+ - additive weight")
print("• =* - multiplicative weight")

# ============================================================================
# PART 7: Key Operations
# ============================================================================
print("\n\n7. KEY VIEW OPERATIONS")
print("-" * 30)

# Update operation - central to ETR reasoning
v1 = View.from_str("{Man(Socrates()*)}")
v2 = View.from_str("Ax {Mortal(x)}^{Man(x*)}")
updated = v1.update(v2)
print(f"v1.update(v2): {updated}")
print("Update combines information while preserving issues")

# Other useful operations
print(f"\nOther operations available:")
print(f"• factor() - removes redundant information")
print(f"• answer() - resolves issues")
print(f"• merge() - combines with external information")
print(f"• depose() - removes questioning")

# ============================================================================
# PART 8: Next Steps
# ============================================================================
print("\n\n8. NEXT STEPS")
print("-" * 30)

print("To learn more about PyETR:")
print("1. Explore the examples/ directory for more cases")
print("2. Read the documentation at: https://oxford-hai-lab.github.io/PyETR")
print("3. Check out pyetr.cases for predefined examples from the book")
print("4. Experiment with different view constructions")
print("5. Try the advanced inference procedures")

print("\nKey modules to explore:")
print("• pyetr.View - core view construction and manipulation")
print("• pyetr.inference - inference procedures") 
print("• pyetr.cases - examples from Reason & Inquiry")
print("• pyetr.atoms - building blocks (predicates, terms, etc.)")

print("\n" + "=" * 60)
print("End of Tutorial")
print("=" * 60) 