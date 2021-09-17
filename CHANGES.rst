1.0.9.3.perfact3
================

- Fix escaping routine. Since the transition to allow usage in both Python 2
  and 3, the joining tried to use a list as joiner, which does not work.
