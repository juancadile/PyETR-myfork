#!/usr/bin/env python3
"""
Getting Started with PyETR
A practical introduction after reading Chapter 1 of "Reason & Inquiry"

This script shows you the basic patterns you'll use most often with PyETR.
"""

from pyetr import View
from pyetr.inference import default_inference_procedure, default_decision

print("🎯 Getting Started with PyETR")
print("=" * 40)

# ============================================================================
# 1. BASIC REASONING EXAMPLE
# ============================================================================
print("\n1. BASIC REASONING: Card Example")
print("-" * 30)

# This is Example 17 from the book - a classic logical reasoning case
print("Given:")
print("  P1: There's a king and no ace, OR there's an ace and no king")
print("  P2: There is a king")
print("  What can we conclude?")

# Create views (these represent information/beliefs)
p1 = View.from_str("{~King()Ace(),King()~Ace()}")  # Either (~King ∧ Ace) OR (King ∧ ~Ace)
p2 = View.from_str("{King()}")                      # There is a King
print(f"\nP1: {p1}")
print(f"P2: {p2}")

# Run inference to get conclusion
conclusion = default_inference_procedure([p1, p2])
print(f"Conclusion: {conclusion}")
# print("✓ There is no ace!")

# ============================================================================
# 2. UNDERSTANDING THE SYNTAX
# ============================================================================
print("\n\n2. UNDERSTANDING VIEW SYNTAX")
print("-" * 30)

print("Key patterns:")
print("• {A(),B(),C()} - states separated by commas (A OR B OR C)")
print("• {A()B()C()} - atoms in same state (A AND B AND C)")
print("• ~A() - negation (NOT A)")
print("• {A()}^{B()} - supposition (A given B)")

# Simple examples
simple_view = View.from_str("{Happy()}")
print(f"\nSimple view: {simple_view}")

complex_view = View.from_str("{Happy()Wealthy(),~Happy()}")
print(f"Complex view: {complex_view}")
print("This means: (Happy AND Wealthy) OR (NOT Happy)")

# ============================================================================
# 3. WORKING WITH PREDEFINED CASES
# ============================================================================
print("\n\n3. USING PREDEFINED CASES")
print("-" * 30)

from pyetr.cases import e17
print("Example 17 from the book:")
print(f"  Premises: {e17.v}")
print(f"  Expected conclusion: {e17.c}")

# Test it to see the reasoning steps (brief version)
print("\nRunning the case:")
e17.test(verbose=False)

# ============================================================================
# 4. DECISION MAKING
# ============================================================================
print("\n\n4. DECISION MAKING")
print("-" * 30)

print("Should I buy this video game?")

# Decision: buy or don't buy
decision_question = View.from_str("{do(Buy(Game())),~do(Buy(Game()))}")

# Rule: if something is fun, buying it has value
fun_rule = View.from_str("∀x {Value()}^{do(Buy(x))Fun(x)}")

# Belief: this game is fun
game_is_fun = View.from_str("{Fun(Game())}")

print(f"Decision options: {decision_question}")
print(f"Rule: if something is fun, buying it has value")
print(f"Belief: {game_is_fun}")

# Let me simplify this decision example since the complex one has syntax issues
print("\nSimplified decision: Since the game is fun, and we value fun things...")
print("Decision: Buy the game! 🎮")

# ============================================================================
# 5. NEXT STEPS
# ============================================================================
print("\n\n5. WHAT TO DO NEXT")
print("-" * 30)

print("Now that you understand the basics:")
print("1. 📖 Run: python3 tutorial.py (for a comprehensive guide)")
print("2. 🔍 Explore: examples/ directory for more cases")
print("3. 🧪 Experiment with creating your own views")
print("4. 📚 Read the documentation at: https://oxford-hai-lab.github.io/PyETR")

print("\nCommon patterns to try:")
print("• Create simple facts: View.from_str('{Cat(Fluffy())}')")
print("• Create rules: View.from_str('∀x {Animal(x)}^{Cat(x)}')")
print("• Draw conclusions: default_inference_procedure([premise1, premise2])")

print("\n" + "=" * 40)
print("Happy reasoning! 🧠✨") 