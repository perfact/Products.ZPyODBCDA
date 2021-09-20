1.0.9.3.perfact4
================

- Drop separate escaping routine so the inherited one from ``Connection`` is
  used. In particular, escaping of apostrophes was broken and did not follow
  the SQL standard of doubling the apostrophe, instead trying to escape with a
  backslash.

1.0.9.3.perfact3
================

- Fix escaping routine. Since the transition to allow usage in both Python 2
  and 3, the joining tried to use a list as joiner, which does not work.
