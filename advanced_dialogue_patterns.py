#!/usr/bin/env python3
"""
Advanced Peer Dialogue Patterns with PyETR
===========================================

This example demonstrates sophisticated dialogue patterns between reasoning peers:
1. Disagreement and conflict resolution
2. Negotiation and compromise
3. Collaborative decision-making
4. Question-driven inquiry
5. Uncertainty and belief revision

Each pattern showcases different aspects of the Erotetic Theory of Reasoning.
"""

from pyetr import View
from pyetr.inference import default_inference_procedure, default_decision

print("🎭 Advanced Peer Dialogue Patterns with PyETR")
print("=" * 55)

# ============================================================================
# PATTERN 1: Disagreement and Conflict Resolution
# ============================================================================
print("\n\n1. DISAGREEMENT AND CONFLICT RESOLUTION")
print("-" * 45)

print("Scenario: Alice and Bob disagree about whether it will rain")

# Alice believes it will rain
alice_belief = View.from_str("{WillRain()}")
print(f"Alice believes: {alice_belief}")

# Bob believes it won't rain  
bob_belief = View.from_str("{~WillRain()}")
print(f"Bob believes: {bob_belief}")

# They share their conflicting views
print("\nConflict emerges when they share views:")
alice_updated = alice_belief.update(bob_belief, verbose=False)
print(f"Alice after hearing Bob: {alice_updated}")

# The contradiction leads to falsum (empty view)
if alice_updated.is_falsum:
    print("Alice: 'Wait, we can't both be right. Let me reconsider...'")

# Resolution through additional evidence
weather_report = View.from_str("{CloudyCloudy()}")
barometer_reading = View.from_str("{LowPressure()}")
rain_rule = View.from_str("∀x {WillRain()}^{CloudyCloudy()LowPressure()}")

print(f"\nNew evidence arrives:")
print(f"Weather report: {weather_report}")
print(f"Barometer: {barometer_reading}")

# Both peers update with new evidence
alice_resolved = default_inference_procedure([alice_belief, weather_report, barometer_reading, rain_rule])
bob_resolved = default_inference_procedure([bob_belief, weather_report, barometer_reading, rain_rule])

print(f"\nAlice's conclusion: {alice_resolved}")
print(f"Bob's conclusion: {bob_resolved}")
print("Both: 'The evidence suggests it will rain!'")

# ============================================================================
# PATTERN 2: Negotiation and Compromise
# ============================================================================
print("\n\n2. NEGOTIATION AND COMPROMISE")
print("-" * 35)

print("Scenario: Alice and Bob negotiating restaurant choice")

# Alice prefers Italian, Bob prefers Chinese
alice_preference = View.from_str("{0.8=* Prefer(Italian()),0.2=* Prefer(Chinese())}")
bob_preference = View.from_str("{0.2=* Prefer(Italian()),0.8=* Prefer(Chinese())}")

print(f"Alice's preferences: {alice_preference}")
print(f"Bob's preferences: {bob_preference}")

# They consider constraints
budget_constraint = View.from_str("{Expensive(Italian()),Cheap(Chinese())}")
time_constraint = View.from_str("{Close(Italian()),Far(Chinese())}")

print(f"\nConstraints:")
print(f"Budget: {budget_constraint}")
print(f"Distance: {time_constraint}")

# Decision-making process
restaurant_decision = View.from_str("{do(GoTo(Italian())),do(GoTo(Chinese()))}")

# Alice's decision process (considering budget)
alice_decision = default_decision(
    dq=restaurant_decision,
    cv=[budget_constraint],
    pr=[alice_preference]
)

# Bob's decision process (considering time)
bob_decision = default_decision(
    dq=restaurant_decision,
    cv=[time_constraint],
    pr=[bob_preference]
)

print(f"\nAlice's decision: {alice_decision}")
print(f"Bob's decision: {bob_decision}")

# Compromise through weighted combination
compromise_weights = View.from_str("{0.5=* Prefer(Italian()),0.5=* Prefer(Chinese())}")
compromise_decision = default_decision(
    dq=restaurant_decision,
    cv=[budget_constraint, time_constraint],
    pr=[compromise_weights]
)

print(f"Compromise decision: {compromise_decision}")
print("Both: 'Let's find a middle ground!'")

# ============================================================================
# PATTERN 3: Question-Driven Inquiry
# ============================================================================
print("\n\n3. QUESTION-DRIVEN INQUIRY")
print("-" * 30)

print("Scenario: Collaborative investigation")

# Alice has a question about who committed the crime
alice_question = View.from_str("∃x {Committed(Crime(),x*)}")
print(f"Alice's question: {alice_question}")
print("Alice: 'Someone committed the crime, but who?'")

