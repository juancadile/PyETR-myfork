# Generating Peer Dialogue with PyETR

This guide explains how to use PyETR (Python Erotetic Theory of Reasoning) to generate dialogue between two or more reasoning peers.

## Core Concept

In PyETR, dialogue emerges naturally from the interaction between **views** (beliefs + questions) and **reasoning operations**. Each peer has their own view, and dialogue happens when they:

1. **Share information** (updating each other's views)
2. **Ask questions** (driven by issue structures)
3. **Reason together** (applying inference procedures)
4. **Resolve conflicts** (through evidence and factoring)

## Basic Dialogue Pattern

```python
from pyetr import View
from pyetr.inference import default_inference_procedure

# 1. Create initial peer views
alice_view = View.from_str("{InKitchen(John())}")  # Alice knows John was in kitchen
bob_view = View.from_str("∃x {AteLastCookie(x*)}")  # Bob questions who ate cookie

# 2. Information sharing
alice_shares = View.from_str("{InKitchen(John())}")
bob_updated = bob_view.update(alice_shares)  # Bob incorporates Alice's info

# 3. Collaborative reasoning
rule = View.from_str("∀x {AteLastCookie(x)}^{InKitchen(x)}")  # Rule: kitchen → ate cookie
conclusion = default_inference_procedure([bob_updated, rule])

print(f"Conclusion: {conclusion}")  # Who ate the cookie
```

## Key PyETR Operations for Dialogue

### 1. Information Exchange
- **`view.update(other_view)`** - Incorporate new information
- **`view.merge(other_view)`** - Combine views from external sources
- **`view.suppose(other_view)`** - Consider hypothetical scenarios

### 2. Question-Driven Dialogue
- **Issue structures (`*`)** - Mark what's being questioned
- **`∃x {Predicate(x*)}`** - "Someone did something, but who?"
- **`∀x {Conclusion(x*)}^{Evidence(x)}`** - "If evidence, then what conclusion?"

### 3. Reasoning Together
- **`default_inference_procedure([view1, view2, ...])`** - Draw joint conclusions
- **`view.answer(question_view)`** - Answer specific questions
- **`view.factor(contradiction)`** - Handle disagreements

### 4. Decision Making
- **`default_decision(dq, cv, pr)`** - Group decision making
- **Do-atoms (`do(Action())`)** - Represent actions/decisions
- **Weighted states** - Model preferences and uncertainty

## Dialogue Patterns

### Pattern 1: Information Sharing
```python
# Alice has information, Bob has questions
alice = View.from_str("{Fact()}")
bob = View.from_str("∃x {Unknown(x*)}")

# Bob incorporates Alice's information
bob_updated = bob.update(alice)
```

### Pattern 2: Disagreement Resolution
```python
# Conflicting beliefs
alice = View.from_str("{WillRain()}")
bob = View.from_str("{~WillRain()}")

# Conflict creates contradiction
combined = alice.update(bob)  # Results in falsum (contradiction)

# Resolution through new evidence
evidence = View.from_str("{DarkClouds()}")
rule = View.from_str("{WillRain()}^{DarkClouds()}")
resolution = default_inference_procedure([evidence, rule])
```

### Pattern 3: Collaborative Investigation
```python
# Question-driven inquiry
question = View.from_str("∃x {Guilty(x*)}")  # Who is guilty?
evidence1 = View.from_str("{AtScene(John())}")  # John was at scene
evidence2 = View.from_str("{HasMotive(John())}")  # John had motive
rule = View.from_str("∀x {Guilty(x)}^{AtScene(x)HasMotive(x)}")

# Collaborative reasoning
conclusion = default_inference_procedure([question, evidence1, evidence2, rule])
```

### Pattern 4: Negotiation and Compromise
```python
# Different preferences
alice_pref = View.from_str("{0.8=* Prefer(OptionA()),0.2=* Prefer(OptionB())}")
bob_pref = View.from_str("{0.3=* Prefer(OptionA()),0.7=* Prefer(OptionB())}")

# Decision with constraints
decision_question = View.from_str("{do(Choose(OptionA())),do(Choose(OptionB()))}")
constraints = View.from_str("{Expensive(OptionA()),Cheap(OptionB())}")

# Individual decisions
alice_choice = default_decision(dq=decision_question, cv=[constraints], pr=[alice_pref])
bob_choice = default_decision(dq=decision_question, cv=[constraints], pr=[bob_pref])

# Compromise
compromise = View.from_str("{0.5=* Prefer(OptionA()),0.5=* Prefer(OptionB())}")
final_decision = default_decision(dq=decision_question, cv=[constraints], pr=[compromise])
```

## Building a Dialogue System

### 1. Peer Class Structure
```python
class DialoguePeer:
    def __init__(self, name: str, initial_view: View):
        self.name = name
        self.view = initial_view
        self.conversation_history = []
    
    def share_information(self, info: View) -> str:
        """Share information with other peers"""
        return self._view_to_speech(info)
    
    def receive_information(self, info: View, from_peer: str) -> str:
        """Process incoming information"""
        old_view = self.view
        self.view = self.view.update(info)
        
        if self.view != old_view:
            return "That changes my thinking!"
        else:
            return "That's consistent with what I knew."
    
    def reason_about(self, rule: View) -> View:
        """Apply reasoning with a rule"""
        return default_inference_procedure([self.view, rule])
```

### 2. Dialogue Management
```python
def generate_dialogue(peers: list[DialoguePeer], scenario: dict):
    """Generate multi-turn dialogue"""
    
    for turn in scenario['turns']:
        speaker = peers[turn['speaker']]
        
        if turn['type'] == 'share':
            info = View.from_str(turn['content'])
            response = speaker.share_information(info)
            
            # Update other peers
            for peer in peers:
                if peer != speaker:
                    peer.receive_information(info, speaker.name)
        
        elif turn['type'] == 'question':
            question = View.from_str(turn['content'])
            # Handle question-driven dialogue
            
        elif turn['type'] == 'reason':
            rule = View.from_str(turn['content'])
            conclusion = speaker.reason_about(rule)
            # Share conclusion with others
```

### 3. Natural Language Generation
```python
def view_to_speech(view: View, context: str = "") -> str:
    """Convert PyETR view to natural language"""
    view_str = str(view)
    
    # Pattern matching for common expressions
    patterns = {
        r"InKitchen\((\w+)\(\)\)": r"I saw \1 in the kitchen",
        r"AteLastCookie\((\w+)\(\)\)": r"\1 ate the last cookie",
        r"∃x \{(\w+)\(x\*\)\}": r"Someone did something, but who?",
        r"do\((\w+)\(.*?\)\)": r"We should \1",
        r"~(\w+)\(\)": r"It's not the case that \1",
    }
    
    for pattern, replacement in patterns.items():
        view_str = re.sub(pattern, replacement, view_str)
    
    return view_str
```

## Advanced Features

### Uncertainty and Belief Revision
```python
# Model uncertainty with weights
uncertain_belief = View.from_str("{0.7=* Probably(Rain()),0.3=* Probably(Sunny())}")

# Update beliefs with new evidence
new_evidence = View.from_str("{DarkClouds()}")
revised_belief = uncertain_belief.update(new_evidence)
```

### Emotional States
```python
# Model emotions through weights
happy_peer = View.from_str("{2.0=* Positive(Mood()),0.1=* Negative(Mood())}")
sad_peer = View.from_str("{0.1=* Positive(Mood()),2.0=* Negative(Mood())}")

# Emotions affect reasoning and responses
```

### Multi-Agent Consensus
```python
def build_consensus(peers: list[DialoguePeer], issue: View) -> View:
    """Build consensus among multiple peers"""
    
    # Collect individual views
    individual_views = [peer.view for peer in peers]
    
    # Find common ground
    consensus = individual_views[0]
    for view in individual_views[1:]:
        consensus = consensus.update(view)
    
    # Apply group reasoning
    if not consensus.is_falsum:
        return default_inference_procedure([consensus, issue])
    else:
        # Handle disagreement through negotiation
        return negotiate_compromise(peers, issue)
```

## Example Scenarios

### 1. Mystery Solving
- **Setup**: Multiple witnesses with partial information
- **Goal**: Collaboratively determine what happened
- **Key**: Question-driven information sharing

### 2. Group Decision Making
- **Setup**: Team with different preferences and constraints
- **Goal**: Reach consensus on action to take
- **Key**: Weighted preferences and compromise

### 3. Scientific Collaboration
- **Setup**: Researchers with different hypotheses and evidence
- **Goal**: Converge on best explanation
- **Key**: Belief revision and evidence integration

### 4. Negotiation
- **Setup**: Parties with conflicting interests
- **Goal**: Find mutually acceptable solution
- **Key**: Constraint satisfaction and trade-offs

## Tips for Implementation

1. **Start Simple**: Begin with basic information sharing before adding complex reasoning
2. **Use Issue Structures**: Questions (`*`) drive natural dialogue flow
3. **Handle Contradictions**: Use `factor()` operations to resolve conflicts
4. **Model Personality**: Different reasoning preferences create distinct dialogue styles
5. **Track Context**: Maintain conversation history for coherent multi-turn dialogue
6. **Natural Language**: Develop good view-to-text conversion for readable output

## Running the Examples

```bash
# Basic dialogue example
python3 peer_dialogue_example.py

# Advanced patterns
python3 advanced_dialogue_patterns.py
```

The examples demonstrate practical implementations of these concepts with working code you can modify and extend for your own dialogue generation needs. 