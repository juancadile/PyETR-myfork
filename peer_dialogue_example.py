#!/usr/bin/env python3
"""
Peer Dialogue Generation with PyETR
====================================

This example demonstrates how to use PyETR to model and generate dialogue 
between two reasoning peers using the Erotetic Theory of Reasoning.

The key insight is that dialogue emerges from:
1. Each peer having their own view (beliefs + questions)
2. Peers sharing information through view operations
3. Questions driving the conversation forward
4. Reasoning operations updating beliefs

We'll model a conversation between Alice and Bob about a shared scenario.
"""

from pyetr import View
from pyetr.inference import default_inference_procedure

print("🗣️  Peer Dialogue Generation with PyETR")
print("=" * 50)

# ============================================================================
# SCENARIO: Alice and Bob discussing a mystery at a party
# ============================================================================
print("\n📖 SCENARIO:")
print("Alice and Bob are at a party trying to figure out who ate the last cookie.")
print("They each have different information and questions.")

# ============================================================================
# PART 1: Initial Peer States
# ============================================================================
print("\n\n1. INITIAL PEER STATES")
print("-" * 30)

# Alice's initial view: She knows John was in the kitchen, but questions if he ate the cookie
alice_view = View.from_str("∀x {InKitchen(John())AteLastCookie(x*)}^{InKitchen(John())}")
print(f"Alice's view: {alice_view}")
print("Alice thinks: 'John was in the kitchen. Did someone eat the last cookie?'")

# Bob's initial view: He knows someone ate the cookie, but questions who
bob_view = View.from_str("∃x {AteLastCookie(x*)}")
print(f"\nBob's view: {bob_view}")
print("Bob thinks: 'Someone definitely ate the last cookie, but who?'")

# ============================================================================
# PART 2: Information Sharing - Alice tells Bob about John
# ============================================================================
print("\n\n2. ALICE SHARES INFORMATION")
print("-" * 30)

# Alice shares her information about John being in the kitchen
alice_shares = View.from_str("{InKitchen(John())}")
print(f"Alice tells Bob: {alice_shares}")
print("Alice: 'I saw John in the kitchen earlier.'")

# Bob updates his view with Alice's information
bob_updated = bob_view.update(alice_shares, verbose=False)
print(f"\nBob's updated view: {bob_updated}")
print("Bob now thinks: 'Someone ate the cookie, and John was in the kitchen...'")

# ============================================================================
# PART 3: Bob Shares New Information
# ============================================================================
print("\n\n3. BOB SHARES INFORMATION")
print("-" * 30)

# Bob remembers seeing crumbs on John's shirt
bob_shares = View.from_str("{CrumbsOnShirt(John())}")
print(f"Bob tells Alice: {bob_shares}")
print("Bob: 'Wait, I remember seeing crumbs on John's shirt!'")

# Alice updates her view with Bob's information
alice_updated = alice_view.update(bob_shares, verbose=False)
print(f"\nAlice's updated view: {alice_updated}")

# ============================================================================
# PART 4: Collaborative Reasoning
# ============================================================================
print("\n\n4. COLLABORATIVE REASONING")
print("-" * 30)

# They combine their evidence with a general rule about cookie eating
# FIXED: Use specific rule about John rather than universal quantification
evidence_rule = View.from_str("{AteLastCookie(John())}^{InKitchen(John())CrumbsOnShirt(John())}")
print(f"Shared reasoning rule: {evidence_rule}")
print("Both agree: 'If John was in the kitchen AND has crumbs, then John ate the cookie'")

# Alice applies the reasoning
alice_conclusion = default_inference_procedure([alice_updated, evidence_rule])
print(f"\nAlice's conclusion: {alice_conclusion}")
print("Alice: 'Based on the evidence, John ate the last cookie!'")

# Bob applies the same reasoning
bob_conclusion = default_inference_procedure([bob_updated, evidence_rule])
print(f"Bob's conclusion: {bob_conclusion}")
print("Bob: 'I agree! John must have eaten it.'")

# Let's also show what happens with just the facts and rule
print(f"\nDemonstrating the reasoning:")
facts = View.from_str("{InKitchen(John())CrumbsOnShirt(John())}")
simple_conclusion = default_inference_procedure([facts, evidence_rule])
print(f"Facts: {facts}")
print(f"Rule: {evidence_rule}")
print(f"Conclusion: {simple_conclusion}")
print("✓ This correctly concludes that John ate the cookie!")

# ============================================================================
# PART 5: Dialogue Generation Framework
# ============================================================================
print("\n\n5. DIALOGUE GENERATION FRAMEWORK")
print("-" * 30)