# Bob provides evidence
bob_evidence = View.from_str("{AtScene(John()),HasMotive(John())}")
print(f"\nBob provides evidence: {bob_evidence}")
print("Bob: 'John was at the scene and had a motive.'")

# Alice incorporates the evidence
alice_updated = alice_question.update(bob_evidence, verbose=False)
print(f"Alice's updated view: {alice_updated}")

# They apply a reasoning rule
crime_rule = View.from_str("∀x {Committed(Crime(),x)}^{AtScene(x)HasMotive(x)}")
print(f"\nReasoning rule: {crime_rule}")
print("Both agree: 'If someone was at the scene and had motive, they committed the crime'")

# Collaborative conclusion
conclusion = default_inference_procedure([alice_updated, crime_rule])
print(f"\nConclusion: {conclusion}")
print("Alice: 'So John committed the crime!'")
print("Bob: 'The evidence points to John.'")

# ============================================================================
# PATTERN 4: Uncertainty and Belief Revision
# ============================================================================
print("\n\n4. UNCERTAINTY AND BELIEF REVISION")
print("-" * 35)

print("Scenario: Medical diagnosis with uncertain evidence")

# Doctor Alice has initial hypothesis with uncertainty
alice_diagnosis = View.from_str("{0.7=* HasDisease(Patient(),Flu()),0.3=* HasDisease(Patient(),Cold())}")
print(f"Dr. Alice's initial diagnosis: {alice_diagnosis}")
print("Dr. Alice: 'Probably flu, but could be a cold.'")

# Doctor Bob provides test results
test_results = View.from_str("{HighFever(Patient()),BodyAches(Patient())}")
print(f"\nDr. Bob's test results: {test_results}")
print("Dr. Bob: 'Patient has high fever and body aches.'")

# Diagnostic rules with different weights
flu_rule = View.from_str("∀x {0.9=* HasDisease(x,Flu())}^{HighFever(x)BodyAches(x)}")
cold_rule = View.from_str("∀x {0.1=* HasDisease(x,Cold())}^{HighFever(x)BodyAches(x)}")

print(f"\nDiagnostic rules:")
print(f"Flu rule: {flu_rule}")
print(f"Cold rule: {cold_rule}")

# Belief revision based on new evidence
alice_revised = default_inference_procedure([alice_diagnosis, test_results, flu_rule, cold_rule])
print(f"\nDr. Alice's revised diagnosis: {alice_revised}")
print("Dr. Alice: 'The test results strongly suggest flu.'")

# ============================================================================
# PATTERN 5: Multi-Peer Consensus Building
# ============================================================================
print("\n\n5. MULTI-PEER CONSENSUS BUILDING")
print("-" * 35)

print("Scenario: Committee decision on project funding")

class CommitteeMember:
    def __init__(self, name: str, view: View):
        self.name = name
        self.view = view
    
    def vote(self, proposal: View) -> View:
        return self.view.update(proposal, verbose=False)

# Committee members with different priorities
alice = CommitteeMember("Alice", View.from_str("{0.8=* Important(Innovation()),0.2=* Important(Cost())}"))
bob = CommitteeMember("Bob", View.from_str("{0.3=* Important(Innovation()),0.7=* Important(Cost())}"))
charlie = CommitteeMember("Charlie", View.from_str("{0.6=* Important(Innovation()),0.4=* Important(Cost())}"))

print("Committee members:")
print(f"Alice (innovation-focused): {alice.view}")
print(f"Bob (cost-focused): {bob.view}")
print(f"Charlie (balanced): {charlie.view}")

# Project proposals
proposal_a = View.from_str("{HighInnovation(ProjectA()),HighCost(ProjectA())}")
proposal_b = View.from_str("{LowInnovation(ProjectB()),LowCost(ProjectB())}")

print(f"\nProposals:")
print(f"Project A: {proposal_a}")
print(f"Project B: {proposal_b}")

# Voting process
funding_decision = View.from_str("{do(Fund(ProjectA())),do(Fund(ProjectB()))}")

# Each member makes a decision
alice_vote = default_decision(dq=funding_decision, cv=[proposal_a, proposal_b], pr=[alice.view])
bob_vote = default_decision(dq=funding_decision, cv=[proposal_a, proposal_b], pr=[bob.view])
charlie_vote = default_decision(dq=funding_decision, cv=[proposal_a, proposal_b], pr=[charlie.view])

print(f"\nVotes:")
print(f"Alice votes: {alice_vote}")
print(f"Bob votes: {bob_vote}")
print(f"Charlie votes: {charlie_vote}")

