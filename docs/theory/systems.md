# Systems from *Reason & Inquiry*

On this page we recap the structure of the book *Reason & Inquiry* and explain how to relate its contents to PyETR.

## Four versions of the ETR system

*Reason & Inquiry* incrementally builds up erotic theory vertically through successive degrees of expressive power in what views can represent.

- **Chapter 2:** introduces the most basic case: views that can express the contents of sentences in sentential logic.
- **Chapter 4:** adds terms and arbitrary objects. With these additions, views can now express the kinds of contents that first-order logic can talk about. In Stuart Russell’s slightly humorous phrase, this gives us the power "to represent the most important aspects of the real word, such as action, space, time, thoughts, and shopping".
- **Chapter 5:** introduces weighted states, that allow us to express reasoning under uncertainty.
- **Chapter 6:** introduces states with dual weights (multiplicative and additive) as well as do-atoms, allowing views to capture decision-making (under uncertainty).


The DNA of the reasoning operations of the erotetic theory stays the same throughout, in that subsequent increases of expressive power strictly generalise the weaker systems. In each level of expressive power do we get a version of the following result (informally stated here, but defined and proved formally in the book): 

If the judgment of the reasoner is in erotetic equilibrium (that is, the judgment is still available regardless of how many further questions are taken on board), then the judgment satisfies classical constraints on rational inference. For first-order and sentential logic equivalent expressive power, this means classical validity. For reasoning under uncertainty, this means Bayesian coherence. For decision making, this means rational choice. The book takes the view that it is not always a rational requirement to satisfy these standards.

PyETR implements the erotetic theory through Chapter 6, [with a few modifications](./differences.md). Since all of the other systems can be translated into the Chapter 6 one, this allows us to use PyETR to study examples written for any of the systems in R&I. In practice, this means there is occasionally a little notational overhead, most notable in [View Construction](../usage/view_construction.md).

## Translations between systems

Views in more primitive systems can be translated into the later systems.

- **Chapter 2 -> Chapter 4:** Treat Chapter 2 atoms as Chapter 4 atoms formed from nullary predicates, and leave the dependency relation and issue structure empty.

- **Chapter 4 -> Chapter 5:** Give each state in the stage the empty multiset $\llangle \rrangle$ as its weight.

- **Chapter 5 -> Chapter 6:** The existing weight of a state becomes its multiplicative weight and its additive weight becomes the empty multiset $\llangle \rrangle$.

These 'upwards' translations are designed to commute with view operations. Concretely, if we write the translation from Chapter $m$ views to Chapter $n$ views as $\uparrow_m^n$, then for any operation $O$ defined in Chapter $m$, firstly Chapter $n$ has an operation with the same name for example, and secondly if $G$ & $D$ are Chapter $m$ views then the following equation holds.

$$
\uparrow_m^n(G[D]^O) = (\uparrow_m^n G)[\uparrow_m^n D]^O
$$

See Theorem B.44 in R&I for the case of $\uparrow_4^5$.

It sometimes seems reasonable to consider 'downwards' translations as well. The step from 5 to 4 works well: we simply drop the weights from the states. We can go from 6 to 5 by forgetting the additive weights and possibly removing any do-atoms. There does not seem to be any feasible way to go from 4 to 2 that preserves a reasonable amount of content. Moreover, downwards translates should not be expected to commute with reasoning operations, see Theorem B.45 in R&I.