class DialoguePeer:
    """A reasoning peer in a dialogue system."""
    
    def __init__(self, name: str, initial_view: View):
        self.name = name
        self.view = initial_view
        self.conversation_history = []
    
    def share_information(self, info: View) -> str:
        """Share information with other peers."""
        self.conversation_history.append(f"SHARED: {info}")
        return f"{self.name}: {self._view_to_speech(info)}"
    
    def receive_information(self, info: View, from_peer: str) -> str:
        """Receive and process information from another peer."""
        old_view = self.view
        self.view = self.view.update(info, verbose=False)
        self.conversation_history.append(f"RECEIVED from {from_peer}: {info}")
        
        if self.view != old_view:
            return f"{self.name}: Interesting! That changes my thinking."
        else:
            return f"{self.name}: That's consistent with what I already knew."
    
    def reason_about(self, rule: View) -> View:
        """Apply reasoning with a given rule."""
        conclusion = default_inference_procedure([self.view, rule])
        self.conversation_history.append(f"REASONED: {rule} -> {conclusion}")
        return conclusion
    
    def _view_to_speech(self, view: View) -> str:
        """Convert a view to natural language (simplified)."""
        view_str = str(view)
        # Simple pattern matching for demo purposes
        if "InKitchen(John())" in view_str:
            return "I saw John in the kitchen."
        elif "CrumbsOnShirt(John())" in view_str:
            return "John had crumbs on his shirt."
        elif "AteLastCookie(John())" in view_str:
            return "John ate the last cookie!"
        else:
            return f"I believe: {view_str}"

# ============================================================================
# PART 6: Simulated Dialogue
# ============================================================================
print("\n\n6. SIMULATED DIALOGUE")
print("-" * 30)

# Create the peers
alice = DialoguePeer("Alice", View.from_str("{InKitchen(John())}"))
bob = DialoguePeer("Bob", View.from_str("∃x {AteLastCookie(x*)}"))

print("🎭 DIALOGUE SIMULATION:")
print()

# Turn 1: Alice shares
print("Turn 1:")
print(alice.share_information(View.from_str("{InKitchen(John())}")))
print(bob.receive_information(View.from_str("{InKitchen(John())}"), "Alice"))
print()

# Turn 2: Bob shares
print("Turn 2:")
print(bob.share_information(View.from_str("{CrumbsOnShirt(John())}")))
print(alice.receive_information(View.from_str("{CrumbsOnShirt(John())}"), "Bob"))
print()

# Turn 3: Collaborative reasoning
print("Turn 3:")
rule = View.from_str("∀x {AteLastCookie(x)}^{InKitchen(x)CrumbsOnShirt(x)}")
alice_conclusion = alice.reason_about(rule)
bob_conclusion = bob.reason_about(rule)

print(f"Alice: {alice._view_to_speech(alice_conclusion)}")
print(f"Bob: {bob._view_to_speech(bob_conclusion)}")

# ============================================================================
# PART 7: Advanced Dialogue Patterns
# ============================================================================
print("\n\n7. ADVANCED DIALOGUE PATTERNS")
print("-" * 30)

print("Key patterns for peer dialogue generation:")
print()
print("🔄 INFORMATION EXCHANGE:")
print("  • Use view.update() to incorporate new information")
print("  • Track what each peer knows vs. questions")
print("  • Model uncertainty with weighted states")
print()
print("❓ QUESTION-DRIVEN DIALOGUE:")
print("  • Use issue structures (*) to represent what's being questioned")
print("  • Questions drive the need for information sharing")
print("  • Resolution of issues advances the conversation")
print()
print("🤝 COLLABORATIVE REASONING:")
print("  • Peers can share reasoning rules")
print("  • Use default_inference_procedure for joint conclusions")
print("  • Factor out contradictions when peers disagree")
print()
print("🎯 DECISION-MAKING DIALOGUES:")
print("  • Use do-atoms for action-oriented conversations")
print("  • Model preferences with weighted states")
print("  • Use default_decision for group decisions")

# ============================================================================
# PART 8: Implementation Tips
# ============================================================================
print("\n\n8. IMPLEMENTATION TIPS")
print("-" * 30)

print("To build your own peer dialogue system:")
print()
print("1. 🏗️  PEER MODELING:")
print("   • Each peer has a current view (beliefs + questions)")
print("   • Track conversation history")
print("   • Model personality through reasoning preferences")
print()
print("2. 💬 DIALOGUE MANAGEMENT:")
print("   • Use view operations for information flow")
print("   • Questions in issue structures drive turn-taking")
print("   • Contradictions create interesting conflicts")
print()
print("3. 🧠 REASONING INTEGRATION:")
print("   • Apply inference procedures for conclusions")
print("   • Use suppose() for hypothetical reasoning")
print("   • Factor() to handle disagreements")
print()
print("4. 🎨 NATURAL LANGUAGE:")
print("   • Map view patterns to speech templates")
print("   • Use view.to_english() if available")
print("   • Consider emotional weights for tone")

print("\n" + "=" * 50)
print("🎉 Dialogue generation complete!")
print("Experiment with different scenarios, rules, and peer personalities!") 