# Consensus building through discussion
print("\nConsensus building:")
print("Alice: 'Project A offers breakthrough innovation!'")
print("Bob: 'But Project B is much more cost-effective.'")
print("Charlie: 'What if we fund Project A but with budget constraints?'")

# Modified proposal with constraints
constrained_proposal = View.from_str("{HighInnovation(ProjectA()),ModerateCost(ProjectA())}")
constraint_rule = View.from_str("∀x {ModerateCost(x)}^{HighInnovation(x)BudgetConstraints()}")

print(f"\nModified proposal: {constrained_proposal}")
print(f"With constraint: {constraint_rule}")

# Re-vote with modified proposal
final_decision = default_decision(
    dq=funding_decision,
    cv=[constrained_proposal, constraint_rule],
    pr=[alice.view, bob.view, charlie.view]  # Combined preferences
)

print(f"\nFinal consensus: {final_decision}")
print("Committee: 'We'll fund Project A with budget oversight!'")

# ============================================================================
# DIALOGUE GENERATION FRAMEWORK
# ============================================================================
print("\n\n6. DIALOGUE GENERATION FRAMEWORK")
print("-" * 35)

class AdvancedDialoguePeer:
    """An advanced reasoning peer with personality and dialogue capabilities."""
    
    def __init__(self, name: str, initial_view: View, personality: dict = None):
        self.name = name
        self.view = initial_view
        self.personality = personality or {}
        self.conversation_history = []
        self.confidence_threshold = personality.get('confidence', 0.5) if personality else 0.5
    
    def express_view(self, context: str = "") -> str:
        """Express current view in natural language."""
        if self.view.is_falsum:
            return f"{self.name}: I'm confused - there seems to be a contradiction."
        elif self.view.is_verum:
            return f"{self.name}: I don't have any specific beliefs about this."
        else:
            return f"{self.name}: {self._view_to_speech(self.view, context)}"
    
    def ask_question(self, about: str) -> str:
        """Ask a question to drive dialogue."""
        return f"{self.name}: I'm wondering about {about}. What do you think?"
    
    def agree_or_disagree(self, other_view: View) -> str:
        """Express agreement or disagreement with another view."""
        combined = self.view.update(other_view, verbose=False)
        
        if combined.is_falsum:
            return f"{self.name}: I disagree - that contradicts what I believe."
        elif combined == self.view:
            return f"{self.name}: I already knew that."
        else:
            return f"{self.name}: That's interesting and changes my perspective."
    
    def propose_compromise(self, issue: str) -> str:
        """Propose a compromise solution."""
        return f"{self.name}: What if we find a middle ground on {issue}?"
    
    def _view_to_speech(self, view: View, context: str = "") -> str:
        """Convert view to natural language with context."""
        view_str = str(view)
        
        # Pattern matching for common dialogue elements
        if "WillRain()" in view_str:
            return "I think it will rain."
        elif "~WillRain()" in view_str:
            return "I don't think it will rain."
        elif "Prefer(" in view_str:
            return "I have preferences about our options."
        elif "do(" in view_str:
            return "I think we should take action."
        elif "*" in view_str:
            return f"I have questions about {context}."
        else:
            return f"My view is: {view_str}"

print("Framework features:")
print("✅ Personality-driven responses")
print("✅ Context-aware dialogue")
print("✅ Conflict detection and resolution")
print("✅ Question generation")
print("✅ Compromise proposals")

# ============================================================================
# SUMMARY AND NEXT STEPS
# ============================================================================
print("\n\n7. SUMMARY AND NEXT STEPS")
print("-" * 30)

print("🎯 Key Dialogue Patterns Demonstrated:")
print("  1. Disagreement → Evidence → Resolution")
print("  2. Negotiation → Constraints → Compromise")
print("  3. Questions → Evidence → Conclusions")
print("  4. Uncertainty → New Data → Belief Revision")
print("  5. Individual Views → Discussion → Consensus")
print()
print("🛠️  Core PyETR Operations for Dialogue:")
print("  • view.update() - Information integration")
print("  • default_inference_procedure() - Collaborative reasoning")
print("  • default_decision() - Group decision-making")
print("  • Weighted states - Uncertainty and preferences")
print("  • Issue structures (*) - Question-driven dialogue")
print("  • Factor operations - Conflict resolution")
print()
print("🚀 Extensions to Explore:")
print("  • Multi-turn conversation management")
print("  • Emotional states through weights")
print("  • Hierarchical dialogue (topics/subtopics)")
print("  • Learning from conversation history")
print("  • Natural language generation improvements")

print("\n" + "=" * 55)
print("🎉 Advanced dialogue patterns complete!")
print("Ready to build sophisticated peer dialogue systems!") 