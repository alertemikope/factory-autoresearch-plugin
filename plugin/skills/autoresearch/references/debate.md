# Debate Protocol

## Roles

- Explorer: generate candidate hypotheses with expected upside and test plan.
- Critic A: produce the first adversarial read on the proposals.
- Critic B: critique the proposals independently, then challenge Critic A where their reasoning looks weak or incomplete.
- Judge: choose the next experiment using evidence, not rhetoric.

## Explorer output

For each hypothesis provide:

- title
- expected impact
- files or surfaces touched
- why it might work
- fastest valid test

## Critic exchange

Critic A should review the explorer output first.

For each hypothesis Critic A provides:

- strongest objection
- failure mode
- Goodhart risk
- lower-risk variant if available

Critic B then responds with:

- independent objection
- agreement_or_disagreement_with_critic_a
- what_critic_a_missed
- preferred_variant
- decision_risk_if_promoted

## Judge rubric

Score proposals on:

- expected impact
- testability
- implementation cost
- regression risk
- novelty vs past lessons
- evaluator integrity

The judge must explicitly cite the main disagreement between Critic A and Critic B before selecting one winner, or at most two isolated winners for parallel execution.

## Rule

Debate narrows the search space. It never replaces mechanical verification.
