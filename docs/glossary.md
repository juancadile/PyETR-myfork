# Glossary of operations and terms

## Arbitrary Object

A kind of term. Analogous to 'bound variable' in logic. Comes in two kinds: 'universal arbitrary objects' are analogous to universally quantified variables, 'existential arbitrary objects' are analogous to existentially quantified variables.

## Arity

The 'number' of arguments received by a function or predicate. In PyETR, this usually is a non-negative integer, but some terms such as Summation take a multiset of terms.

## Atom

Atoms are the smallest units with logical content in PyETR, corresponding to positive and negative atomic formulae in logic.
They are most often built out of [predicates](#predicate) possibly applied to [terms](#term). See also [do atoms](#do-atom) which can contain atoms.

## Constant

A 0-[arity](#arity) functional term.

## Default Reasoning Procedure

The erotetic theory of reason holds that the primary aim of reason is to answer a question a reasoner has taken on board as directly as possible and arrive at a residual view that includes only what is "novel" after a judgment is made. The default reasoning procedure is an algorithmic empirical hypothesis about what the central tendency of the system is in terms of inferences being made, expressed in terms of operations like [Update](#update), [Merge](#merge), Answer, and [Factor](#factor).

## Dependency

Existential arbitrary objects can have a dependency on a number of universal arbitrary objects.
If the existential $e$ depends on universals $u_1,\ldots,u_n$, this can be read as $e$ stands for a specific individual for every possible instantiation of $u_1,\ldots,u_n$.

## Dependency Relation

Contains the classifications of [arbitrary objects](#arbitrary-object) into universals and existentials, as well as any [dependencies](#dependency) between [arbitrary objects](#arbitrary-object).

## Do Atom

An atom formed by the keyword `do` applied to a [set](#set) of [atoms](#atom).
A chain of reasoning that ends in a view such as `{ do(A B C) }` means making a decision to 'act so as to make `A`, `B`, and `C` the case'.

## Factor

A view operation which reduces the complexity of the current view by factoring out the content of a second view.
An important special case is to 'factor out falsum', which drops any states that contain a primitive absurdity.

## Functional Term

A functional term represents a mathematical function. Can be a [constant](#constant) or contain other [terms](#term).

## Inquire

To pose a question on a starting view, where the question is represented as another view.

## Issue Context

A structure representing the location of the issue or question mark in an [atom](#atom).

## Issue Structure

The section of the [view](#view) that describes which parts of the [stage](#stage) and [supposition](#supposition) are at issue. Expressed as a series of pairs of [term](#term) and [issue contexts](#issue-context).

## Merge

Combine two views.

## Multiset

A multiset is a collection of objects which is *unordered* and *possibly has repeats*, cf. [Set](#set)
In ETR multisets are represented as comma-separated lists between double-angle brackets, thus

\[
    \llangle 1,1,2 \rrangle = \llangle 1,2,1 \rrangle = \llangle 2,1,1 \rrangle
\]

are three ways of writing the same thing: the multiset containing two copies of the number $1$ and one copy of the number $2$.

In ETR, multisets are always finite and can be empty.

## Novelization

Novelizing a set of [arbitrary objects](#arbitrary-object) in a [view](#view) (or [state](#state), etc) means selecting a replacement for each one, all distinct from any arbitrary object used up to that point, and systematically substituting the replacements for all occurrences of the originals.

The resulting view is 'alpha-equivalent' to the original one, in the sense familiar from logic, type theory, and programming languages.

## Predicate

A logic predicate that receives a certain number of arguments.

## Real Number

A type of [constant](#constant) with an associated numeric value.

## Query

A view operation for determining whether a given conclusion is directly supported by the current view.

## Set

A set is a collection of objects which is *unordered* and *without repeats*, cf [Multiset](#multiset).
As is standard, sets are represented as comma-separated lists between curly brackets, thus

\[
    \{1,2\} = \{2,1\} = \{1,1,2\}
\]

are three (of many possible) ways of writing the same thing: the set whose members are $1$ and $2$ only (note that repeating a member in the description has no effect). However, note that a [State](#state) is by definition a kind of set, but when a set is considered as a state we use a different notation, see [Stages and states](usage/view_construction.md#stages-and-states) and [Do atoms](usage/view_construction.md#do-atoms) in View construction.

In PyETR, all sets are finite, so we usually write 'set' when we really mean 'finite set'. In ETR, all sets involved in the construction of a [View](#view) are finite, but note that some entities, such as "the set of all views", are infinite sets.

## Stage

The main component of a view is the stage.
In general, the stage is a set of [weighted states](#weighted-state), but if all weights are trivial it will appear just as a set of [states](#state).

Intuitively, the stage expresses a disjunction of the states it contains, with extra non-logical information in the weights.

## State

A state is a [set](#set) of [atoms](#atom) and [do-atoms](#do-atom). Intuitively, a state expresses a conjunction of the atoms it contains.

## Supposition

A set of [weighted states](#weighted-state) representing a condition.

## Term

An [arbitrary object](#arbitrary-object) or [functional term](#functional-term).

## Update

`update` is a view operation. It is the workhorse of reasoning, being a key component of the [Default Reasoning Procedure](#default-reasoning-procedure).
For an initial view `G` and an incoming view `D`, `G.update(D)` is a view which updates `G` by treating `D` as a source of new information that potentially resolves some of the inquisitiveness of `G`.

`update` actually decomposes into more basic operations. In PyETR, `G.update(D)` 


 written $G[D]^\circlearrowright$ in R&I and `G.update(D)` in PyETR.


First View: Currently active point of view
Second View: Treated as a fact
Conclusion: New active point of view

Take a starting view, and when provided a new perspective produces a third view.

## View

A view is the basic object manipulated during reasoning. The current focus of a reasoner is taken to be a view. Incoming information arrives as a sequence of views, and latent beliefs are a collection of views. The different view operations correspond to different ways of evolving the current view in light of either new information or selected latent beliefs.

Views are built up from a [Stage](#stage), a [Supposition](#supposition), a [Dependency Relation](#dependency-relation), and an [Issue Structure](#issue-structure).

## Weight

A weight is a [multiset](#multiset) of [terms](#term) designated as either the additive or multiplicative weight in a [weighted state](#weighted-state).

## Weighted state

Each [state](#state) in a [stage](#stage) is equipped with extra non-logical content in the form of additive and multiplicative [weights](#weight), making it a weighted state.
States in [suppositions](#supposition) do not come with weights.
One or both of the weights can be empty.
A weighted state where both weights are the empty multiset is notated just as an ordinary state.




